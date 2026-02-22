"""
Tests for buggy_code.py - Sistema de Biblioteca
Experimento 1: Debugging Multi-Tipo

IMPORTANTE: Este arquivo testa o código BUGGY para demonstrar os erros.
Os testes devem FALHAR com o código buggy e PASSAR após as correções.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar o diretório ao path
sys.path.insert(0, str(Path(__file__).parent))


def test_error_3_syntax_error():
    """
    Este teste PASSA enquanto o bug existir (detecta o SyntaxError).
    Após corrigir, este teste deve FALHAR (não haverá SyntaxError).
    """
    with pytest.raises(SyntaxError):
        with open("experiment-1-debugging/buggy_code.py") as f:
            compile(f.read(), "buggy_code.py", "exec")


# Os testes abaixo só podem rodar após corrigir o erro de sintaxe
# Descomente após corrigir o Erro 3

"""
from buggy_code import Book, Library


def test_error_1_is_available_logic():
    '''
    Este teste FALHA com o código buggy (retorna False quando deveria ser True).
    '''
    book = Book("123", "Test", "Author", 3)
    # Bug: retorna False quando há cópias (deveria retornar True)
    assert book.is_available() is True


def test_error_2_return_book_operator():
    '''
    Este teste FALHA com o código buggy (cópias diminuem em vez de aumentar).
    '''
    book = Book("123", "Test", "Author", 3)
    book.borrow("user1")
    assert book.available_copies == 2
    book.return_book("user1")
    # Bug: available_copies diminui em vez de aumentar
    assert book.available_copies == 3


def test_error_4_missing_user_validation():
    '''
    Este teste FALHA com o código buggy (permite emprestar sem registro).
    '''
    lib = Library("Test")
    lib.add_book("123", "Test", "Author", 1)
    # Bug: permite emprestar sem registrar usuário
    result = lib.borrow_book("unregistered_user", "123")
    assert result["success"] is False
    assert "not registered" in result["error"].lower()


def test_error_5_calculate_fine_no_validation():
    '''
    Este teste FALHA com o código buggy (não verifica se está atrasado).
    '''
    lib = Library("Test")
    lib.add_book("123", "Test", "Author", 1)
    lib.register_user("user1")
    lib.borrow_book("user1", "123")
    
    # Livro não está atrasado, multa deveria ser 0
    fine = lib.calculate_fine("user1", "123")
    assert fine == 0.0


def test_error_6_division_by_zero():
    '''
    Este teste FALHA com o código buggy (divisão incorreta e potencial erro).
    '''
    lib = Library("Test")
    lib.add_book("123", "Test", "Author", 1)
    lib.register_user("user1")
    
    # Emprestar e simular atraso
    book = lib.books["123"]
    book.borrow("user1")
    book.borrowed_by["user1"] = datetime.now() - timedelta(days=3)
    
    # E lógica de cálculo está errada
    overdue = lib.get_overdue_books()
    assert len(overdue) == 1
    assert overdue[0]["fine"] == 6.0


def test_error_7_case_sensitive_search():
    '''
    Este teste FALHA com o código buggy (não encontra com case diferente).
    '''
    lib = Library("Test")
    lib.add_book("123", "Effective Java", "Joshua Bloch", 1)
    
    # Bug: busca é case-sensitive
    results_lower = lib.search_books("java")
    results_upper = lib.search_books("JAVA")
    results_mixed = lib.search_books("JaVa")
    
    assert len(results_lower) == 1
    assert len(results_upper) == 1
    assert len(results_mixed) == 1
"""
