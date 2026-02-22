# Experimento 4: Análise de Incidente com a Técnica dos 5 Porquês

## 🎯 Objetivos de Aprendizado

Ao completar este experimento, você será capaz de:

1. **Analisar logs de incidentes** para identificar sintomas e padrões de falha
2. **Aplicar a técnica dos 5 Porquês** para descobrir a causa raiz de um problema
3. **Distinguir entre sintomas e causas raiz** em cenários de falha complexos
4. **Interpretar métricas de observabilidade** (Golden Signals) durante incidentes
5. **Propor ações preventivas** baseadas na análise de causa raiz
6. **Correlacionar eventos** em múltiplas fontes de dados (logs de aplicação, banco de dados, métricas)

## 📖 Contexto

Você é um engenheiro de software em uma equipe de e-commerce. Um incidente crítico ocorreu no sistema de pagamentos, causando timeouts generalizados e perda de transações. Sua missão é investigar o incidente, identificar a causa raiz usando a técnica dos 5 Porquês, e propor ações para prevenir recorrência.

## 🔍 Cenário do Incidente

Leia o arquivo `incident_scenario.md` para entender:
- O que aconteceu e quando
- Sintomas observados pelos usuários
- Métricas de performance durante o incidente
- Contexto do sistema e deploys recentes
- Impacto no negócio

## 📊 Dados Disponíveis

Você tem acesso a três fontes de dados para sua investigação:

### 1. Logs da Aplicação (`logs/application.log`)
Contém eventos do sistema de pagamentos, incluindo:
- Processamento de pagamentos
- Erros e warnings
- Eventos de deploy e operações
- Alertas de monitoramento

### 2. Logs do Banco de Dados (`logs/database.log`)
Contém informações sobre:
- Conexões de banco de dados
- Queries executadas
- Estado do pool de conexões
- Transações e locks

### 3. Métricas do Sistema (`logs/metrics.json`)
Contém os **Golden Signals** coletados a cada minuto:
- **Latência**: Tempo de resposta (média, P95, P99)
- **Tráfego**: Requisições por segundo
- **Erros**: Taxa de erro em porcentagem
- **Saturação**: Uso de CPU, memória, conexões de banco

## 🛠️ Instruções

### Passo 1: Análise Inicial dos Dados

1. **Leia o cenário do incidente** (`incident_scenario.md`)
   - Anote o horário de início dos sintomas
   - Identifique o que mudou recentemente no sistema
   - Liste os sintomas principais

2. **Analise as métricas** (`logs/metrics.json`)
   - Identifique quando as métricas começaram a degradar
   - Observe quais métricas foram mais afetadas
   - Procure por correlações entre diferentes métricas

3. **Examine os logs da aplicação** (`logs/application.log`)
   - Procure por erros e warnings próximos ao horário do incidente
   - Identifique padrões de falha
   - Note mensagens que indicam problemas de recursos

4. **Investigue os logs do banco** (`logs/database.log`)
   - Verifique o estado das conexões
   - Procure por transações longas ou travadas
   - Identifique mensagens de erro relacionadas a recursos

### Passo 2: Aplicar a Técnica dos 5 Porquês

1. **Abra o template** `five_whys_template.md`

2. **Comece com o sintoma inicial**
   - Descreva o problema observado pelos usuários
   - Use dados concretos dos logs e métricas

3. **Faça a primeira pergunta "Por quê?"**
   - Por quê esse sintoma ocorreu?
   - Baseie sua resposta em evidências dos logs
   - Cite trechos específicos dos logs como evidência

4. **Continue perguntando "Por quê?"**
   - Para cada resposta, pergunte novamente "Por quê?"
   - Vá cada vez mais fundo na cadeia de causalidade
   - Sempre forneça evidências dos logs

5. **Identifique a causa raiz**
   - Quando você chegar a uma causa que:
     - Explica todos os sintomas
     - É acionável (pode ser corrigida)
     - Não tem um "por quê" mais profundo relevante
   - Essa é sua causa raiz!

6. **Proponha ações preventivas**
   - Liste ações de curto, médio e longo prazo
   - Seja específico e prático
   - Considere mudanças em código, processo e monitoramento

### Passo 3: Validação

1. **Compare sua análise** com a solução de referência em `solution/ROOT_CAUSE_ANALYSIS.md`
   - Você identificou a mesma causa raiz?
   - Suas evidências foram similares?
   - Suas ações preventivas fazem sentido?

2. **Reflita sobre o processo**
   - O que foi mais desafiador na análise?
   - Quais logs foram mais úteis?
   - Como você poderia melhorar o processo de investigação?

## 💡 Dicas

Precisa de ajuda? Consulte o arquivo `hints.md` para dicas progressivas sem revelar a solução completa.

## 🎓 Conceitos Relacionados

Este experimento aplica conceitos apresentados na aula:

- **Técnica dos 5 Porquês**: Método de análise de causa raiz através de perguntas sucessivas
- **Golden Signals**: Métricas fundamentais de observabilidade (Latência, Tráfego, Erros, Saturação)
- **Análise de Logs**: Técnicas para extrair informações relevantes de logs estruturados
- **Correlação de Eventos**: Conectar eventos em diferentes fontes de dados
- **Sintoma vs Causa Raiz**: Distinguir entre o que é observado e o que causou o problema
- **Ações Preventivas**: Transformar análise em melhorias concretas

## 📚 Recursos Adicionais

- [The Five Whys - Toyota Production System](https://en.wikipedia.org/wiki/Five_whys)
- [Google SRE Book - Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
- [The Four Golden Signals - Google SRE](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Incident Analysis: How Learning is Different Than Fixing](https://www.adaptivecapacitylabs.com/blog/2018/03/23/incident-analysis-how-learning-is-different-than-fixing/)

## ✅ Critérios de Sucesso

Você completou o experimento com sucesso quando:

- ✅ Analisou todas as três fontes de dados (logs de aplicação, banco, métricas)
- ✅ Preencheu o template dos 5 Porquês com perguntas e respostas
- ✅ Forneceu evidências concretas dos logs para cada resposta
- ✅ Identificou uma causa raiz que explica todos os sintomas
- ✅ Propôs pelo menos 3 ações preventivas (curto, médio, longo prazo)
- ✅ Comparou sua análise com a solução de referência

## 🚀 Próximos Passos

Após completar este experimento:

1. **Pratique com incidentes reais**: Aplique a técnica dos 5 Porquês em problemas do seu trabalho
2. **Melhore o monitoramento**: Pense em quais métricas/logs ajudariam a detectar este problema mais cedo
3. **Compartilhe conhecimento**: Discuta sua análise com colegas e compare abordagens
4. **Crie runbooks**: Documente como responder a incidentes similares no futuro

---

**Tempo estimado**: 45-60 minutos

**Dificuldade**: ⭐⭐⭐ Intermediário

**Pré-requisitos**: Conhecimento básico de sistemas web, bancos de dados e logs
