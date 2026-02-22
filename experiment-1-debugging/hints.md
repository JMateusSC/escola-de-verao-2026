# 💡 Dicas - Experimento 1: Jogo dos 7 Erros

## Estratégia Geral

🎯 **Dica Principal**: Execute os testes primeiro! Eles mostram exatamente onde estão os problemas.

```bash
pytest experiment-1-debugging/test_solution.py -v
```

Cada teste que falha aponta para um bug específico. Leia o nome do teste e a mensagem de erro.

---

## 🐛 Erro 1: Lógica Invertida

<details>
<summary>Dica 1: Onde procurar?</summary>

O teste `test_is_available_with_copies` falha. Olhe para o método `Book.is_available()`.

</details>

<details>
<summary>Dica 2: O que está errado?</summary>

A função retorna `True` quando `available_copies <= 0`. Isso faz sentido? Um livro está disponível quando NÃO há cópias?

</details>

<details>
<summary>Dica 3: Como corrigir?</summary>

Inverta a lógica: um livro está disponível quando `available_copies > 0`.

```python
def is_available(self) -> bool:
    return self.available_copies > 0  # Corrigido
```

</details>

---

## 🐛 Erro 2: Operador Aritmético Errado

<details>
<summary>Dica 1: Onde procurar?</summary>

O teste `test_return_increases_copies` falha. Olhe para o método `Book.return_book()`.

</details>

<details>
<summary>Dica 2: O que deveria acontecer?</summary>

Quando um livro é devolvido, o número de cópias disponíveis deveria **aumentar**, não diminuir.

</details>

<details>
<summary>Dica 3: Como corrigir?</summary>

Troque `-=` por `+=`:

```python
def return_book(self, user_id: str) -> bool:
    if user_id not in self.borrowed_by:
        return False
    
    self.available_copies += 1  # Corrigido: incrementa
    del self.borrowed_by[user_id]
    return True
```

</details>

---

## 🐛 Erro 3: Erro de Sintaxe

<details>
<summary>Dica 1: Como identificar?</summary>

Execute o código: `python experiment-1-debugging/buggy_code.py`

Python mostrará um `SyntaxError` com a linha exata.

</details>

<details>
<summary>Dica 2: Onde está?</summary>

O erro está no método `Library.add_book()`, na linha que cria um novo `Book`.

</details>

<details>
<summary>Dica 3: O que falta?</summary>

Falta um parêntese de fechamento `)` no final da linha:

```python
else:
    self.books[isbn] = Book(isbn, title, author, copies)  # Corrigido
```

</details>

---

## 🐛 Erro 4: Falta Validação

<details>
<summary>Dica 1: Onde procurar?</summary>

O teste `test_borrow_book_unregistered_user` falha. Olhe para `Library.borrow_book()`.

</details>

<details>
<summary>Dica 2: O que está faltando?</summary>

A função não verifica se o usuário está registrado antes de emprestar o livro. Qualquer pessoa pode emprestar!

</details>

<details>
<summary>Dica 3: Como corrigir?</summary>

Adicione validação no início da função:

```python
def borrow_book(self, user_id: str, isbn: str) -> dict:
    # Corrigido: valida se usuário existe
    if user_id not in self.users:
        return {"success": False, "error": "User not registered"}
    
    if isbn not in self.books:
        return {"success": False, "error": "Book not found"}
    # ... resto do código
```

</details>

---

## 🐛 Erro 5: Falta Validação de Caso Especial

<details>
<summary>Dica 1: Onde procurar?</summary>

O teste `test_calculate_fine_no_delay` falha. Olhe para `Library.calculate_fine()`.

</details>

<details>
<summary>Dica 2: Qual é o problema?</summary>

A função calcula multa mesmo quando o livro NÃO está atrasado. Se `days_late` for negativo ou zero, a multa deveria ser 0.

</details>

<details>
<summary>Dica 3: Como corrigir?</summary>

Adicione validação antes de calcular a multa:

```python
def calculate_fine(self, user_id: str, isbn: str) -> float:
    # ... código anterior ...
    
    days_late = (datetime.now() - due_date).days
    
    # Corrigido: verifica se está atrasado
    if days_late <= 0:
        return 0.0
    
    fine = days_late * 2.0
    return fine
```

