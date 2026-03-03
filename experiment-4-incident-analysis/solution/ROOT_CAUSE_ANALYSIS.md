# Análise de Causa Raiz - Técnica dos 5 Porquês

## Sobre a Técnica

A técnica dos **5 Porquês** é um método de análise de causa raiz desenvolvido por Sakichi Toyoda e usado no Sistema Toyota de Produção. O objetivo é ir além dos sintomas superficiais e descobrir a causa raiz de um problema através de perguntas sucessivas "Por quê?".

---

## Sintoma Inicial

**Descreva o problema observado pelos usuários ou pelo sistema:**

Sistema de pagamentos com timeouts generalizados. Taxa de erro saltou de 0.1% para 15% e latência de 200ms para 8.000ms.

**Quando ocorreu:**

15 de março de 2024, às 14:30 BRT (1h30 após deploy da versão 2.4.0)

**Impacto:**

- 3.500 usuários afetados
- R$ 125.000 em receita perdida

---

## Análise dos 5 Porquês

### Por quê #1?

**Pergunta:** Por quê os usuários experimentaram timeouts no sistema de pagamentos?

**Resposta:**

Requisições não conseguiam obter conexões com o banco de dados.

**Evidências:**

```
application.log:
2024-03-15T14:27:05.890Z [WARN] payment_service - Database connection timeout request_id=pay_901 wait_time=5.2s
2024-03-15T14:29:12.345Z [ERROR] database_pool - Connection pool exhausted for 60 seconds, active_connections=100 waiting_requests=45
```

---

### Por quê #2?

**Pergunta:** Por quê o pool de conexões do banco de dados estava esgotado?

**Resposta:**

Conexões não estavam sendo liberadas. Ficaram em estado "idle in transaction" por mais de 30 segundos.

**Evidências:**

```
application.log:
2024-03-15T14:31:15.234Z [WARN] database_pool - Connection leak detected: 23 connections held for >30 seconds

database.log:
2024-03-15 14:31:15 UTC [WARN]   - 23 connections held for >30 seconds
2024-03-15 14:31:15 UTC [WARN]   - All leaked connections in state: idle in transaction
2024-03-15 14:31:15 UTC [WARN]   - Common pattern: BEGIN -> INSERT notifications -> NO COMMIT/ROLLBACK
```

---

### Por quê #3?

**Pergunta:** Por quê as conexões não estavam sendo liberadas?

**Resposta:**

Transações iniciadas com `BEGIN` não eram finalizadas com `COMMIT` ou `ROLLBACK`. O módulo de cashback abria transações mas não as fechava.

**Evidências:**

```
database.log:
2024-03-15 14:31:15 UTC [WARN]   - Common pattern: BEGIN -> INSERT notifications -> NO COMMIT/ROLLBACK
2024-03-15 14:31:15 UTC [WARN]   - Application: payment_app (cashback_service module)
2024-03-15 14:45:45 UTC [WARN] Transaction pid=12389 has been idle in transaction for 20m
```

---

### Por quê #4?

**Pergunta:** Por quê o módulo de cashback não estava finalizando as transações?

**Resposta:**

A nova feature de cashback (v2.4.0) não inclui tratamento de exceções nem garante finalização de transações quando ocorrem erros no envio de notificações.

**Evidências:**

```
application.log:
2024-03-15T14:30:45.789Z [INFO] cashback_service - Calculating cashback for user_id=usr_9234 amount=200.00
2024-03-15T14:30:46.012Z [ERROR] notification_service - Failed to send notification user_id=usr_9234 error=DatabaseConnectionTimeout
2024-03-15T14:31:00.123Z [ERROR] cashback_service - Failed to record cashback user_id=usr_9234 error=DatabaseConnectionTimeout
```

---

### Por quê #5?

**Pergunta:** Por quê o código da feature de cashback não incluiu tratamento adequado de transações?

**Resposta:**

Não foram implementados blocos `try-finally` ou context managers. Além disso, a atualização do SQLAlchemy de 1.4 para 2.0 mudou o comportamento de transações, e o código não foi adaptado.

**Evidências:**

- Restart do serviço não resolveu (problema no código, não no estado)
- Pool esgotou novamente após restart (14:51:45)
- Apenas rollback para v2.3.5 resolveu o problema

