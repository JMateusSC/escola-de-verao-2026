# 📖 Guia de Análise Completo - Observabilidade

## Visão Geral

Este guia apresenta uma análise completa do experimento de observabilidade, explicando como interpretar logs estruturados, analisar métricas (Golden Signals), e identificar problemas em sistemas distribuídos.

---

## 🔍 Análise dos Logs

### Estrutura dos Logs

O serviço emite logs estruturados em formato JSON. Cada log contém:

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

**Campos importantes:**
- `timestamp`: Permite ordenar eventos cronologicamente
- `level`: Indica severidade (DEBUG < INFO < WARNING < ERROR < CRITICAL)
- `message`: Descrição legível do evento
- `context`: Dados estruturados adicionais (variável por tipo de log)
- `request_id`: Permite rastrear uma requisição do início ao fim

### Tipos de Logs Emitidos

O serviço emite 3 tipos de logs por requisição:

#### 1. Log de Início (INFO)
```json
{
  "level": "INFO",
  "message": "Processing request req-001",
  "context": {"data_size": 42},
  "request_id": "req-001"
}
```

**Indica**: Requisição foi recebida e está sendo processada.

#### 2. Log de Conclusão (INFO ou ERROR)

**Sucesso:**
```json
{
  "level": "INFO",
  "message": "Request req-001 completed successfully",
  "context": {"status": "success"},
  "request_id": "req-001"
}
```

**Falha:**
```json
{
  "level": "ERROR",
  "message": "Request req-003 failed: Simulated processing error",
  "context": {
    "error_type": "ValueError",
    "error_message": "Simulated processing error"
  },
  "request_id": "req-003"
}
```

**Indica**: Resultado final do processamento.

#### 3. Log de Métricas (DEBUG)
```json
{
  "level": "DEBUG",
  "message": "Request req-001 metrics",
  "context": {
    "latency_ms": 55.3,
    "total_requests": 1
  },
  "request_id": "req-001"
}
```

**Indica**: Métricas de performance da requisição.

### Exemplo de Análise: Rastreando uma Requisição

Vamos rastrear `req-003` que falhou:

```bash
grep '"request_id": "req-003"' logs.json
```

**Resultado:**
```json
{"timestamp": "2024-01-15T14:30:45.100", "level": "INFO", "message": "Processing request req-003", ...}
{"timestamp": "2024-01-15T14:30:45.150", "level": "ERROR", "message": "Request req-003 failed: Simulated processing error", ...}
{"timestamp": "2024-01-15T14:30:45.151", "level": "DEBUG", "message": "Request req-003 metrics", "context": {"latency_ms": 51.2, ...}}
```

**Análise:**
1. **14:30:45.100**: Requisição iniciada
2. **14:30:45.150**: Falhou após 50ms com `ValueError`
3. **14:30:45.151**: Latência registrada: 51.2ms

**Conclusão**: Requisição falhou rapidamente (não foi timeout), erro foi durante processamento.

---

## 📊 Análise dos Golden Signals

### O que são Golden Signals?

Conceito criado pelo Google SRE (Site Reliability Engineering). São as **4 métricas fundamentais** para monitorar qualquer sistema:

1. **Latency (Latência)**: Quanto tempo leva para processar requisições
2. **Traffic (Tráfego)**: Quantas requisições o sistema está processando
3. **Errors (Erros)**: Quantas requisições estão falhando
4. **Saturation (Saturação)**: Quão "cheio" está o sistema (uso de recursos)

### 1. Latency (Latência)

**Definição**: Tempo de resposta das requisições, medido em milissegundos.

**Exemplo de métrica:**
```json
{
  "latency": 55.3
}
```

**Interpretação:**
- **< 100ms**: ✅ Excelente - usuário não percebe atraso
- **100-500ms**: ⚠️ Aceitável - pequeno atraso perceptível
- **500-1000ms**: ⚠️ Problemático - atraso notável
- **> 1000ms**: ❌ Crítico - experiência ruim

**No experimento**: Latência média ~50ms é excelente.

