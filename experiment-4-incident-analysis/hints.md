# Dicas para Análise do Incidente

Este arquivo contém dicas progressivas para ajudá-lo na investigação. Tente resolver o máximo possível sozinho antes de consultar as dicas!

## 🔍 Dica 1: Por Onde Começar?

<details>
<summary>Clique para revelar</summary>

Comece analisando as **métricas** (`logs/metrics.json`) para entender o comportamento do sistema ao longo do tempo:

1. Procure pelo momento em que as métricas começaram a degradar
2. Observe especialmente:
   - `latency_ms` (latência média)
   - `errors_percent` (taxa de erro)
   - `db_connections_active` (conexões de banco ativas)

Você notará algo interessante acontecendo por volta das 14:25-14:27...

</details>

---

## 🔍 Dica 2: O Que Procurar nos Logs da Aplicação?

<details>
<summary>Clique para revelar</summary>

Nos logs da aplicação (`logs/application.log`), procure por:

1. **Mensagens de WARNING e ERROR** próximas ao horário do incidente (14:25-14:30)
2. **Palavras-chave importantes**:
   - "connection pool"
   - "exhausted"
   - "timeout"
   - "leak"

Preste atenção especial nas mensagens sobre o estado do pool de conexões. O que está acontecendo com as conexões?

</details>

---

## 🔍 Dica 3: O Que os Logs do Banco Revelam?

<details>
<summary>Clique para revelar</summary>

Nos logs do banco de dados (`logs/database.log`), procure por:

1. **Estado das conexões**: Quantas conexões estão ativas? Há um limite?
2. **Mensagens de erro**: "FATAL: sorry, too many clients already"
3. **Transações longas**: Há transações que ficam abertas por muito tempo?
4. **Estado "idle in transaction"**: O que isso significa?

Dica importante: Uma transação "idle in transaction" significa que foi iniciada com BEGIN mas nunca foi finalizada com COMMIT ou ROLLBACK. Isso mantém a conexão ocupada!

</details>

---

## 🔍 Dica 4: Correlacionando os Eventos

<details>
<summary>Clique para revelar</summary>

Tente correlacionar estes eventos:

1. **13:00**: O que aconteceu neste horário? (Veja `incident_scenario.md`)
2. **14:25**: As métricas começam a degradar
3. **14:27**: O pool de conexões esgota completamente
4. **14:31**: Uma análise de "connection leak" é registrada

Há uma relação entre o deploy das 13:00 e o problema que começou às 14:25?

</details>

---

## 🔍 Dica 5: Identificando o Módulo Problemático

<details>
<summary>Clique para revelar</summary>

Procure nos logs por menções a módulos específicos da aplicação:

- `payment_service`
- `cashback_service`
- `notification_service`

Qual desses módulos aparece frequentemente nas mensagens de erro e warnings sobre conexões?

Dica: Olhe especialmente para as mensagens sobre "connection leak" e "idle in transaction" - elas mencionam qual módulo está causando o problema.

</details>

---

## 🔍 Dica 6: O Padrão do Vazamento

<details>
<summary>Clique para revelar</summary>

Nos logs do banco, há uma mensagem muito reveladora sobre o padrão das conexões vazadas:

```
Common pattern: BEGIN -> INSERT notifications -> NO COMMIT/ROLLBACK
```

O que isso significa?
- Uma transação é iniciada (BEGIN)
- Um INSERT é executado
- Mas a transação nunca é finalizada!

Qual módulo está fazendo INSERTs em notifications? E por que ele não está finalizando as transações?

</details>

---

## 🔍 Dica 7: Por Que o Restart Não Funcionou?

<details>
<summary>Clique para revelar</summary>

Observe o que aconteceu após o restart do serviço (14:50):

1. As conexões foram fechadas
2. O serviço reiniciou
3. Mas... o problema voltou rapidamente!

Por quê? Porque o **bug no código** ainda estava lá. O restart apenas limpou as conexões, mas não corrigiu o código que estava vazando conexões.

Isso é uma pista importante: o problema não era de infraestrutura ou configuração, mas sim um **bug no código** introduzido recentemente.

</details>

---

