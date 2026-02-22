# Guia de Solução - Experimento 3: Concorrência

Este documento explica em detalhes o problema de race condition e como resolvê-lo usando locks.

---

## Análise do Problema

### O Código Buggy

```python
class BankAccount:
    def __init__(self, initial_balance: int):
        self.balance = initial_balance
    
    def deposit(self, amount: int):
        current = self.balance          # Linha 1: Leitura
        time.sleep(0.001)               # Linha 2: Processamento
        self.balance = current + amount # Linha 3: Escrita
```

### Por que há Race Condition?

A operação de depósito envolve três passos:
1. **Ler** o saldo atual
2. **Calcular** o novo saldo
3. **Escrever** o novo saldo

Quando múltiplas threads executam isso simultaneamente, pode ocorrer o seguinte:

```
Estado inicial: balance = 100

Thread A                          Thread B
-----------                       -----------
current = balance  (100)          
                                  current = balance  (100)
time.sleep(0.001)                 
                                  time.sleep(0.001)
balance = 100 + 10  (110)         
                                  balance = 100 + 20  (120)

Resultado final: 120
Resultado esperado: 130
```

**Problema:** Thread B leu o saldo ANTES de Thread A escrever o novo valor. O depósito de Thread A foi perdido!

### Características de uma Race Condition

1. **Não-determinística:** Resultados diferentes em execuções diferentes
2. **Dependente de timing:** Ocorre quando threads intercalam de forma específica
3. **Difícil de reproduzir:** Pode não aparecer sempre
4. **Difícil de debugar:** Breakpoints alteram o timing e podem "esconder" o bug

---

## A Solução: Threading.Lock

### Conceito de Lock (Mutex)

Um **lock** (ou mutex - mutual exclusion) é um mecanismo de sincronização que garante:
- Apenas uma thread pode "adquirir" o lock por vez
- Outras threads que tentam adquirir o lock ficam bloqueadas (esperando)
- Quando o lock é liberado, uma das threads esperando pode adquiri-lo

### Implementação Correta

```python
import threading

class ThreadSafeBankAccount:
    def __init__(self, initial_balance: int):
        self.balance = initial_balance
        self.lock = threading.Lock()  # Criar o lock
    
    def deposit(self, amount: int):
        with self.lock:  # Adquire o lock
            current = self.balance
            time.sleep(0.001)
            self.balance = current + amount
        # Lock é liberado automaticamente ao sair do bloco with
    
    def withdraw(self, amount: int):
        with self.lock:
            current = self.balance
            time.sleep(0.001)
            self.balance = current - amount
    
    def get_balance(self) -> int:
        with self.lock:
            return self.balance
```

### Como o Lock Resolve o Problema

```
Estado inicial: balance = 100

Thread A                          Thread B
-----------                       -----------
with lock:  (adquire lock)        
  current = balance  (100)        with lock:  (BLOQUEADA - esperando lock)
  time.sleep(0.001)               
  balance = 110                   
(libera lock)                     
                                  (adquire lock)
                                    current = balance  (110)
                                    time.sleep(0.001)
                                    balance = 130
                                  (libera lock)

Resultado final: 130 ✓
```

**Solução:** Thread B só consegue ler o saldo DEPOIS que Thread A terminou completamente sua operação.

---

## Detalhes da Implementação

### 1. Criando o Lock

```python
def __init__(self, initial_balance: int):
    self.balance = initial_balance
    self.lock = threading.Lock()  # Um lock por instância
```

**Importante:**
- Criar o lock no `__init__` garante que há um único lock por conta
- Todas as threads que acessam a mesma conta usam o mesmo lock
- Contas diferentes têm locks diferentes (não interferem entre si)

### 2. Usando o Context Manager

```python
with self.lock:
    # Seção crítica
    current = self.balance
    self.balance = current + amount
```

**Equivalente a:**
```python
self.lock.acquire()
try:
    current = self.balance
    self.balance = current + amount
finally:
    self.lock.release()  # Sempre libera, mesmo com exceção
```

