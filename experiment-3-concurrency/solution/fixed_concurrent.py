"""
Experimento 3 - Concorrência: Solução Thread-Safe

Este módulo implementa uma versão thread-safe da conta bancária,
usando threading.Lock para sincronização adequada.

OBJETIVO: Demonstrar como corrigir race conditions usando locks.
"""

import threading
import time


class ThreadSafeBankAccount:
    """
    Conta bancária COM proteção contra race conditions.
    
    Esta implementação usa threading.Lock para garantir que operações
    críticas sejam executadas atomicamente, evitando race conditions.
    """
    
    def __init__(self, initial_balance: int):
        self.balance = initial_balance
        self.lock = threading.Lock()  # Lock para sincronização
    
    def deposit(self, amount: int):
        """
        Deposita um valor na conta de forma thread-safe.
        
        SOLUÇÃO: Usa context manager (with lock) para garantir
        que apenas uma thread execute a operação por vez.
        """
        with self.lock:  # Adquire o lock automaticamente
            current = self.balance
            time.sleep(0.001)  # Simula processamento
            self.balance = current + amount
        # Lock é liberado automaticamente ao sair do bloco with
    
    def withdraw(self, amount: int):
        """
        Saca um valor da conta de forma thread-safe.
        
        SOLUÇÃO: Mesma proteção com lock do deposit.
        """
        with self.lock:
            current = self.balance
            time.sleep(0.001)  # Simula processamento
            self.balance = current - amount
    
    def get_balance(self) -> int:
        """
        Retorna o saldo atual de forma thread-safe.
        
        Nota: Para leituras simples, o lock pode não ser necessário
        em Python devido ao GIL, mas é boa prática para consistência.
        """
        with self.lock:
            return self.balance


def run_concurrent_transactions_safe(account: ThreadSafeBankAccount, num_threads: int, amount: int = 10):
    """
    Executa transações concorrentes na conta thread-safe.
    
    Args:
        account: Conta bancária thread-safe para realizar transações
        num_threads: Número de threads a criar
        amount: Valor a depositar em cada thread
    
    Esta função cria múltiplas threads que depositam simultaneamente,
    mas agora com sincronização adequada.
    """
    threads = []
    
    # Criar e iniciar threads
    for _ in range(num_threads):
        t = threading.Thread(target=account.deposit, args=(amount,))
        threads.append(t)
        t.start()
    
    # Aguardar todas as threads terminarem
    for t in threads:
        t.join()


if __name__ == "__main__":
    """
    Demonstração da solução thread-safe.
    Execute este script múltiplas vezes - o resultado será sempre consistente!
    """
    print("=== Demonstração de Solução Thread-Safe ===\n")
    
    num_threads = 20
    deposit_amount = 10
    expected_balance = num_threads * deposit_amount
    
    print(f"Configuração:")
    print(f"  - Número de threads: {num_threads}")
    print(f"  - Valor por depósito: {deposit_amount}")
    print(f"  - Saldo esperado: {expected_balance}\n")
    
    # Executar múltiplas vezes para demonstrar consistência
    results = []
    num_runs = 5
    
    print(f"Executando {num_runs} vezes...\n")
    
    for run in range(1, num_runs + 1):
        account = ThreadSafeBankAccount(0)
        run_concurrent_transactions_safe(account, num_threads, deposit_amount)
        final_balance = account.get_balance()
        results.append(final_balance)
        
        status = "✓ CORRETO" if final_balance == expected_balance else "✗ INCORRETO"
        print(f"Execução {run}: Saldo final = {final_balance} {status}")
    
    print(f"\nResultados únicos: {set(results)}")
    print(f"Número de resultados diferentes: {len(set(results))}")
    
    if len(set(results)) == 1 and results[0] == expected_balance:
        print("\n✓ SUCESSO!")
        print("Todas as execuções produziram o resultado correto e consistente.")
        print("A sincronização com locks resolveu a race condition.")
    else:
        print("\n✗ Ainda há problemas - verifique a implementação.")