## 🔍 Dica 8: A Nova Feature

<details>
<summary>Clique para revelar</summary>

No `incident_scenario.md`, você verá que a versão 2.4.0 incluía:
- **Nova feature de cashback automático**
- Refatoração do módulo de notificações
- Atualização de dependências

E nos logs, você vê problemas com:
- `cashback_service`
- Inserções em `notifications`
- Transações não finalizadas

Conecte os pontos: A nova feature de cashback está relacionada ao problema de vazamento de conexões!

</details>

---

## 🔍 Dica 9: Estruturando os 5 Porquês

<details>
<summary>Clique para revelar</summary>

Aqui está uma estrutura sugerida para seus 5 Porquês:

1. **Por quê #1**: Por quê os usuários tiveram timeouts?
   - Resposta: Algo sobre não conseguir conexões com o banco...

2. **Por quê #2**: Por quê não havia conexões disponíveis?
   - Resposta: Algo sobre o pool estar esgotado...

3. **Por quê #3**: Por quê o pool estava esgotado?
   - Resposta: Algo sobre vazamento de conexões...

4. **Por quê #4**: Por quê as conexões estavam vazando?
   - Resposta: Algo sobre transações não finalizadas...

5. **Por quê #5**: Por quê as transações não estavam sendo finalizadas?
   - Resposta: Algo sobre o código do cashback_service...

Cada resposta deve levar naturalmente à próxima pergunta!

</details>

---

## 🔍 Dica 10: Ações Preventivas

<details>
<summary>Clique para revelar</summary>

Pense em ações em três níveis:

**Curto Prazo (Imediato)**:
- Corrigir o bug no código
- Adicionar testes que detectem o problema
- Melhorar monitoramento

**Médio Prazo (Semanas)**:
- Melhorar processo de code review
- Adicionar análise estática (linters)
- Criar testes de carga automatizados

**Longo Prazo (Meses)**:
- Treinamento da equipe
- Melhorar observabilidade
- Implementar práticas de SRE (runbooks, game days)

Seja específico! Em vez de "melhorar testes", diga "adicionar teste de integração que verifica se todas as conexões são fechadas após cada requisição".

</details>

---

## 🔍 Dica 11: Evidências Concretas

<details>
<summary>Clique para revelar</summary>

Para cada resposta nos 5 Porquês, você deve fornecer **evidências concretas** dos logs. Por exemplo:

❌ **Ruim**: "O pool de conexões estava cheio"

✅ **Bom**: "O pool de conexões estava esgotado, como evidenciado por:
```
application.log:
2024-03-15T14:27:05.678Z [ERROR] database_pool - Connection pool exhausted

database.log:
2024-03-15 14:27:05 UTC [LOG] active connections: 100/100 (EXHAUSTED)
```"

Sempre cite trechos específicos dos logs!

</details>

---

## 🔍 Dica 12: Validando Sua Causa Raiz

<details>
<summary>Clique para revelar</summary>

Uma boa causa raiz deve:

1. ✅ **Explicar todos os sintomas**: Sua causa raiz explica os timeouts, a alta latência, a taxa de erro, e o pool esgotado?

2. ✅ **Ser acionável**: Você pode fazer algo concreto para corrigir?

3. ✅ **Ser verificável**: O rollback para v2.3.5 resolveu o problema? Isso confirma que a v2.4.0 era a causa?

4. ✅ **Não ter "por quê" mais profundo relevante**: Se você perguntar "por quê" mais uma vez, a resposta seria sobre treinamento, processo, ou cultura - que são suas ações preventivas, não a causa raiz técnica.

Se sua causa raiz não atende a esses critérios, você pode não ter ido fundo o suficiente (ou foi longe demais)!

</details>

---

## 💡 Lembre-se

- **Sintomas não são causas raiz**: "Pool de conexões esgotado" é um sintoma, não a causa raiz
- **Use evidências**: Cada afirmação deve ser suportada por dados dos logs
- **Seja específico**: "Bug no código" não é específico o suficiente - qual código? Qual bug?
- **Pense em prevenção**: A análise só é útil se levar a ações que previnem recorrência

Boa investigação! 🔍