**Como calcular:**
```python
# Extrair latências dos logs DEBUG
latencies = [
    log["context"]["latency_ms"]
    for log in logs
    if "latency_ms" in log.get("context", {})
]

# Calcular média
avg_latency = sum(latencies) / len(latencies)
print(f"Latência média: {avg_latency:.2f}ms")

# Calcular percentis
latencies_sorted = sorted(latencies)
p50 = latencies_sorted[len(latencies) // 2]
p95 = latencies_sorted[int(len(latencies) * 0.95)]
p99 = latencies_sorted[int(len(latencies) * 0.99)]

print(f"P50: {p50:.2f}ms")
print(f"P95: {p95:.2f}ms")
print(f"P99: {p99:.2f}ms")
```

**Por que percentis importam?**
- **Média** pode esconder problemas (um outlier de 10s aumenta pouco a média)
- **P95** mostra a experiência de 95% dos usuários
- **P99** mostra a experiência dos 1% mais lentos (ainda importante!)

### 2. Traffic (Tráfego)

**Definição**: Volume de requisições processadas.

**Exemplo de métrica:**
```json
{
  "traffic": 10
}
```

**Interpretação:**
- Indica carga no sistema
- Útil para detectar picos ou quedas anormais
- Ajuda a dimensionar recursos

**No experimento**: 10 requisições é baixo (teste), produção pode ter milhares/segundo.

**Como analisar:**
```python
# Contar requisições por minuto
from datetime import datetime
from collections import defaultdict

requests_per_minute = defaultdict(int)
for log in logs:
    if "Processing request" in log["message"]:
        timestamp = datetime.fromisoformat(log["timestamp"])
        minute = timestamp.strftime("%Y-%m-%d %H:%M")
        requests_per_minute[minute] += 1

for minute, count in sorted(requests_per_minute.items()):
    print(f"{minute}: {count} requisições")
```

**Padrões a observar:**
- **Pico súbito**: Pode indicar ataque ou evento viral
- **Queda súbita**: Pode indicar problema (usuários não conseguem acessar)
- **Padrão diário**: Normal ter mais tráfego em horários de pico

### 3. Errors (Erros)

**Definição**: Quantidade de requisições que falharam.

**Exemplo de métrica:**
```json
{
  "errors": 1
}
```

**Interpretação:**
- **Taxa de erro** é mais útil que número absoluto
- Fórmula: `(erros / total) × 100`

**Referências:**
- **< 0.1%**: ✅ Excelente (1 erro a cada 1000 requisições)
- **0.1-1%**: ✅ Bom (1-10 erros a cada 1000)
- **1-5%**: ⚠️ Aceitável (10-50 erros a cada 1000)
- **5-10%**: ⚠️ Problemático (50-100 erros a cada 1000)
- **> 10%**: ❌ Crítico (> 100 erros a cada 1000)

**No experimento**: Taxa ~10% é esperada (simulação aleatória).

**Como calcular:**
```python
# Contar erros
error_logs = [log for log in logs if log["level"] == "ERROR"]
error_count = len(error_logs)

# Contar total de requisições
total_requests = len([log for log in logs if "Processing request" in log["message"]])

# Calcular taxa
error_rate = (error_count / total_requests) * 100
print(f"Taxa de erro: {error_rate:.2f}%")

# Analisar tipos de erro
error_types = {}
for log in error_logs:
    error_type = log["context"].get("error_type", "Unknown")
    error_types[error_type] = error_types.get(error_type, 0) + 1

print("Tipos de erro:")
for error_type, count in error_types.items():
    print(f"  {error_type}: {count}")
```

**Tipos de erro comuns:**
- **ValueError**: Dados inválidos
- **TimeoutError**: Operação demorou demais
- **ConnectionError**: Falha de rede
- **PermissionError**: Falta de permissão

### 4. Saturation (Saturação)

**Definição**: Utilização de recursos (CPU, memória, disco, rede).

**Exemplo de métrica:**
```json
{
  "saturation": 67.2
}
```

