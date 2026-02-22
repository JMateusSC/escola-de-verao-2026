# 💡 Dicas - Experimento 2: Observabilidade

## Estratégia Geral

🎯 **Dica Principal**: Logs estruturados em JSON são fáceis de filtrar e analisar. Use ferramentas como `grep`, `jq`, ou Python para processar os dados.

---

## 🔍 Analisando Logs Estruturados

<details>
<summary>Dica 1: Como contar requisições processadas?</summary>

Procure por logs que indicam conclusão de requisição. Há duas possibilidades:
- Logs com "completed successfully" (sucesso)
- Logs com "failed" (erro)

```bash
# Contar sucessos
grep "completed successfully" logs.json | wc -l

# Contar erros
grep "failed" logs.json | wc -l

# Total = sucessos + erros
```

</details>

<details>
<summary>Dica 2: Como identificar o tipo de erro?</summary>

Logs de erro contêm o campo `context.error_type`. Procure por:

```json
{
  "level": "ERROR",
  "context": {
    "error_type": "ValueError",
    "error_message": "Simulated processing error"
  }
}
```

Use `grep` ou Python para extrair esses campos.

</details>

<details>
<summary>Dica 3: Como rastrear uma requisição específica?</summary>

Use o `request_id` para ver todos os logs relacionados:

```bash
# Ver todos os logs de req-003
grep '"request_id": "req-003"' logs.json
```

Você verá:
1. Log de início ("Processing request")
2. Log de conclusão ("completed" ou "failed")
3. Log de métricas (DEBUG com latency_ms)

</details>

---

## 📊 Interpretando Golden Signals

<details>
<summary>Dica 1: O que é uma latência saudável?</summary>

**Referências gerais:**
- **< 100ms**: Excelente - usuário não percebe atraso
- **100-500ms**: Aceitável - pequeno atraso perceptível
- **500-1000ms**: Problemático - atraso notável
- **> 1000ms**: Crítico - experiência ruim

No experimento, a latência média deve estar entre 10-100ms (processamento simulado).

</details>

<details>
<summary>Dica 2: Como calcular taxa de erro?</summary>

Fórmula:

```
Taxa de Erro (%) = (Número de Erros / Total de Requisições) × 100
```

Exemplo:
- Total: 10 requisições
- Erros: 1 requisição
- Taxa: (1 / 10) × 100 = 10%

**Referências:**
- **< 1%**: Excelente
- **1-5%**: Aceitável
- **5-10%**: Atenção necessária
- **> 10%**: Crítico

</details>

<details>
<summary>Dica 3: O que significa saturação?</summary>

Saturação mede o uso de recursos (CPU, memória, disco, rede).

No experimento, medimos CPU:
- **< 70%**: Sistema saudável, tem capacidade de sobra
- **70-85%**: Atenção, sistema está ficando carregado
- **> 85%**: Crítico, sistema pode ficar lento ou instável

</details>

<details>
<summary>Dica 4: Como os Golden Signals se relacionam?</summary>

Os 4 sinais estão interconectados:

1. **Tráfego alto** → pode causar **saturação alta**
2. **Saturação alta** → pode causar **latência alta**
3. **Latência alta** → pode causar **timeouts** (erros)
4. **Erros altos** → indicam problema no sistema

Procure por essas correlações nos dados!

</details>

---

## 🛠️ Usando Ferramentas de Análise

<details>
<summary>Dica 1: Como usar grep para filtrar logs?</summary>

```bash
# Filtrar por nível
grep '"level": "ERROR"' logs.json

# Filtrar por request_id
grep '"request_id": "req-005"' logs.json

# Filtrar por mensagem
grep "failed" logs.json

# Combinar filtros (AND)
grep '"level": "ERROR"' logs.json | grep "ValueError"
```

</details>

<details>
<summary>Dica 2: Como usar jq para processar JSON?</summary>

`jq` é uma ferramenta poderosa para JSON:

```bash
# Extrair apenas mensagens
cat logs.json | jq '.message'

# Filtrar por nível
cat logs.json | jq 'select(.level == "ERROR")'

# Extrair latências
cat logs.json | jq 'select(.context.latency_ms) | .context.latency_ms'

# Calcular média de latências
cat logs.json | jq -s 'map(select(.context.latency_ms)) | map(.context.latency_ms) | add / length'
```

</details>

<details>
<summary>Dica 3: Como usar Python para análise?</summary>

```python
import json

# Carregar logs
with open("logs.json") as f:
    logs = [json.loads(line) for line in f]

# Filtrar erros
errors = [log for log in logs if log["level"] == "ERROR"]
print(f"Erros: {len(errors)}")

# Calcular latência média
latencies = [
    log["context"]["latency_ms"]
    for log in logs
    if "latency_ms" in log.get("context", {})
]
avg_latency = sum(latencies) / len(latencies)
print(f"Latência média: {avg_latency:.2f}ms")

# Contar tipos de erro
error_types = {}
for log in errors:
    error_type = log["context"].get("error_type", "Unknown")
    error_types[error_type] = error_types.get(error_type, 0) + 1
print(f"Tipos de erro: {error_types}")
```

</details>

---

