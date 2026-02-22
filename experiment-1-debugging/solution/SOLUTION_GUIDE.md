# 📖 Guia de Solução Completo - Jogo dos 7 Erros

## Visão Geral

Este guia explica cada um dos 7 bugs presentes no sistema de biblioteca e como corrigi-los. Use este guia apenas após tentar resolver o experimento por conta própria.

---

## 🐛 Erro 1: Lógica Invertida em `is_available()`

### Localização
**Arquivo**: `buggy_code.py`  
**Classe**: `Book`  
**Método**: `is_available()`  
**Linha**: ~24

### Código Buggy

```python
def is_available(self) -> bool:
    """Verifica se há cópias disponíveis"""
    # ERRO 1: Lógica invertida
    return self.available_copies <= 0
```

### Problema

A lógica está invertida. A função retorna `True` quando `available_copies <= 0`, ou seja, quando **não há** cópias disponíveis. Isso é o oposto do comportamento esperado.

### Impacto

- Livros sem cópias aparecem como disponíveis
- Livros com cópias aparecem como indisponíveis
- Sistema permite emprestar livros que não existem
- Usuários não conseguem emprestar livros que deveriam estar disponíveis

### Correção

```python
def is_available(self) -> bool:
    """Verifica se há cópias disponíveis"""
    return self.available_copies > 0  # ✅ Corrigido
```

### Explicação

Um livro está disponível quando há **pelo menos uma** cópia disponível, ou seja, `available_copies > 0`.

### Teste que Detecta

```python
def test_is_available_with_copies():
    book = Book("123", "Test", "Author", 3)
    assert book.is_available() is True  # Falha com código buggy
```

---

## 🐛 Erro 2: Operador Errado em `return_book()`

### Localização
**Arquivo**: `buggy_code.py`  
**Classe**: `Book`  
**Método**: `return_book()`  
**Linha**: ~39

### Código Buggy

```python
def return_book(self, user_id: str) -> bool:
    """Devolve o livro"""
    if user_id not in self.borrowed_by:
        return False
    
    # ERRO 2: Incremento errado
    self.available_copies -= 1  # Deveria ser +=
    del self.borrowed_by[user_id]
    return True
```

### Problema

Usa `-=` (decremento) em vez de `+=` (incremento). Quando um livro é devolvido, o número de cópias disponíveis **diminui** em vez de aumentar.

### Impacto

- Devolver livros reduz cópias disponíveis
- Eventualmente `available_copies` fica negativo
- Sistema perde controle do inventário
- Livros "desaparecem" do sistema

### Correção

```python
def return_book(self, user_id: str) -> bool:
    """Devolve o livro"""
    if user_id not in self.borrowed_by:
        return False
    
    self.available_copies += 1  # ✅ Corrigido
    del self.borrowed_by[user_id]
    return True
```

### Explicação

Quando um livro é devolvido, ele volta ao estoque. Portanto, devemos **incrementar** (`+=`) o número de cópias disponíveis.

### Teste que Detecta

```python
def test_return_increases_copies():
    book = Book("123", "Test", "Author", 3)
    book.borrow("user1")
    assert book.available_copies == 2
    book.return_book("user1")
    assert book.available_copies == 3  # Falha com código buggy
```

---

## 🐛 Erro 3: Erro de Sintaxe em `add_book()`

### Localização
**Arquivo**: `buggy_code.py`  
**Classe**: `Library`  
**Método**: `add_book()`  
**Linha**: ~71

### Código Buggy

```python
def add_book(self, isbn: str, title: str, author: str, copies: int):
    """Adiciona um livro ao catálogo"""
    if isbn in self.books:
        # ERRO 3: Sintaxe - parêntese faltando
        self.books[isbn].total_copies += copies
        self.books[isbn].available_copies += copies
    else:
        self.books[isbn] = Book(isbn, title, author, copies  # Falta )
```

### Problema

Falta um parêntese de fechamento `)` na última linha. Python não consegue interpretar o código.

### Impacto

- **Código não executa**: `SyntaxError: '(' was never closed`
- Bloqueia toda a aplicação
- Deve ser corrigido primeiro antes de testar outros bugs