**Interpretação (CPU):**
- **< 70%**: ✅ Saudável - sistema tem capacidade de sobra
- **70-85%**: ⚠️ Atenção - sistema está ficando carregado
- **85-95%**: ⚠️ Crítico - sistema pode ficar lento
- **> 95%**: ❌ Emergência - sistema pode travar

**No experimento**: CPU ~67% é saudável.

**Como analisar:**
```python
# Extrair saturação ao longo do tempo
saturations = []
for log in logs:
    if "metrics" in log["message"]:
        # Saturação é atualizada a cada requisição
        # Precisamos buscar no serviço, não nos logs
        pass

# No experimento, saturação é simulada aleatoriamente (20-80%)
# Em produção, você coletaria de ferramentas de monitoramento
```

**Outros recursos a monitorar:**
- **Memória**: % de RAM usada
- **Disco**: % de espaço usado, IOPS
- **Rede**: Largura de banda usada, pacotes perdidos
- **Threads/Conexões**: Pool de threads/conexões disponíveis

---

## 🔗 Correlacionando Logs e Métricas

### Exemplo 1: Erro causou aumento de latência?

**Hipótese**: Requisições que falharam tiveram latência diferente.

**Análise:**
```python
# Latência de requisições bem-sucedidas
success_latencies = []
error_latencies = []

for log in logs:
    if "latency_ms" in log.get("context", {}):
        request_id = log["request_id"]
        latency = log["context"]["latency_ms"]
        
        # Verificar se essa requisição teve erro
        has_error = any(
            l["request_id"] == request_id and l["level"] == "ERROR"
            for l in logs
        )
        
        if has_error:
            error_latencies.append(latency)
        else:
            success_latencies.append(latency)

print(f"Latência média (sucesso): {sum(success_latencies)/len(success_latencies):.2f}ms")
print(f"Latência média (erro): {sum(error_latencies)/len(error_latencies):.2f}ms")
```

**Resultado esperado**: Latências similares, pois erros são simulados aleatoriamente (não por timeout).

### Exemplo 2: Pico de tráfego causou saturação?

**Hipótese**: Quando tráfego aumenta, CPU aumenta.

**Análise:**
```python
# Agrupar por janelas de tempo
from datetime import datetime, timedelta

window_size = timedelta(seconds=10)
windows = {}

for log in logs:
    if "Processing request" in log["message"]:
        timestamp = datetime.fromisoformat(log["timestamp"])
        window = timestamp.replace(second=timestamp.second // 10 * 10, microsecond=0)
        
        if window not in windows:
            windows[window] = {"requests": 0, "cpu": []}
        
        windows[window]["requests"] += 1

# Correlacionar com CPU (simplificado)
for window, data in sorted(windows.items()):
    print(f"{window}: {data['requests']} requisições")
```

**Resultado esperado**: Em produção, mais requisições → mais CPU. No experimento, CPU é aleatória.

### Exemplo 3: Degradação gradual

**Hipótese**: Métricas pioram ao longo do tempo (ex: memory leak).

**Análise:**
```python
# Dividir logs em janelas
window_size = 5
for i in range(0, len(logs), window_size):
    window_logs = logs[i:i+window_size]
    
    # Calcular métricas da janela
    latencies = [
        log["context"]["latency_ms"]
        for log in window_logs
        if "latency_ms" in log.get("context", {})
    ]
    
    errors = [log for log in window_logs if log["level"] == "ERROR"]
    
    if latencies:
        print(f"Janela {i//window_size}:")
        print(f"  Latência média: {sum(latencies)/len(latencies):.2f}ms")
        print(f"  Erros: {len(errors)}")
```

**Resultado esperado**: No experimento, métricas são estáveis. Em produção, degradação indica problema.

---

## 🎯 Cenários Práticos de Análise

### Cenário 1: Taxa de Erro Alta

**Sintoma**: Taxa de erro subiu de 1% para 15%.

**Investigação:**

1. **Quando começou?**
   ```python
   # Encontrar primeiro erro
   first_error = next(log for log in logs if log["level"] == "ERROR")
   print(f"Primeiro erro: {first_error['timestamp']}")
   ```

