"""
Tests for fixed_code.py - Sistema de Biblioteca
Experimento 1: Debugging Multi-Tipo

Estes testes verificam que a solução corrigida funciona corretamente.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Adicionar o diretório solution ao path
solution_path = Path(__file__).parent / "solution"
sys.path.insert(0, str(solution_path))

from fixed_code import Book, Library


class TestBook:
    """Testes para a classe Book"""
    
    def test_book_creation(self):
        """Testa criação de livro"""
        book = Book("123", "Test Book", "Test Author", 5)
        assert book.isbn == "123"
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.total_copies == 5
        assert book.available_copies == 5
    
    def test_is_available_with_copies(self):
        """Testa que livro com cópias está disponível (ERRO 1)"""
        book = Book("123", "Test", "Author", 3)
        assert book.is_available() is True
    
    def test_is_available_without_copies(self):
        """Testa que livro sem cópias não está disponível (ERRO 1)"""
        book = Book("123", "Test", "Author", 0)
        assert book.is_available() is False
    
    def test_borrow_decreases_copies(self):
        """Testa que emprestar diminui cópias disponíveis"""
        book = Book("123", "Test", "Author", 3)
        book.borrow("user1")
        assert book.available_copies == 2
    
    def test_return_increases_copies(self):
        """Testa que devolver aumenta cópias disponíveis (ERRO 2)"""
        book = Book("123", "Test", "Author", 3)
        book.borrow("user1")
        assert book.available_copies == 2
        book.return_book("user1")
        assert book.available_copies == 3
    
    def test_cannot_borrow_when_unavailable(self):
        """Testa que não pode emprestar quando não há cópias"""
        book = Book("123", "Test", "Author", 1)
        book.borrow("user1")
        result = book.borrow("user2")
        assert result is False


class TestLibrary:
    """Testes para a classe Library"""
    
    def test_library_creation(self):
        """Testa criação de biblioteca"""
        lib = Library("Test Library")
        assert lib.name == "Test Library"
        assert len(lib.books) == 0
        assert len(lib.users) == 0
    
    def test_add_new_book(self):
        """Testa adicionar novo livro (ERRO 3)"""
        lib = Library("Test")
        lib.add_book("123", "Test Book", "Author", 3)
        assert "123" in lib.books
        assert lib.books["123"].total_copies == 3
    
    def test_add_existing_book_increases_copies(self):
        """Testa que adicionar livro existente aumenta cópias (ERRO 3)"""
        lib = Library("Test")
        lib.add_book("123", "Test Book", "Author", 3)
        lib.add_book("123", "Test Book", "Author", 2)
        assert lib.books["123"].total_copies == 5
        assert lib.books["123"].available_copies == 5
    
    def test_register_user(self):
        """Testa registro de usuário"""
        lib = Library("Test")
        lib.register_user("user1")
        assert "user1" in lib.users
    
    def test_borrow_book_unregistered_user(self):
        """Testa que usuário não registrado não pode emprestar (ERRO 4)"""
        lib = Library("Test")
        lib.add_book("123", "Test", "Author", 1)
        result = lib.borrow_book("user1", "123")
        assert result["success"] is False
        assert "not registered" in result["error"].lower()
    
    def test_borrow_book_success(self):
        """Testa empréstimo bem-sucedido"""
        lib = Library("Test")
        lib.add_book("123", "Test", "Author", 1)
        lib.register_user("user1")
        result = lib.borrow_book("user1", "123")
        assert result["success"] is True
        assert "due_date" in result
    
    def test_borrow_nonexistent_book(self):
        """Testa emprestar livro inexistente"""
        lib = Library("Test")
        lib.register_user("user1")
        result = lib.borrow_book("user1", "999")
        assert result["success"] is False
        assert "not found" in result["error"].lower()
    
    def test_calculate_fine_no_delay(self):
        """Testa que não há multa se não está atrasado (ERRO 5)"""
        lib = Library("Test")
        lib.add_book("123", "Test", "Author", 1)
        lib.register_user("user1")
        lib.borrow_book("user1", "123")
        fine = lib.calculate_fine("user1", "123")
        assert fine == 0.0
    
    def test_calculate_fine_with_delay(self):
        """Testa cálculo de multa com atraso (ERRO 5)"""
        lib = Library("Test")
        lib.add_book("123", "Test", "Author", 1)
        lib.register_user("user1")
        
        # Emprestar e simular atraso
        book = lib.books["123"]
        book.borrow("user1")
        # Simular data de vencimento no passado
        book.borrowed_by["user1"] = datetime.now() - timedelta(days=5)
        
        fine = lib.calculate_fine("user1", "123")
        assert fine == 10.0  # 5 dias * R$ 2.00
    
    def test_get_available_books(self):
        """Testa listagem de livros disponíveis"""
        lib = Library("Test")
        lib.add_book("123", "Available Book", "Author", 2)
        lib.add_book("456", "Unavailable Book", "Author", 1)
        lib.register_user("user1")
        lib.borrow_book("user1", "456")
        
        available = lib.get_available_books()
        assert len(available) == 1
        assert available[0]["isbn"] == "123"
    
    def test_get_overdue_books(self):
        """Testa listagem de livros atrasados (ERRO 6)"""
        lib = Library("Test")
        lib.add_book("123", "Test", "Author", 2)
        lib.register_user("user1")
        
        # Emprestar e simular atraso
        book = lib.books["123"]
        book.borrow("user1")
        book.borrowed_by["user1"] = datetime.now() - timedelta(days=3)
        
        overdue = lib.get_overdue_books()
        assert len(overdue) == 1
        assert overdue[0]["days_late"] == 3
        assert overdue[0]["fine"] == 6.0  # 3 dias * R$ 2.00
    
    def test_search_books_case_insensitive(self):
        """Testa busca case-insensitive (ERRO 7)"""
        lib = Library("Test")
        lib.add_book("123", "Effective Java", "Joshua Bloch", 1)
        lib.add_book("456", "Clean Code", "Robert Martin", 1)
        
        # Busca com diferentes cases
        results_lower = lib.search_books("java")
        results_upper = lib.search_books("JAVA")
        results_mixed = lib.search_books("JaVa")
        
        assert len(results_lower) == 1
        assert len(results_upper) == 1
        assert len(results_mixed) == 1
        assert results_lower[0]["isbn"] == "123"
    
    def test_search_books_by_author(self):
        """Testa busca por autor"""
        lib = Library("Test")
        lib.add_book("123", "Book 1", "Martin Fowler", 1)
        lib.add_book("456", "Book 2", "Robert Martin", 1)
        
        results = lib.search_books("martin")
        assert len(results) == 2
    
    def test_search_books_no_results(self):
        """Testa busca sem resultados"""
        lib = Library("Test")
        lib.add_book("123", "Test", "Author", 1)
        
        results = lib.search_books("nonexistent")
        assert len(results) == 0


class TestIntegration:
    """Testes de integração do sistema completo"""
    
    def test_complete_borrow_return_cycle(self):
        """Testa ciclo completo de empréstimo e devolução"""
        lib = Library("Test")
        lib.add_book("123", "Test Book", "Author", 2)
        lib.register_user("user1")
        
        # Estado inicial
        assert lib.books["123"].available_copies == 2
        
        # Emprestar
        result = lib.borrow_book("user1", "123")
        assert result["success"] is True
        assert lib.books["123"].available_copies == 1
        
        # Devolver
        lib.books["123"].return_book("user1")
        assert lib.books["123"].available_copies == 2
    
    def test_multiple_users_same_book(self):
        """Testa múltiplos usuários emprestando o mesmo livro"""
        lib = Library("Test")
        lib.add_book("123", "Popular Book", "Author", 3)
        lib.register_user("user1")
        lib.register_user("user2")
        lib.register_user("user3")
        
        # Três usuários emprestam
        lib.borrow_book("user1", "123")
        lib.borrow_book("user2", "123")
        lib.borrow_book("user3", "123")
        
        assert lib.books["123"].available_copies == 0
        assert not lib.books["123"].is_available()