### Correção

```python
def add_book(self, isbn: str, title: str, author: str, copies: int):
    """Adiciona um livro ao catálogo"""
    if isbn in self.books:
        self.books[isbn].total_copies += copies
        self.books[isbn].available_copies += copies
    else:
        self.books[isbn] = Book(isbn, title, author, copies)  # ✅ Corrigido
```

### Explicação

Erros de sintaxe são os mais fáceis de identificar porque Python indica a linha exata e o tipo de erro. Sempre corrija erros de sintaxe primeiro.

### Como Identificar

Execute o código:
```bash
python experiment-1-debugging/buggy_code.py
```

Python mostra:
```
SyntaxError: '(' was never closed
```

---

## 🐛 Erro 4: Falta Validação em `borrow_book()`

### Localização
**Arquivo**: `buggy_code.py`  
**Classe**: `Library`  
**Método**: `borrow_book()`  
**Linha**: ~64

### Código Buggy

```python
def borrow_book(self, user_id: str, isbn: str) -> dict:
    """Processa empréstimo de livro"""
    # ERRO 4: Não valida se usuário existe
    
    if isbn not in self.books:
        return {"success": False, "error": "Book not found"}
    
    book = self.books[isbn]
    success = book.borrow(user_id)
    # ...
```

### Problema

A função não verifica se o usuário está registrado antes de permitir o empréstimo. Qualquer pessoa (mesmo não cadastrada) pode emprestar livros.

### Impacto

- Usuários não registrados podem emprestar livros
- Sistema perde controle de quem tem os livros
- Impossível cobrar multas ou contatar usuários
- Violação de regras de negócio

### Correção

```python
def borrow_book(self, user_id: str, isbn: str) -> dict:
    """Processa empréstimo de livro"""
    # ✅ Corrigido: Valida se usuário existe
    if user_id not in self.users:
        return {"success": False, "error": "User not registered"}
    
    if isbn not in self.books:
        return {"success": False, "error": "Book not found"}
    
    book = self.books[isbn]
    success = book.borrow(user_id)
    # ...
```

### Explicação

Validações de pré-condição devem vir **antes** da lógica principal. Sempre valide entradas antes de processar operações críticas.

### Teste que Detecta

```python
def test_borrow_book_unregistered_user():
    lib = Library("Test")
    lib.add_book("123", "Test", "Author", 1)
    result = lib.borrow_book("user1", "123")  # user1 não registrado
    assert result["success"] is False  # Falha com código buggy
    assert "not registered" in result["error"].lower()
```

---

## 🐛 Erro 5: Falta Validação em `calculate_fine()`

### Localização
**Arquivo**: `buggy_code.py`  
**Classe**: `Library`  
**Método**: `calculate_fine()`  
**Linha**: ~88

### Código Buggy

```python
def calculate_fine(self, user_id: str, isbn: str) -> float:
    """Calcula multa por atraso (R$ 2.00 por dia)"""
    # ... validações ...
    
    due_date = book.borrowed_by[user_id]
    days_late = (datetime.now() - due_date).days
    
    # ERRO 5: Não verifica se está atrasado
    fine = days_late * 2.0  # Pode ser negativo!
    return fine
```

### Problema

A função não verifica se o livro está realmente atrasado. Se `days_late` for negativo ou zero (livro não está atrasado), a multa será negativa ou zero, mas o cálculo é feito de qualquer forma.

### Impacto

- Multas negativas quando livro não está atrasado
- Lógica confusa e incorreta
- Pode causar problemas em relatórios financeiros

### Correção

```python
def calculate_fine(self, user_id: str, isbn: str) -> float:
    """Calcula multa por atraso (R$ 2.00 por dia)"""
    # ... validações ...
    
    due_date = book.borrowed_by[user_id]
    days_late = (datetime.now() - due_date).days
    
    # ✅ Corrigido: Verifica se está atrasado
    if days_late <= 0:
        return 0.0
    
    fine = days_late * 2.0
    return fine
```

### Explicação

Sempre valide casos especiais antes de fazer cálculos. Neste caso, se o livro não está atrasado (`days_late <= 0`), a multa deve ser zero.