</details>

---

## 🐛 Erro 6: Divisão por Zero

<details>
<summary>Dica 1: Onde procurar?</summary>

O teste `test_get_overdue_books` pode falhar com `ZeroDivisionError`. Olhe para `Library.get_overdue_books()`.

</details>

<details>
<summary>Dica 2: Onde está a divisão perigosa?</summary>

A linha `fine = days_late / book.available_copies` pode causar divisão por zero se todos os livros estiverem emprestados (`available_copies = 0`).

</details>

<details>
<summary>Dica 3: Como corrigir?</summary>

A lógica de cálculo de multa está errada. A multa deveria ser baseada em dias de atraso, não em cópias disponíveis:

```python
def get_overdue_books(self) -> List[dict]:
    overdue = []
    for isbn, book in self.books.items():
        for user_id, due_date in book.borrowed_by.items():
            if datetime.now() > due_date:
                days_late = (datetime.now() - due_date).days
                fine = days_late * 2.0  # Corrigido: R$ 2.00 por dia
                
                overdue.append({
                    "isbn": isbn,
                    "title": book.title,
                    "user_id": user_id,
                    "days_late": days_late,
                    "fine": fine
                })
    return overdue
```

</details>

---

## 🐛 Erro 7: Comparação Case-Sensitive

<details>
<summary>Dica 1: Onde procurar?</summary>

O teste `test_search_books_case_insensitive` falha. Olhe para `Library.search_books()`.

</details>

<details>
<summary>Dica 2: Qual é o problema?</summary>

A busca usa `query in book.title`, que é case-sensitive. Buscar por "java" não encontra "Java".

</details>

<details>
<summary>Dica 3: Como corrigir?</summary>

Converta tudo para minúsculas antes de comparar:

```python
def search_books(self, query: str) -> List[dict]:
    results = []
    query_lower = query.lower()  # Corrigido
    for isbn, book in self.books.items():
        # Corrigido: comparação case-insensitive
        if query_lower in book.title.lower() or query_lower in book.author.lower():
            results.append({
                "isbn": isbn,
                "title": book.title,
                "author": book.author,
                "available": book.available_copies
            })
    return results
```

</details>

---

## 🔧 Dicas de Debugging

### Usando o Debugger do VS Code

1. **Colocar Breakpoint**: Clique à esquerda do número da linha
2. **Iniciar Debug**: Pressione F5 ou clique no ícone de play
3. **Inspecionar Variáveis**: Veja o painel "Variables" à esquerda
4. **Avançar**: Use F10 (Step Over) para executar linha por linha

### Debugging com Print

Adicione prints temporários para entender o fluxo:

```python
def is_available(self):
    print(f"DEBUG: available_copies = {self.available_copies}")
    result = self.available_copies <= 0
    print(f"DEBUG: returning {result}")
    return result
```

### Lendo Mensagens de Teste

Quando um teste falha, leia a mensagem:

```
AssertionError: assert False is True
```

Isso significa que o teste esperava `True` mas recebeu `False`.

---

## 📊 Progresso

Use este checklist para acompanhar seu progresso:

- [ ] ✅ Erro 1: `is_available()` - Lógica invertida
- [ ] ✅ Erro 2: `return_book()` - Operador errado
- [ ] ✅ Erro 3: `add_book()` - Sintaxe
- [ ] ✅ Erro 4: `borrow_book()` - Falta validação
- [ ] ✅ Erro 5: `calculate_fine()` - Falta validação
- [ ] ✅ Erro 6: `get_overdue_books()` - Divisão por zero
- [ ] ✅ Erro 7: `search_books()` - Case-sensitive

---

## 🆘 Ainda com Dúvidas?

Se após usar essas dicas você ainda estiver com dificuldades:

1. Execute os testes com mais detalhes: `pytest experiment-1-debugging/test_solution.py -vv`
2. Use o debugger para inspecionar valores em tempo real
3. Compare seu código com `solution/fixed_code.py`
4. Leia o guia completo em `solution/SOLUTION_GUIDE.md`

Boa sorte! 🚀
