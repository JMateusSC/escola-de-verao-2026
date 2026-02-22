# Incidente: Falha no Sistema de Pagamentos

## Resumo Executivo

Em 15 de março de 2024, às 14:30 BRT, o sistema de pagamentos da plataforma de e-commerce apresentou degradação severa de performance, resultando em timeouts generalizados e perda de transações. O incidente durou aproximadamente 45 minutos e afetou cerca de 3.500 usuários.

## Timeline do Incidente

| Horário | Evento |
|---------|--------|
| 13:00 | Deploy da versão 2.4.0 em produção (incluindo nova feature de cashback) |
| 14:25 | Primeiros alertas de latência elevada no sistema de pagamentos |
| 14:30 | Taxa de erro ultrapassa threshold crítico (15%) |
| 14:32 | Equipe de plantão notificada via PagerDuty |
| 14:35 | Início da investigação - análise de logs e métricas |
| 14:45 | Identificação de pool de conexões de banco esgotado |
| 14:50 | Tentativa de restart do serviço (sem sucesso) |
| 15:00 | Decisão de rollback para versão 2.3.5 |
| 15:10 | Rollback concluído - sistema voltando ao normal |
| 15:15 | Métricas normalizadas - incidente resolvido |

## Sintomas Observados

### Performance
- **Latência média**: Aumentou de 200ms para 8.000ms
- **P95 latência**: Subiu de 500ms para 15.000ms
- **P99 latência**: Atingiu 30.000ms (timeout do cliente)

### Disponibilidade
- **Taxa de erro**: Saltou de 0.1% para 15% em 5 minutos
- **Taxa de sucesso**: Caiu de 99.9% para 85%
- **Timeouts**: 450 requisições/minuto resultando em timeout

### Tráfego
- **Volume de requisições**: 1.000 req/min (normal para horário)
- **Requisições bem-sucedidas**: Apenas 850 req/min
- **Requisições falhando**: 150 req/min

### Recursos
- **CPU**: 45% (normal)
- **Memória**: 62% (normal)
- **Conexões de banco**: 100/100 (ESGOTADO)
- **Thread pool**: 80/200 (normal)

## Contexto do Sistema

### Arquitetura
- **Aplicação**: Python 3.11 com Flask
- **Banco de dados**: PostgreSQL 14
- **Pool de conexões**: Configurado com máximo de 100 conexões
- **Infraestrutura**: 4 instâncias EC2 t3.large atrás de load balancer

### Deploy Recente
A versão 2.4.0 incluía:
- Nova feature de cashback automático
- Refatoração do módulo de notificações
- Atualização de dependências (SQLAlchemy 1.4 → 2.0)
- Melhorias de logging

### Condições Operacionais
- **Horário**: Período de pico moderado (14h30)
- **Carga**: Dentro do esperado para o horário
- **Infraestrutura**: Sem problemas reportados na AWS
- **Dependências externas**: Todos os serviços externos operacionais

## Impacto no Negócio

- **Transações perdidas**: Aproximadamente 6.750 tentativas de pagamento
- **Usuários afetados**: ~3.500 usuários únicos
- **Receita estimada perdida**: R$ 125.000
- **Tickets de suporte**: 89 tickets abertos
- **Reclamações em redes sociais**: 23 menções negativas

## Dados Disponíveis para Investigação

Os seguintes arquivos de log estão disponíveis para análise:

1. **logs/application.log**: Logs da aplicação com eventos do sistema de pagamentos
2. **logs/database.log**: Logs do PostgreSQL mostrando conexões e queries
3. **logs/metrics.json**: Métricas dos Golden Signals coletadas durante o incidente

## Questões para Investigação

1. Por que a taxa de erro aumentou tão rapidamente?
2. Por que o pool de conexões de banco esgotou?
3. Qual a relação entre o deploy da versão 2.4.0 e o incidente?
4. Por que o restart do serviço não resolveu o problema?
5. Como prevenir que isso aconteça novamente?

## Próximos Passos

Use a técnica dos **5 Porquês** para investigar a causa raiz deste incidente. Analise os logs disponíveis e preencha o template `five_whys_template.md` com sua análise.
