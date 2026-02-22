# Experimento 3 - Concorrência e Race Conditions

## Objetivos de Aprendizado

Ao completar este experimento, você será capaz de:

1. **Identificar race conditions** em código concorrente
2. **Reproduzir problemas de concorrência** de forma consistente
3. **Entender o conceito de operações atômicas** e seções críticas
4. **Aplicar mecanismos de sincronização** (locks) para resolver race conditions
5. **Validar thread safety** através de testes

## Contexto

Race conditions são um dos bugs mais difíceis de detectar e corrigir em software. Elas ocorrem quando múltiplas threads acessam dados compartilhados simultaneamente, e pelo menos uma delas modifica os dados. O resultado final depende da ordem de execução das threads, tornando o comportamento não-determinístico.

### O que é uma Race Condition?

Uma race condition acontece quando:
1. Duas ou mais threads acessam a mesma variável/recurso
2. Pelo menos uma thread modifica o recurso
3. Não há sincronização adequada entre as threads
4. O resultado depende do timing de execução (não-determinístico)

### Exemplo Clássico: Operação Read-Modify-Write

```python
# Thread 1                    # Thread 2
current = balance  # 100      current = balance  # 100
new_value = current + 10      new_value = current + 20
balance = new_value  # 110    balance = new_value  # 120

# Resultado final: 120 (perdemos o depósito de 10!)
# Resultado esperado: 130
```

## Estrutura do Experimento

```
experiment-3-concurrency/
├── README.md                    # Este arquivo
├── race_condition.py            # Código BUGGY com race condition
├── solution/
│   ├── fixed_concurrent.py      # Código CORRETO thread-safe
│   └── SOLUTION_GUIDE.md        # Explicação detalhada da solução
└── hints.md                     # Dicas progressivas
```

## Instruções

### Parte 1: Observar a Race Condition

1. **Execute o código buggy múltiplas vezes:**

```bash
python code/experiment-3-concurrency/race_condition.py
```

2. **Observe os resultados:**
   - Execute pelo menos 5 vezes
   - Anote os diferentes resultados que você obtém
   - Perceba que o mesmo código produz resultados diferentes

3. **Perguntas para reflexão:**
   - Por que os resultados são diferentes a cada execução?
   - Qual é o resultado esperado? Por que não obtemos esse resultado?
   - Em que momento exatamente ocorre o problema?

### Parte 2: Entender o Problema

1. **Analise o código em `race_condition.py`:**
   - Identifique a classe `BankAccount`
   - Examine os métodos `deposit()` e `withdraw()`
   - Observe a função `run_concurrent_transactions()`

2. **Identifique a seção crítica:**
   - Qual parte do código acessa dados compartilhados?
   - Onde ocorre a operação read-modify-write?
   - Por que o `time.sleep()` amplifica o problema?

3. **Use o debugger (opcional):**
   - Configure breakpoints nos métodos `deposit()` e `withdraw()`
   - Execute com múltiplas threads
   - Observe como as threads intercalam suas execuções

### Parte 3: Implementar a Solução

1. **Crie sua própria solução:**
   - Copie `race_condition.py` para um novo arquivo
   - Adicione sincronização usando `threading.Lock`
   - Use o context manager `with lock:` para proteger seções críticas

2. **Teste sua solução:**
   - Execute múltiplas vezes
   - Verifique se o resultado é sempre consistente
   - Compare com o resultado esperado

3. **Se precisar de ajuda:**
   - Consulte `hints.md` para dicas progressivas
   - Veja a solução completa em `solution/fixed_concurrent.py`
   - Leia a explicação detalhada em `solution/SOLUTION_GUIDE.md`

### Parte 4: Validar com Testes

1. **Execute os testes automatizados:**

```bash
pytest code/experiment-3-concurrency/test_race_condition.py -v
pytest code/experiment-3-concurrency/test_thread_safe.py -v
```

2. **Entenda os testes:**
   - Os testes demonstram a race condition de forma automatizada
   - Property tests validam consistência com parâmetros aleatórios
   - Testes executam múltiplas iterações para detectar problemas intermitentes

## Conceitos Importantes

### Threading.Lock

Um lock (mutex) garante exclusão mútua - apenas uma thread pode adquirir o lock por vez:

```python
lock = threading.Lock()

# Forma manual
lock.acquire()
try:
    # seção crítica
    pass
finally:
    lock.release()

# Forma recomendada (context manager)
with lock:
    # seção crítica
    pass  # lock é liberado automaticamente
```

### Seção Crítica

Trecho de código que acessa recursos compartilhados e deve ser executado atomicamente (sem interrupção):

```python
# ERRADO - não é atômico
current = self.balance
self.balance = current + amount

# CORRETO - protegido por lock
with self.lock:
    current = self.balance
    self.balance = current + amount
```

### Atomicidade

Uma operação é atômica quando é executada completamente ou não é executada - não pode ser interrompida no meio:

- `x = 5` é atômico em Python
- `x = x + 1` NÃO é atômico (read-modify-write)
- Operações protegidas por lock são atômicas

## Desafios Adicionais (Opcional)

1. **Múltiplas operações:**
   - Modifique o código para fazer depósitos E saques concorrentes
   - Verifique se a solução ainda funciona

2. **Deadlock:**
   - Crie um cenário com dois locks
   - Tente provocar um deadlock (threads travadas esperando uma pela outra)
   - Como evitar deadlocks?

3. **Performance:**
   - Meça o tempo de execução com e sem locks
   - Qual é o custo da sincronização?
   - Quando vale a pena usar locks?

4. **Alternativas:**
   - Pesquise sobre `threading.RLock` (reentrant lock)
   - Explore `queue.Queue` para comunicação thread-safe
   - Investigue `threading.Semaphore` para controle de acesso

## Recursos Adicionais

- [Python Threading Documentation](https://docs.python.org/3/library/threading.html)
- [Real Python: Threading in Python](https://realpython.com/intro-to-python-threading/)
- [Race Conditions and Deadlocks](https://en.wikipedia.org/wiki/Race_condition)

## Próximos Passos

Após completar este experimento:
1. Revise os conceitos de concorrência da apresentação
2. Pratique identificando race conditions em código real
3. Prossiga para o Experimento 4 - Análise de Incidente

---

**Dica:** Race conditions são bugs intermitentes - podem não aparecer sempre. Execute o código múltiplas vezes e com diferentes números de threads para aumentar a probabilidade de observar o problema.