**Por que usar `with`?**
- Mais limpo e legível
- Garante que o lock será liberado mesmo se houver exceção
- Previne deadlocks causados por locks não liberados

### 3. Protegendo Todas as Operações

```python
def deposit(self, amount: int):
    with self.lock:  # Protegido
        # ...

def withdraw(self, amount: int):
    with self.lock:  # Protegido
        # ...

def get_balance(self) -> int:
    with self.lock:  # Protegido
        return self.balance
```

**Regra:** TODOS os métodos que acessam `self.balance` devem usar o lock.

---

## Conceitos Importantes

### Seção Crítica

**Definição:** Trecho de código que acessa recursos compartilhados e deve ser executado atomicamente.

```python
# Seção crítica
with self.lock:
    current = self.balance      # Leitura
    time.sleep(0.001)           # Processamento
    self.balance = current + amount  # Escrita
```

**Características:**
- Deve ser a menor possível (para melhor performance)
- Deve incluir TODA a operação read-modify-write
- Não deve incluir operações desnecessárias (I/O, cálculos complexos)

### Atomicidade

**Definição:** Uma operação é atômica quando é executada completamente ou não é executada - não pode ser interrompida no meio.

**Exemplos em Python:**

```python
# Atômico (operação simples)
x = 5
y = x

# NÃO atômico (read-modify-write)
x = x + 1
x += 1
self.balance = self.balance + amount

# Tornado atômico com lock
with self.lock:
    x = x + 1  # Agora é atômico
```

### Exclusão Mútua

**Definição:** Garantia de que apenas uma thread executa a seção crítica por vez.

```python
# Thread A                    # Thread B
with self.lock:               # Tenta adquirir lock
    # Executa                 # BLOQUEADA (esperando)
    # ...                     # ...
# Libera lock                 # Adquire lock
                              with self.lock:
                                  # Executa
```

---

## Validação da Solução

### Teste Manual

```bash
# Execute múltiplas vezes
for i in {1..10}; do python solution/fixed_concurrent.py; done
```

**Resultado esperado:**
- Todas as execuções produzem o mesmo resultado
- Resultado é sempre correto (num_threads × deposit_amount)

### Testes Automatizados

```python
def test_thread_safe_consistency():
    """Testa que a solução é thread-safe"""
    results = []
    for _ in range(10):
        account = ThreadSafeBankAccount(0)
        run_concurrent_transactions_safe(account, num_threads=20, amount=10)
        results.append(account.get_balance())
    
    expected = 20 * 10  # 200
    assert all(r == expected for r in results), "Thread safety violated"
```

### Property-Based Testing

```python
@given(
    num_threads=st.integers(min_value=5, max_value=50),
    amount=st.integers(min_value=1, max_value=100)
)
def test_property_thread_safe_consistency(num_threads, amount):
    """Testa com parâmetros aleatórios"""
    account = ThreadSafeBankAccount(0)
    run_concurrent_transactions_safe(account, num_threads, amount)
    
    expected = num_threads * amount
    assert account.get_balance() == expected
```

---

## Comparação: Antes e Depois

### Código Buggy (Race Condition)

```python
class BankAccount:
    def __init__(self, initial_balance: int):
        self.balance = initial_balance
    
    def deposit(self, amount: int):
        current = self.balance
        time.sleep(0.001)
        self.balance = current + amount
```

**Problemas:**
- ❌ Não é thread-safe
- ❌ Resultados inconsistentes
- ❌ Operações podem ser perdidas
- ❌ Comportamento não-determinístico

### Código Correto (Thread-Safe)

```python
class ThreadSafeBankAccount:
    def __init__(self, initial_balance: int):
        self.balance = initial_balance
        self.lock = threading.Lock()
    
    def deposit(self, amount: int):
        with self.lock:
            current = self.balance
            time.sleep(0.001)
            self.balance = current + amount
```