2. **Qual tipo de erro?**
   ```python
   # Contar tipos
   error_types = {}
   for log in logs:
       if log["level"] == "ERROR":
           error_type = log["context"].get("error_type", "Unknown")
           error_types[error_type] = error_types.get(error_type, 0) + 1
   ```

3. **Há padrão?**
   - Todos os erros são do mesmo tipo?
   - Erros acontecem em horários específicos?
   - Erros afetam requisições específicas?

4. **Correlação com outras métricas?**
   - Latência aumentou junto?
   - CPU está alta?
   - Houve deploy recente?

**Ações:**
- Se erro específico: Investigar código relacionado
- Se erro aleatório: Pode ser problema de infraestrutura
- Se erro em horário específico: Pode ser carga ou job agendado

### Cenário 2: Latência Alta

**Sintoma**: Latência P95 subiu de 100ms para 2000ms.

**Investigação:**

1. **Quais requisições estão lentas?**
   ```python
   # Encontrar requisições com latência > 1000ms
   slow_requests = [
       log for log in logs
       if log.get("context", {}).get("latency_ms", 0) > 1000
   ]
   ```

2. **Há padrão?**
   - Todas as requisições estão lentas ou apenas algumas?
   - Requisições lentas têm algo em comum?

3. **Correlação com saturação?**
   - CPU está alta?
   - Memória está cheia?
   - Disco está lento?

4. **Há erros relacionados?**
   - Requisições lentas também falharam?
   - Há timeouts?

**Ações:**
- Se todas lentas: Problema de infraestrutura (CPU, rede)
- Se algumas lentas: Problema de código (query lenta, loop infinito)
- Se latência crescente: Memory leak ou cache cheio

### Cenário 3: Sistema Instável

**Sintoma**: Métricas oscilam muito (latência varia de 50ms a 5000ms).

**Investigação:**

1. **Calcular variabilidade:**
   ```python
   import statistics
   
   latencies = [log["context"]["latency_ms"] for log in logs if "latency_ms" in log.get("context", {})]
   mean = statistics.mean(latencies)
   stdev = statistics.stdev(latencies)
   
   print(f"Média: {mean:.2f}ms")
   print(f"Desvio padrão: {stdev:.2f}ms")
   print(f"Coeficiente de variação: {(stdev/mean)*100:.2f}%")
   ```

2. **Identificar outliers:**
   ```python
   outliers = [l for l in latencies if l > mean + 2 * stdev]
   print(f"Outliers: {outliers}")
   ```

3. **Procurar causa:**
   - Garbage collection?
   - Contenção de recursos (locks)?
   - Rede instável?

**Ações:**
- Analisar logs de GC
- Verificar locks e concorrência
- Monitorar rede

---

## 📈 Boas Práticas de Observabilidade

### 1. Logging Estruturado

**✅ Bom:**
```json
{
  "level": "ERROR",
  "message": "Database query failed",
  "context": {
    "query": "SELECT * FROM users WHERE id = ?",
    "error": "Connection timeout",
    "duration_ms": 5000
  }
}
```

**❌ Ruim:**
```
ERROR: Database query failed: Connection timeout
```

**Por quê?**
- JSON é fácil de parsear automaticamente
- Campos estruturados permitem filtros precisos
- Contexto rico facilita debugging

### 2. Use Request IDs

**✅ Bom:**
```json
{"request_id": "req-123", "message": "Processing request"}
{"request_id": "req-123", "message": "Query executed"}
{"request_id": "req-123", "message": "Request completed"}
```

**Por quê?**
- Permite rastrear requisição do início ao fim
- Essencial em sistemas distribuídos
- Facilita debugging de problemas específicos

### 3. Log Níveis Apropriados

- **DEBUG**: Informação detalhada para debugging (ex: valores de variáveis)
- **INFO**: Eventos normais do sistema (ex: requisição processada)
- **WARNING**: Algo inesperado mas não crítico (ex: retry bem-sucedido)
- **ERROR**: Erro que precisa atenção (ex: requisição falhou)
- **CRITICAL**: Sistema em estado crítico (ex: banco de dados inacessível)