## 🔎 Identificando Padrões

<details>
<summary>Dica 1: Como identificar picos de latência?</summary>

1. Extraia todas as latências dos logs DEBUG
2. Calcule a média e desvio padrão
3. Identifique valores > média + 2×desvio

```python
import statistics

latencies = [55.2, 48.3, 52.1, 150.5, 49.8]  # exemplo
mean = statistics.mean(latencies)
stdev = statistics.stdev(latencies)

outliers = [l for l in latencies if l > mean + 2 * stdev]
print(f"Picos de latência: {outliers}")
```

</details>

<details>
<summary>Dica 2: Como detectar degradação gradual?</summary>

Compare métricas ao longo do tempo:

1. Divida os logs em janelas de tempo (ex: a cada 10 requisições)
2. Calcule métricas para cada janela
3. Observe se há tendência de piora

```python
# Exemplo: latência por janela
window_size = 5
for i in range(0, len(logs), window_size):
    window = logs[i:i+window_size]
    latencies = [log["context"]["latency_ms"] for log in window if "latency_ms" in log.get("context", {})]
    if latencies:
        print(f"Janela {i//window_size}: {sum(latencies)/len(latencies):.2f}ms")
```

</details>

<details>
<summary>Dica 3: Como correlacionar erros com latência?</summary>

Verifique se requisições que falharam tinham latência diferente:

```python
# Latência de requisições bem-sucedidas
success_logs = [log for log in logs if "completed successfully" in log["message"]]
success_latencies = [log["context"]["latency_ms"] for log in success_logs if "latency_ms" in log.get("context", {})]

# Latência de requisições que falharam
error_logs = [log for log in logs if log["level"] == "ERROR"]
# Note: erros podem não ter latência no mesmo log, precisa correlacionar por request_id

print(f"Latência média (sucesso): {sum(success_latencies)/len(success_latencies):.2f}ms")
```

</details>

---

## 📈 Interpretando Resultados

<details>
<summary>Dica 1: O que fazer se a taxa de erro for alta?</summary>

**Taxa de erro > 10%** indica problema sério:

1. **Identifique o tipo de erro**: Todos os erros são do mesmo tipo?
2. **Procure padrões**: Erros acontecem em horários específicos?
3. **Verifique recursos**: Sistema está saturado?
4. **Analise logs**: Há mensagens de erro detalhadas?

No experimento, erros são simulados aleatoriamente (10% de chance), então taxa ~10% é esperada.

</details>

<details>
<summary>Dica 2: O que fazer se a latência for alta?</summary>

**Latência > 500ms** requer investigação:

1. **Identifique requisições lentas**: Quais request_ids têm alta latência?
2. **Procure correlação**: Latência alta coincide com saturação alta?
3. **Verifique erros**: Requisições lentas também falharam?
4. **Analise contexto**: Há algo especial nessas requisições?

</details>

<details>
<summary>Dica 3: Como saber se o sistema está saudável?</summary>

**Sistema saudável:**
- ✅ Latência < 100ms
- ✅ Taxa de erro < 1%
- ✅ Saturação < 70%
- ✅ Tráfego estável

**Sistema com problemas:**
- ❌ Latência > 1000ms
- ❌ Taxa de erro > 10%
- ❌ Saturação > 85%
- ❌ Tráfego caindo (usuários desistindo)

</details>

---

## 🎯 Exercícios Práticos

<details>
<summary>Exercício 1: Análise Básica</summary>

Execute o serviço e responda:

1. Quantas requisições foram processadas?
2. Quantas falharam?
3. Qual foi a taxa de erro?
4. Qual foi a latência média?

**Dica**: Use `grep` e `wc -l` para contar, ou carregue os logs em Python.

</details>

<details>
<summary>Exercício 2: Rastreamento de Requisição</summary>

Escolha uma requisição que falhou e rastreie-a:

1. Encontre o log de início
2. Encontre o log de erro
3. Veja qual foi o tipo de erro
4. Verifique se há log de métricas

**Dica**: Use `grep` com o `request_id`.

</details>

<details>
<summary>Exercício 3: Análise de Tendências</summary>

Execute o serviço 3 vezes e compare:

1. A taxa de erro é consistente?
2. A latência média varia muito?
3. A saturação é estável?

**Dica**: Erros são aleatórios (10%), então haverá variação.

</details>

---

## 🆘 Ainda com Dúvidas?

Se após usar essas dicas você ainda estiver com dificuldades:

1. Execute o serviço novamente e observe os logs em tempo real
2. Use o analisador de logs (`log_analyzer.py`) para filtrar dados
3. Compare seus resultados com `solution/ANALYSIS_GUIDE.md`
4. Experimente modificar o código para gerar mais/menos erros

## 📚 Conceitos-Chave

- **Logs estruturados**: Formato JSON facilita análise automatizada
- **Golden Signals**: 4 métricas fundamentais (Latência, Tráfego, Erros, Saturação)
- **Tracing**: Rastreamento via `request_id`
- **Correlação**: Conectar eventos nos logs com mudanças nas métricas
- **Análise de tendências**: Observar mudanças ao longo do tempo

Boa análise! 🔍