**Benefícios:**
- ✅ Thread-safe
- ✅ Resultados consistentes
- ✅ Todas as operações são processadas
- ✅ Comportamento determinístico

---

## Considerações de Performance

### Custo da Sincronização

Locks têm um custo:
- Overhead de adquirir/liberar o lock
- Threads bloqueadas não fazem trabalho útil
- Serialização reduz paralelismo

### Quando Usar Locks

**Use locks quando:**
- Múltiplas threads acessam dados compartilhados
- Pelo menos uma thread modifica os dados
- Corretude é mais importante que performance

**Evite locks quando:**
- Dados são read-only (imutáveis)
- Cada thread tem seus próprios dados
- Pode usar estruturas thread-safe (Queue, etc.)

### Otimizações

```python
# Minimizar seção crítica
def deposit(self, amount: int):
    # Cálculos fora do lock
    new_value = self.calculate_fees(amount)
    
    # Apenas a escrita dentro do lock
    with self.lock:
        self.balance += new_value
```

---

## Problemas Comuns e Soluções

### Problema 1: Deadlock

**Cenário:**
```python
# Thread A                    # Thread B
with lock1:                   with lock2:
    with lock2:  # BLOQUEADA      with lock1:  # BLOQUEADA
        pass                          pass
```

**Solução:** Sempre adquirir locks na mesma ordem.

### Problema 2: Lock Muito Amplo

```python
# RUIM - lock desnecessariamente amplo
with self.lock:
    result = expensive_calculation()  # Não precisa de lock
    self.balance += result
```

**Solução:** Minimizar seção crítica.

```python
# BOM - lock apenas onde necessário
result = expensive_calculation()
with self.lock:
    self.balance += result
```

### Problema 3: Esquecer de Proteger Algum Método

```python
def deposit(self, amount: int):
    with self.lock:  # Protegido
        self.balance += amount

def get_balance(self) -> int:
    return self.balance  # NÃO protegido - pode ler valor inconsistente!
```

**Solução:** Proteger TODAS as operações.

---

## Conceitos Avançados

### GIL (Global Interpreter Lock)

Python tem um GIL que permite apenas uma thread executar bytecode por vez. Mas race conditions ainda ocorrem porque:

1. O GIL pode ser liberado entre bytecodes
2. Operações compostas (read-modify-write) não são atômicas
3. O GIL é liberado durante I/O

### Alternativas a Locks

1. **Queue:** Comunicação thread-safe
```python
from queue import Queue
q = Queue()
q.put(item)  # Thread-safe
```

2. **RLock:** Lock reentrante
```python
lock = threading.RLock()
# Pode ser adquirido múltiplas vezes pela mesma thread
```

3. **Semaphore:** Controla número de acessos
```python
sem = threading.Semaphore(3)  # Até 3 threads simultâneas
```

4. **Condition:** Sincronização complexa
```python
cv = threading.Condition()
# Permite wait/notify entre threads
```

---

## Resumo

### O Problema
- Race conditions ocorrem quando múltiplas threads acessam dados compartilhados sem sincronização
- Resultam em comportamento não-determinístico e bugs difíceis de reproduzir

### A Solução
- Use `threading.Lock` para proteger seções críticas
- Use context manager `with lock:` para garantir liberação
- Proteja TODAS as operações que acessam dados compartilhados

### Boas Práticas
- ✅ Um lock por recurso compartilhado
- ✅ Minimizar seções críticas
- ✅ Sempre usar context manager
- ✅ Documentar requisitos de thread safety
- ✅ Testar com múltiplas threads e execuções

### Lembre-se
> "Concorrência é difícil. Sincronização é essencial. Testes são fundamentais."

---

## Próximos Passos

1. Experimente modificar o código e observar o comportamento
2. Tente criar cenários mais complexos (múltiplas contas, transferências)
3. Explore outras primitivas de sincronização (RLock, Semaphore, Condition)
4. Estude sobre deadlocks e como evitá-los
5. Prossiga para o Experimento 4 - Análise de Incidente