### 4. Monitore os 4 Golden Signals

Sempre monitore:
1. **Latency**: Tempo de resposta
2. **Traffic**: Volume de requisições
3. **Errors**: Taxa de erro
4. **Saturation**: Uso de recursos

Esses 4 sinais cobrem a maioria dos problemas.

### 5. Defina SLOs (Service Level Objectives)

Exemplo:
- **Latência P95 < 200ms** (95% das requisições respondem em < 200ms)
- **Taxa de erro < 0.1%** (99.9% de sucesso)
- **Disponibilidade > 99.9%** (< 43 minutos de downtime por mês)

SLOs ajudam a definir o que é "saudável".

---

## ✅ Checklist de Análise

Use este checklist ao analisar logs e métricas:

### Análise de Logs
- [ ] Logs estão em formato estruturado (JSON)?
- [ ] Logs contêm timestamp, level, message, context?
- [ ] Há request_id para rastreamento?
- [ ] Logs de erro contêm stack trace ou contexto suficiente?
- [ ] Níveis de log estão apropriados?

### Análise de Métricas
- [ ] Latência está dentro do esperado?
- [ ] Taxa de erro está aceitável?
- [ ] Saturação está saudável?
- [ ] Tráfego está no padrão esperado?
- [ ] Há tendências preocupantes (crescimento de erros, latência)?

### Correlação
- [ ] Erros correlacionam com latência alta?
- [ ] Picos de tráfego causam saturação?
- [ ] Há degradação gradual ao longo do tempo?
- [ ] Eventos externos (deploy, horário) afetam métricas?

### Ações
- [ ] Problemas identificados estão documentados?
- [ ] Causa raiz foi investigada?
- [ ] Ações corretivas foram definidas?
- [ ] Alertas foram configurados para prevenir recorrência?

---

## 🎓 Lições Aprendidas

### 1. Observabilidade ≠ Monitoring

- **Monitoring**: Saber que algo está errado (alerta dispara)
- **Observabilidade**: Entender **por quê** está errado (logs e métricas)

Observabilidade permite investigar problemas desconhecidos.

### 2. Logs Estruturados São Essenciais

Logs em texto livre são difíceis de analisar automaticamente. JSON permite:
- Filtros precisos
- Agregações
- Correlações
- Dashboards automáticos

### 3. Golden Signals Cobrem 80% dos Problemas

Monitorar centenas de métricas é confuso. Os 4 Golden Signals cobrem a maioria dos problemas:
- Latência alta → usuários insatisfeitos
- Erros altos → funcionalidade quebrada
- Saturação alta → sistema lento
- Tráfego anormal → ataque ou problema

### 4. Contexto É Fundamental

Um log sem contexto é inútil:

**❌ Ruim**: `"Error processing request"`  
**✅ Bom**: `"Error processing request req-123: Database timeout after 5000ms on query SELECT * FROM users"`

### 5. Correlação Revela Causa Raiz

Analisar métricas isoladamente pode enganar:
- Latência alta pode ser causada por CPU alta
- CPU alta pode ser causada por pico de tráfego
- Pico de tráfego pode ser causado por ataque

Correlacionar eventos revela a cadeia de causalidade.

---

## 🚀 Próximos Passos

Após completar este experimento, você sabe:

✅ Interpretar logs estruturados em JSON  
✅ Analisar Golden Signals (Latência, Tráfego, Erros, Saturação)  
✅ Rastrear requisições usando request_id  
✅ Correlacionar logs com métricas  
✅ Identificar padrões e anomalias  

**Próximo experimento**: Experimento 3 - Concorrência (race conditions)

---

## 📚 Referências

- [Google SRE Book - Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- [The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals)
- [Structured Logging](https://www.structlog.org/en/stable/why.html)
- [Distributed Tracing](https://opentelemetry.io/docs/concepts/observability-primer/#distributed-traces)
- [Observability Engineering by Charity Majors](https://www.oreilly.com/library/view/observability-engineering/9781492076438/)
