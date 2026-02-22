"""
Experimento 3 - Concorrência: Race Condition

Este módulo demonstra uma race condition clássica em operações bancárias.
O código NÃO é thread-safe e produzirá resultados inconsistentes quando
executado com múltiplas threads.

OBJETIVO: Identificar o problema de concorrência e entender por que ocorre.
"""

import threading
import time


class BankAccount:
    """
    Conta bancária SEM proteção contra race conditions.
    
    ATENÇÃO: Esta implementação é BUGGY e serve apenas para demonstração.
    Não use este código em produção!
    """
    
    def __init__(self, initial_balance: int):
        self.balance = initial_balance
    
    def deposit(self, amount: int):
        """
        Deposita um valor na conta.
        
        PROBLEMA: Operação read-modify-write sem sincronização.
        O sleep amplifica a janela de tempo para race condition.
        """
        current = self.balance
        time.sleep(0.001)  # Simula processamento - amplifica race condition
        self.balance = current + amount
    
    def withdraw(self, amount: int):
        """
        Saca um valor da conta.
        
        PROBLEMA: Mesma race condition do deposit.
        """
        current = self.balance
        time.sleep(0.001)  # Simula processamento - amplifica race condition
        self.balance = current - amount
    
    def get_balance(self) -> int:
        """Retorna o saldo atual."""
        return self.balance


def run_concurrent_transactions(account: BankAccount, num_threads: int, amount: int = 10):
    """
    Executa transações concorrentes na conta.
    
    Args:
        account: Conta bancária para realizar transações
        num_threads: Número de threads a criar
        amount: Valor a depositar em cada thread
    
    Esta função cria múltiplas threads que depositam simultaneamente,
    demonstrando a race condition.
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
    Demonstração da race condition.
    Execute este script múltiplas vezes e observe resultados diferentes!
    """
    print("=== Demonstração de Race Condition ===\n")
    
    num_threads = 20
    deposit_amount = 10
    expected_balance = num_threads * deposit_amount
    
    print(f"Configuração:")
    print(f"  - Número de threads: {num_threads}")
    print(f"  - Valor por depósito: {deposit_amount}")
    print(f"  - Saldo esperado: {expected_balance}\n")
    
    # Executar múltiplas vezes para demonstrar inconsistência
    results = []
    num_runs = 5
    
    print(f"Executando {num_runs} vezes...\n")
    
    for run in range(1, num_runs + 1):
        account = BankAccount(0)
        run_concurrent_transactions(account, num_threads, deposit_amount)
        final_balance = account.get_balance()
        results.append(final_balance)
        
        status = "✓ CORRETO" if final_balance == expected_balance else "✗ INCORRETO"
        print(f"Execução {run}: Saldo final = {final_balance} {status}")
    
    print(f"\nResultados únicos: {set(results)}")
    print(f"Número de resultados diferentes: {len(set(results))}")
    
    if len(set(results)) > 1:
        print("\n⚠️  RACE CONDITION DETECTADA!")
        print("O mesmo código produziu resultados diferentes em execuções diferentes.")
        print("Isso indica um problema de concorrência que precisa ser corrigido.")
    else:
        print("\n⚠️  Race condition pode não ter sido demonstrada nesta execução.")
        print("Execute novamente ou aumente o número de threads.")