### Teste que Detecta

```python
def test_calculate_fine_no_delay():
    lib = Library("Test")
    lib.add_book("123", "Test", "Author", 1)
    lib.register_user("user1")
    lib.borrow_book("user1", "123")
    fine = lib.calculate_fine("user1", "123")
    assert fine == 0.0  # Falha se retornar valor negativo
```

---

## 🐛 Erro 6: Divisão por Zero em `get_overdue_books()`

### Localização
**Arquivo**: `buggy_code.py`  
**Classe**: `Library`  
**Método**: `get_overdue_books()`  
**Linha**: ~110

### Código Buggy

```python
def get_overdue_books(self) -> List[dict]:
    """Retorna lista de livros atrasados"""
    overdue = []
    for isbn, book in self.books.items():
        for user_id, due_date in book.borrowed_by.items():
            if datetime.now() > due_date:
                # ERRO 6: Division by zero potencial
                days_late = (datetime.now() - due_date).days
                fine = days_late / book.available_copies  # ❌ Divisão errada!
                # ...
```

### Problema

Dois problemas:
1. **Divisão por zero**: Se `available_copies = 0` (todos os livros emprestados), causa `ZeroDivisionError`
2. **Lógica errada**: Multa não deveria depender de cópias disponíveis, mas sim de dias de atraso

### Impacto

- Crash da aplicação quando todos os livros estão emprestados
- Cálculo de multa completamente incorreto
- Multas diferentes para o mesmo atraso dependendo do estoque

### Correção

```python
def get_overdue_books(self) -> List[dict]:
    """Retorna lista de livros atrasados"""
    overdue = []
    for isbn, book in self.books.items():
        for user_id, due_date in book.borrowed_by.items():
            if datetime.now() > due_date:
                days_late = (datetime.now() - due_date).days
                fine = days_late * 2.0  # ✅ Corrigido: R$ 2.00 por dia
                
                overdue.append({
                    "isbn": isbn,
                    "title": book.title,
                    "user_id": user_id,
                    "days_late": days_late,
                    "fine": fine
                })
    return overdue
```

### Explicação

A multa deve ser calculada como `dias_atrasados * valor_por_dia`, não dividindo por cópias disponíveis. Isso é um erro de lógica de negócio.

### Teste que Detecta

```python
def test_get_overdue_books():
    lib = Library("Test")
    lib.add_book("123", "Test", "Author", 2)
    lib.register_user("user1")
    
    book = lib.books["123"]
    book.borrow("user1")
    book.borrowed_by["user1"] = datetime.now() - timedelta(days=3)
    
    overdue = lib.get_overdue_books()
    assert overdue[0]["fine"] == 6.0  # 3 dias * R$ 2.00
```

---

## 🐛 Erro 7: Busca Case-Sensitive em `search_books()`

### Localização
**Arquivo**: `buggy_code.py`  
**Classe**: `Library`  
**Método**: `search_books()`  
**Linha**: ~127

### Código Buggy

```python
def search_books(self, query: str) -> List[dict]:
    """Busca livros por título ou autor"""
    results = []
    # ERRO 7: Comparação case-sensitive
    for isbn, book in self.books.items():
        if query in book.title or query in book.author:
            results.append({
                "isbn": isbn,
                "title": book.title,
                "author": book.author,
                "available": book.available_copies
            })
    return results
```

### Problema

A busca é case-sensitive. Buscar por "java" não encontra "Java", buscar por "MARTIN" não encontra "Martin".

### Impacto

- Usuários não encontram livros que existem
- Experiência de usuário ruim
- Necessidade de saber a capitalização exata
- Reduz efetividade da busca

### Correção

```python
def search_books(self, query: str) -> List[dict]:
    """Busca livros por título ou autor"""
    results = []
    # ✅ Corrigido: Busca case-insensitive
    query_lower = query.lower()
    for isbn, book in self.books.items():
        if query_lower in book.title.lower() or query_lower in book.author.lower():
            results.append({
                "isbn": isbn,
                "title": book.title,
                "author": book.author,
                "available": book.available_copies
            })
    return results
```

