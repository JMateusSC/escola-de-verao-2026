# Dicas - Experimento 3: Concorrência

Este arquivo contém dicas progressivas para ajudá-lo a resolver o problema de race condition. Tente resolver por conta própria antes de ler as dicas!

---

## Dica 1: Identificando o Problema

<details>
<summary>Clique para ver a dica</summary>

O problema está nos métodos `deposit()` e `withdraw()` da classe `BankAccount`.

Observe estas três linhas:
```python
current = self.balance      # Lê o valor
time.sleep(0.001)           # Simula processamento
self.balance = current + amount  # Escreve o novo valor
```

Quando múltiplas threads executam isso simultaneamente, elas podem ler o mesmo valor inicial antes de qualquer uma escrever o novo valor.

**Pergunta:** O que acontece se duas threads lerem `balance = 100` ao mesmo tempo, cada uma adicionar 10, e depois ambas escreverem 110?

</details>

---

## Dica 2: O que é uma Seção Crítica?

<details>
<summary>Clique para ver a dica</summary>

Uma **seção crítica** é um trecho de código que acessa recursos compartilhados (como `self.balance`) e precisa ser executado atomicamente - sem interrupção de outras threads.

No nosso caso, a seção crítica é:
```python
current = self.balance
self.balance = current + amount
```

Essas duas linhas devem ser executadas como uma operação única, sem que outras threads acessem `self.balance` no meio.

**Solução:** Precisamos de um mecanismo para garantir que apenas uma thread execute a seção crítica por vez.

</details>

---

## Dica 3: Usando Locks

<details>
<summary>Clique para ver a dica</summary>

Python fornece `threading.Lock` para sincronização. Um lock funciona assim:

1. Apenas uma thread pode "adquirir" o lock por vez
2. Outras threads que tentam adquirir o lock ficam bloqueadas esperando
3. Quando a thread libera o lock, outra thread pode adquiri-lo

**Como usar:**

```python
import threading

class MinhaClasse:
    def __init__(self):
        self.lock = threading.Lock()  # Criar o lock
    
    def metodo_critico(self):
        with self.lock:  # Adquire o lock
            # Seção crítica aqui
            # Apenas uma thread executa por vez
            pass
        # Lock é liberado automaticamente
```

**Tarefa:** Adicione um lock à classe `BankAccount` e use-o nos métodos `deposit()` e `withdraw()`.

</details>

---

## Dica 4: Onde Colocar o Lock?

<details>
<summary>Clique para ver a dica</summary>

Você precisa:

1. **Criar o lock no `__init__`:**
```python
def __init__(self, initial_balance: int):
    self.balance = initial_balance
    self.lock = threading.Lock()  # Adicione esta linha
```

2. **Proteger o método `deposit()`:**
```python
def deposit(self, amount: int):
    with self.lock:  # Adicione esta linha
        current = self.balance
        time.sleep(0.001)
        self.balance = current + amount
```

3. **Proteger o método `withdraw()` da mesma forma**

**Importante:** O lock deve envolver TODA a seção crítica, incluindo a leitura e a escrita.

</details>

---

## Dica 5: Por que usar `with lock:`?

<details>
<summary>Clique para ver a dica</summary>

O `with` é um context manager que garante que o lock será liberado mesmo se ocorrer uma exceção:

```python
# Forma manual (não recomendada)
self.lock.acquire()
try:
    # seção crítica
    self.balance = current + amount
finally:
    self.lock.release()  # Sempre libera, mesmo com exceção

# Forma recomendada (equivalente)
with self.lock:
    # seção crítica
    self.balance = current + amount
# Lock liberado automaticamente
```

Use sempre `with lock:` - é mais seguro e mais limpo!

</details>

---

## Dica 6: Testando sua Solução

<details>
<summary>Clique para ver a dica</summary>

Para verificar se sua solução funciona:

1. **Execute múltiplas vezes:**
```bash
for i in {1..10}; do python race_condition.py; done
```