---

## Causa Raiz Identificada

**Resumo da Causa Raiz:**

Implementação inadequada do gerenciamento de transações na feature de cashback (v2.4.0). O código não usa context managers para garantir finalização de transações, causando connection leaks que esgotaram o pool.

**Por que esta é a causa raiz e não apenas um sintoma?**

- Explica todos os sintomas observados
- É acionável (pode ser corrigida no código)
- Rollback para versão anterior resolveu imediatamente
- Restart não resolveu (confirma que é código, não estado)

---

## Ações Preventivas

### 1. Ação Imediata (Curto Prazo)

**O quê:**

Corrigir o código do módulo de cashback usando context managers do SQLAlchemy 2.0:

```python
# ANTES (v2.4.0 - INCORRETO)
def calculate_and_notify_cashback(user_id, amount):
    session.begin()
    cashback = calculate_cashback(amount)
    session.execute(insert_cashback_query)
    send_notification(user_id, cashback)  # Se falhar, não faz commit/rollback
    session.commit()

# DEPOIS (CORRETO)
def calculate_and_notify_cashback(user_id, amount):
    try:
        with session.begin():  # Garante commit ou rollback
            cashback = calculate_cashback(amount)
            session.execute(insert_cashback_query)
            send_notification(user_id, cashback)
    except Exception as e:
        logger.error(f"Failed to process cashback: {e}")
        raise
```

**Responsável:** Equipe de Backend

**Prazo:** 24 horas

---

### 2. Ação de Médio Prazo

**O quê:**

Implementar monitoramento proativo de connection leaks:

- Alerta quando uso do pool > 70%
- Alerta para transações > 10 segundos
- Dashboard de estado do pool em tempo real
- Métrica de conexões "idle in transaction"

**Responsável:** Equipe de SRE

**Prazo:** 1 semana

---

### 3. Ação de Longo Prazo

**O quê:**

Estabelecer processo de prevenção:

- Code review checklist para gerenciamento de recursos
- Linter para detectar `session.begin()` sem context manager
- Testes de integração validando liberação de conexões
- Testes de carga antes de deploys
- Documentação de boas práticas SQLAlchemy 2.0

**Responsável:** Tech Lead + QA

**Prazo:** 1 mês

---

## Lições Aprendidas

**O que funcionou bem durante o incidente?**

- Monitoramento detectou o problema em 5 minutos
- PagerDuty alertou a equipe automaticamente
- Logs estruturados permitiram identificar o padrão
- Decisão de rollback foi rápida após restart falhar

**O que poderia ter sido melhor?**

- Testes de carga antes do deploy
- Code review não identificou o problema
- Faltou alerta de uso do pool antes de 100%
- Tempo até rollback foi longo (30 minutos)

**Conhecimento adquirido:**

- SQLAlchemy 2.0 mudou comportamento de transações - sempre usar context managers
- Connection leaks esgotam pool rapidamente
- Restart não resolve problemas de código
- Monitoramento de recursos é crítico

---

## Validação

**Como você validará que as ações preventivas foram efetivas?**

- Testes automatizados validando liberação de conexões
- Testes de carga (2x carga normal por 1 hora)
- Monitoramento de métricas por 1 semana após correção
- Code review checklist em 100% dos PRs

**Métricas de sucesso:**
- Pool nunca ultrapassa 70%
- Zero transações "idle in transaction" > 10s
- Taxa de erro < 0.5%

**Data de revisão:**

- Imediata: 1 semana após correção (22/03/2024)
- Médio prazo: 1 mês (15/04/2024)
- Longo prazo: 3 meses (15/06/2024)

---

## Diagrama de Causalidade

```
Timeouts no sistema de pagamentos
    ↓ Por quê?
Requisições não conseguiam conexões de banco
    ↓ Por quê?
Pool de conexões esgotado (100/100)
    ↓ Por quê?
Conexões não sendo liberadas (idle in transaction)
    ↓ Por quê?
Transações não finalizadas com COMMIT/ROLLBACK
    ↓ Por quê?
Código sem context managers + SQLAlchemy 2.0
    ↓
🎯 CAUSA RAIZ: Gerenciamento inadequado de transações
   na feature de cashback (v2.4.0)
```
