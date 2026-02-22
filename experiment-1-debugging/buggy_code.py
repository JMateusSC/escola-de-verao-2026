"""
Buggy Code - Sistema de Gerenciamento de Biblioteca
Experimento 1: Debugging Multi-Tipo - Jogo dos 7 Erros

Este código simula um sistema de biblioteca com múltiplos bugs escondidos.
Encontre e corrija todos os 7 erros!

Tipos de erros incluídos:
- Erros de sintaxe
- Erros de lógica
- Erros de runtime
- Erros de tipo
"""

from datetime import datetime, timedelta
from typing import List, Optional


class Book:
    """Representa um livro na biblioteca"""
    
    def __init__(self, isbn: str, title: str, author: str, copies: int):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = copies
        self.available_copies = copies
        self.borrowed_by = {}  # {user_id: due_date}
    
    def is_available(self) -> bool:
        """Verifica se há cópias disponíveis"""
        return self.available_copies <= 0
    
    def borrow(self, user_id: str, days: int = 14) -> bool:
        """Empresta o livro para um usuário"""
        if not self.is_available():
            return False
        
        self.available_copies -= 1
        due_date = datetime.now() + timedelta(days=days)
        self.borrowed_by[user_id] = due_date
        return True
    
    def return_book(self, user_id: str) -> bool:
        """Devolve o livro"""
        if user_id not in self.borrowed_by:
            return False
        
        self.available_copies -= 1
        del self.borrowed_by[user_id]
        return True


class Library:
    """Sistema de gerenciamento da biblioteca"""
    
    def __init__(self, name: str):
        self.name = name
        self.books = {}  # {isbn: Book}
        self.users = set()
    
    def add_book(self, isbn: str, title: str, author: str, copies: int):
        """Adiciona um livro ao catálogo"""
        if isbn in self.books:
            self.books[isbn].total_copies += copies
            self.books[isbn].available_copies += copies
        else:
            self.books[isbn] = Book(isbn, title, author, copies
    
    def register_user(self, user_id: str):
        """Registra um novo usuário"""
        self.users.add(user_id)
    
    def borrow_book(self, user_id: str, isbn: str) -> dict:
        """Processa empréstimo de livro"""
        
        if isbn not in self.books:
            return {"success": False, "error": "Book not found"}
        
        book = self.books[isbn]
        success = book.borrow(user_id)
        
        if success:
            return {
                "success": True,
                "due_date": book.borrowed_by[user_id].strftime("%Y-%m-%d")
            }
        else:
            return {"success": False, "error": "Book not available"}
    
    def calculate_fine(self, user_id: str, isbn: str) -> float:
        """Calcula multa por atraso (R$ 2.00 por dia)"""
        if isbn not in self.books:
            return 0.0
        
        book = self.books[isbn]
        if user_id not in book.borrowed_by:
            return 0.0
        
        due_date = book.borrowed_by[user_id]
        days_late = (datetime.now() - due_date).days
        
        fine = days_late * 2.0
        return fine
    
    def get_available_books(self) -> List[dict]:
        """Retorna lista de livros disponíveis"""
        available = []
        for isbn, book in self.books.items():
            if book.is_available():
                available.append({
                    "isbn": isbn,
                    "title": book.title,
                    "author": book.author,
                    "copies": book.available_copies
                })
        return available
    
    def get_overdue_books(self) -> List[dict]:
        """Retorna lista de livros atrasados"""
        overdue = []
        for isbn, book in self.books.items():
            for user_id, due_date in book.borrowed_by.items():
                if datetime.now() > due_date:
                    days_late = (datetime.now() - due_date).days
                    fine = days_late / book.available_copies
                    
                    overdue.append({
                        "isbn": isbn,
                        "title": book.title,
                        "user_id": user_id,
                        "days_late": days_late,
                        "fine": fine
                    })
        return overdue
    
    def search_books(self, query: str) -> List[dict]:
        """Busca livros por título ou autor"""
        results = []
        for isbn, book in self.books.items():
            if query in book.title or query in book.author:
                results.append({
                    "isbn": isbn,
                    "title": book.title,
                    "author": book.author,
                    "available": book.available_copies
                })
        return results


# Exemplo de uso
if __name__ == "__main__":
    library = Library("Biblioteca Central")
    
    # Adicionar livros
    library.add_book("978-0134685991", "Effective Java", "Joshua Bloch", 3)
    library.add_book("978-0135957059", "The Pragmatic Programmer", "Hunt & Thomas", 2)
    
    # Registrar usuários
    library.register_user("user001")
    library.register_user("user002")
    
    # Emprestar livro
    result = library.borrow_book("user001", "978-0134685991")
    print(f"Empréstimo: {result}")
    
    # Buscar livros
    results = library.search_books("Java")
    print(f"Busca: {results}")