2. **Aumente o número de threads:**
```python
num_threads = 50  # Mais threads = mais chance de race condition
```

3. **Verifique consistência:**
   - Todas as execuções devem produzir o mesmo resultado
   - O resultado deve ser exatamente `num_threads * deposit_amount`

4. **Execute os testes automatizados:**
```bash
pytest code/experiment-3-concurrency/ -v
```

Se ainda houver inconsistências, verifique se:
- O lock está sendo criado no `__init__`
- O `with self.lock:` envolve TODA a seção crítica
- Você está usando o mesmo lock em todos os métodos

</details>

---

## Dica 7: Erros Comuns

<details>
<summary>Clique para ver a dica</summary>

### Erro 1: Lock fora da seção crítica
```python
# ERRADO
with self.lock:
    current = self.balance
# Lock liberado aqui - race condition ainda existe!
self.balance = current + amount
```

### Erro 2: Criar um novo lock a cada chamada
```python
# ERRADO
def deposit(self, amount: int):
    lock = threading.Lock()  # Novo lock - não protege nada!
    with lock:
        self.balance += amount
```

### Erro 3: Esquecer de usar o lock em algum método
```python
# ERRADO
def deposit(self, amount: int):
    with self.lock:  # Protegido
        self.balance += amount

def withdraw(self, amount: int):
    self.balance -= amount  # NÃO protegido - race condition!
```

### Solução Correta:
- Um único lock criado no `__init__`
- Usado em TODOS os métodos que acessam `self.balance`
- Envolve TODA a seção crítica (leitura + modificação + escrita)

</details>

---

## Dica 8: Entendendo o `time.sleep()`

<details>
<summary>Clique para ver a dica</summary>

O `time.sleep(0.001)` no código buggy serve para **amplificar** a race condition:

```python
current = self.balance      # Thread 1 lê: 100
time.sleep(0.001)           # Thread 1 dorme
                            # Thread 2 lê: 100 (ainda não mudou!)
                            # Thread 2 dorme
                            # Thread 1 acorda
self.balance = current + 10 # Thread 1 escreve: 110
                            # Thread 2 acorda
self.balance = current + 10 # Thread 2 escreve: 110 (perdeu o +10 da Thread 1!)
```

Sem o sleep, a race condition ainda existe, mas é mais difícil de observar porque as operações são muito rápidas.

**Na solução com lock:** O sleep não causa problema porque apenas uma thread executa por vez.

</details>

---

## Dica 9: Conceitos Avançados (Opcional)

<details>
<summary>Clique para ver a dica</summary>

### GIL (Global Interpreter Lock)

Python tem um GIL que permite apenas uma thread executar bytecode por vez. Então por que temos race conditions?

**Resposta:** O GIL é liberado durante operações de I/O e pode ser liberado entre bytecodes. A operação `self.balance = current + amount` não é atômica - envolve múltiplos bytecodes.

### Alternativas a Locks

1. **Queue:** Para comunicação thread-safe
```python
from queue import Queue
q = Queue()
q.put(item)  # Thread-safe
item = q.get()  # Thread-safe
```

2. **Atomic operations:** Algumas operações são atômicas em Python
```python
x = 5  # Atômico
x += 1  # NÃO atômico (read-modify-write)
```

3. **Threading.RLock:** Lock reentrante (pode ser adquirido múltiplas vezes pela mesma thread)

4. **Multiprocessing:** Evita GIL usando processos separados

</details>

---

## Ainda com Dúvidas?

Se você tentou todas as dicas e ainda está com dificuldades:

1. Consulte a solução completa em `solution/fixed_concurrent.py`
2. Leia a explicação detalhada em `solution/SOLUTION_GUIDE.md`
3. Execute os testes e veja como eles validam a solução
4. Experimente modificar o código e observe o comportamento

**Lembre-se:** Entender race conditions é fundamental para programação concorrente. Vale a pena investir tempo para compreender bem este conceito!