### Explicação

Para busca case-insensitive, converta tanto a query quanto os campos de busca para minúsculas (ou maiúsculas) antes de comparar.

### Teste que Detecta

```python
def test_search_books_case_insensitive():
    lib = Library("Test")
    lib.add_book("123", "Effective Java", "Joshua Bloch", 1)
    
    results_lower = lib.search_books("java")
    results_upper = lib.search_books("JAVA")
    results_mixed = lib.search_books("JaVa")
    
    assert len(results_lower) == 1  # Falha com código buggy
    assert len(results_upper) == 1
    assert len(results_mixed) == 1
```

---

## 📊 Resumo dos Erros

| # | Tipo | Localização | Problema | Impacto |
|---|------|-------------|----------|---------|
| 1 | Lógica | `Book.is_available()` | Condição invertida | Livros disponíveis aparecem como indisponíveis |
| 2 | Lógica | `Book.return_book()` | Operador errado (`-=` em vez de `+=`) | Devolver livros reduz estoque |
| 3 | Sintaxe | `Library.add_book()` | Parêntese faltando | Código não executa |
| 4 | Validação | `Library.borrow_book()` | Não valida usuário | Não registrados podem emprestar |
| 5 | Validação | `Library.calculate_fine()` | Não valida atraso | Multas negativas |
| 6 | Runtime | `Library.get_overdue_books()` | Divisão por zero + lógica errada | Crash e cálculo incorreto |
| 7 | Lógica | `Library.search_books()` | Case-sensitive | Busca ineficaz |

---

## 🎓 Lições Aprendidas

### 1. Ordem de Correção Importa

1. **Sintaxe** (Erro 3): Bloqueia execução, corrija primeiro
2. **Validação** (Erros 4, 5): Previne estados inválidos
3. **Lógica** (Erros 1, 2, 7): Produz resultados incorretos
4. **Runtime** (Erro 6): Causa crashes em casos específicos

### 2. Tipos de Bugs Requerem Técnicas Diferentes

- **Sintaxe**: Leia mensagem de erro do compilador
- **Lógica**: Teste com exemplos, analise algoritmo
- **Validação**: Pense em pré-condições e casos especiais
- **Runtime**: Teste edge cases, adicione validações

### 3. Testes São Essenciais

Cada bug foi detectado por um teste específico. Testes automatizados:
- Verificam correções
- Previnem regressões
- Documentam comportamento esperado
- Testam edge cases sistematicamente

### 4. Debugger É Seu Aliado

Use o debugger para:
- Pausar execução em pontos específicos
- Inspecionar valores de variáveis
- Entender fluxo de execução
- Identificar onde comportamento diverge do esperado

### 5. Validações Previnem Bugs

Sempre valide:
- **Pré-condições**: Entradas são válidas?
- **Invariantes**: Estado do objeto é consistente?
- **Pós-condições**: Resultado é válido?
- **Edge cases**: Valores extremos funcionam?

---

## ✅ Checklist de Validação

Após corrigir todos os bugs, verifique:

- [ ] ✅ Código executa sem erros de sintaxe
- [ ] ✅ Todos os 22 testes passam
- [ ] ✅ Livros disponíveis aparecem corretamente
- [ ] ✅ Devolver livros aumenta estoque
- [ ] ✅ Apenas usuários registrados podem emprestar
- [ ] ✅ Multas são calculadas corretamente
- [ ] ✅ Não há divisão por zero
- [ ] ✅ Busca funciona independente de capitalização

---

## 🚀 Próximos Passos

Parabéns por completar o Experimento 1! Você agora sabe:

✅ Identificar diferentes tipos de bugs  
✅ Usar o debugger efetivamente  
✅ Aplicar debugging sistemático  
✅ Validar correções com testes  

**Próximo experimento**: Experimento 2 - Observabilidade (análise de logs e métricas)

---

## 📚 Referências

- [Python Debugging with VS Code](https://code.visualstudio.com/docs/python/debugging)
- [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- [Pytest Documentation](https://docs.pytest.org/)
- [Clean Code by Robert Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
