# Experimento 2: Observabilidade - Análise de Logs e Métricas

## 🎯 Objetivos de Aprendizado

Ao completar este experimento, você será capaz de:

1. **Analisar logs estruturados**: Interpretar logs em formato JSON com contexto rico
2. **Identificar problemas através de logs**: Usar logs para detectar falhas e comportamentos anômalos
3. **Monitorar Golden Signals**: Entender e analisar as 4 métricas fundamentais de observabilidade
4. **Correlacionar logs e métricas**: Conectar eventos nos logs com mudanças nas métricas

## 📚 Descrição do Experimento

Este experimento simula um **serviço web observável** que:

- Processa requisições de forma assíncrona
- Emite logs estruturados em formato JSON
- Coleta métricas de observabilidade (Golden Signals)
- Simula falhas ocasionais para análise

Você irá analisar os logs e métricas para identificar padrões, detectar problemas e entender o comportamento do sistema.

## 🔍 Golden Signals

Os **Golden Signals** são as 4 métricas fundamentais para monitorar qualquer sistema:

1. **Latency (Latência)**: Tempo de resposta das requisições (em milissegundos)
2. **Traffic (Tráfego)**: Volume de requisições processadas
3. **Errors (Erros)**: Quantidade de requisições que falharam
4. **Saturation (Saturação)**: Utilização de recursos (CPU, memória, etc.)

## 📊 Estrutura dos Logs

Cada log é um objeto JSON com os seguintes campos:

```json
{
  "timestamp": "2024-01-15T14:30:45.123456",
  "level": "INFO",
  "message": "Processing request req-001",
  "context": {
    "data_size": 42
  },
  "request_id": "req-001"
}
```

**Campos:**
- `timestamp`: Data e hora do evento (ISO 8601)
- `level`: Severidade (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `message`: Descrição do evento
- `context`: Dados contextuais adicionais
- `request_id`: Identificador para rastreamento (tracing)

## 🔍 Instruções

### Passo 1: Executar o Serviço

Execute o serviço para gerar logs e métricas:

```bash
python code/experiment-2-observability/service.py
```

Observe:
- Logs estruturados sendo emitidos
- Algumas requisições falhando (simulação de erros)
- Métricas finais (Golden Signals)

### Passo 2: Analisar os Logs

Examine os logs gerados e responda:

1. **Quantas requisições foram processadas?**
   - Dica: Conte logs com "completed successfully"

2. **Quantas requisições falharam?**
   - Dica: Conte logs com level "ERROR"

3. **Qual foi a taxa de erro?**
   - Fórmula: `(erros / total) * 100`

4. **Qual foi o tipo de erro mais comum?**
   - Dica: Olhe o campo `context.error_type`

5. **Qual requisição teve maior latência?**
   - Dica: Procure logs DEBUG com `context.latency_ms`

### Passo 3: Analisar as Métricas

Examine as métricas finais (Golden Signals):

```json
{
  "latency": 55.3,
  "traffic": 10,
  "errors": 1,
  "saturation": 67.2
}
```

Responda:

1. **A latência está saudável?**
   - Referência: < 100ms é bom, < 500ms é aceitável, > 1000ms é problemático

2. **A taxa de erro está aceitável?**
   - Referência: < 1% é excelente, < 5% é aceitável, > 10% é crítico

3. **O sistema está saturado?**
   - Referência: < 70% é saudável, 70-85% é atenção, > 85% é crítico

### Passo 4: Usar o Analisador de Logs

Use a ferramenta `log_analyzer.py` para filtrar e analisar logs:

```python
from log_analyzer import LogAnalyzer

analyzer = LogAnalyzer()

# Carregar logs de um arquivo
logs = analyzer.load_logs("logs.json")

# Filtrar por nível
errors = analyzer.filter_by_level(logs, "ERROR")
print(f"Encontrados {len(errors)} erros")

# Filtrar por período
recent = analyzer.filter_by_timerange(
    logs,
    "2024-01-15T14:00:00",
    "2024-01-15T15:00:00"
)

# Calcular taxa de erro
error_rate = analyzer.calculate_error_rate(logs)
print(f"Taxa de erro: {error_rate:.2f}%")
```

### Passo 5: Identificar Padrões

Procure por padrões nos logs:

1. **Erros correlacionados**: Erros acontecem em sequência ou isolados?
2. **Picos de latência**: Há requisições com latência muito acima da média?
3. **Degradação gradual**: As métricas pioram ao longo do tempo?
4. **Horários críticos**: Há horários com mais erros ou latência?

## 💡 Estratégias de Análise

### 1. Comece pelos Erros

Erros são os sinais mais óbvios de problemas:

```bash
# Filtrar apenas logs de erro
grep '"level": "ERROR"' logs.json
```

### 2. Use request_id para Rastreamento

O `request_id` permite rastrear uma requisição do início ao fim:

```bash
# Ver todos os logs de uma requisição específica
grep '"request_id": "req-003"' logs.json
```

### 3. Analise Tendências

Compare métricas ao longo do tempo:
- Latência está aumentando?
- Taxa de erro está crescendo?
- CPU está subindo?

### 4. Correlacione Eventos

Conecte logs com métricas:
- Um erro causou aumento de latência?
- Um pico de tráfego causou saturação?

## 📝 Conceitos Relacionados

Este experimento aplica conceitos da apresentação:

- **Observabilidade**: Capacidade de entender o estado interno do sistema através de outputs externos
- **Logging Estruturado**: Logs em formato JSON para facilitar análise automatizada
- **Golden Signals**: As 4 métricas fundamentais (Latência, Tráfego, Erros, Saturação)
- **Tracing**: Rastreamento de requisições através do sistema usando IDs únicos
- **Análise de Logs**: Técnicas para extrair insights de logs

## 🆘 Precisa de Ajuda?

- **Dicas progressivas**: Consulte `hints.md` para dicas de análise
- **Análise completa**: Após completar, veja `solution/ANALYSIS_GUIDE.md`

## ✅ Checklist de Conclusão

- [ ] Executei o serviço e observei os logs
- [ ] Identifiquei quantas requisições falharam
- [ ] Calculei a taxa de erro
- [ ] Analisei as métricas (Golden Signals)
- [ ] Usei o analisador de logs para filtrar eventos
- [ ] Identifiquei padrões nos logs
- [ ] Correlacionei logs com métricas
- [ ] Entendi o que cada Golden Signal representa

## 🎓 Próximos Passos

Após completar este experimento, você estará pronto para:
- **Experimento 3**: Concorrência (race conditions)
- **Experimento 4**: Análise de Incidente (técnica dos 5 Porquês)

Boa análise! 🔍
