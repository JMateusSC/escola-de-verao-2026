# Experimento 1: Debugging Multi-Tipo - Jogo dos 7 Erros

## 🎯 Objetivos de Aprendizado

Ao completar este experimento, você será capaz de:

1. **Identificar diferentes tipos de bugs em código realista**: Reconhecer erros de sintaxe, lógica, runtime e validação
2. **Usar o debugger do VS Code efetivamente**: Configurar breakpoints, inspecionar variáveis e rastrear fluxo de execução
3. **Aplicar debugging sistemático**: Seguir um processo estruturado para localizar e corrigir falhas
4. **Validar correções com testes**: Usar testes automatizados para verificar que os bugs foram corrigidos

## 📚 Descrição do Experimento

Este experimento simula um **Sistema de Gerenciamento de Biblioteca** com funcionalidades realistas:

- Cadastro de livros e usuários
- Empréstimo e devolução de livros
- Cálculo de multas por atraso
- Busca de livros por título ou autor
- Listagem de livros disponíveis e atrasados

O código contém **7 bugs escondidos** de diferentes tipos. Seu desafio é encontrar e corrigir todos eles!

## 🐛 Os 7 Erros

O código contém os seguintes tipos de erros:

1. **Erro de Lógica** - Condição invertida
2. **Erro de Lógica** - Operador aritmético errado
3. **Erro de Sintaxe** - Parêntese faltando
4. **Erro de Validação** - Falta verificação de pré-condição
5. **Erro de Lógica** - Falta validação de caso especial
6. **Erro de Runtime** - Divisão por zero potencial
7. **Erro de Lógica** - Comparação case-sensitive

## 🔍 Instruções

### Passo 1: Análise Inicial

1. Abra o arquivo `buggy_code.py`
2. Leia o código e entenda a estrutura:
   - Classe `Book`: Representa um livro
   - Classe `Library`: Gerencia a biblioteca
3. Execute o código: `python experiment-1-debugging/buggy_code.py`
4. Observe se há erros imediatos

### Passo 2: Executar os Testes

Os testes revelam onde estão os bugs:

```bash
# Execute os testes da solução
pytest experiment-1-debugging/test_solution.py -v
```

Observe quais testes falham. Cada teste que falha indica um bug específico.

### Passo 3: Usar o Debugger

1. Abra o painel de Debug no VS Code (Ctrl+Shift+D)
2. Selecione "Experiment 1: Debugging Multi-Tipo"
3. Coloque breakpoints nas funções suspeitas
4. Execute o debugger (F5)
5. Inspecione variáveis e fluxo de execução

**Dica**: Coloque breakpoints em:
- `Book.is_available()` - linha 24
- `Book.return_book()` - linha 39
- `Library.add_book()` - linha 56
- `Library.borrow_book()` - linha 64
- `Library.calculate_fine()` - linha 82
- `Library.get_overdue_books()` - linha 106
- `Library.search_books()` - linha 123

### Passo 4: Encontrar e Corrigir os Bugs

Para cada bug:

1. **Identifique o sintoma**: Qual teste falha? O que ele espera?
2. **Localize o código**: Onde está o problema?
3. **Entenda a causa**: Por que o código está errado?
4. **Corrija**: Faça a alteração mínima necessária
5. **Valide**: Execute os testes novamente

### Passo 5: Validação Final

Quando todos os bugs estiverem corrigidos:

```bash
# Todos os testes devem passar
pytest experiment-1-debugging/test_solution.py -v

# Resultado esperado: 30+ testes passando ✅
```

## 💡 Estratégias de Debugging

### 1. Leia as Mensagens de Erro

Python fornece mensagens detalhadas:
- **SyntaxError**: Indica linha exata do erro de sintaxe
- **AssertionError**: Mostra valor esperado vs. obtido
- **AttributeError/TypeError**: Indica problema de tipo ou atributo

### 2. Use Print Debugging

Adicione prints temporários para entender o fluxo:

```python
def is_available(self):
    print(f"DEBUG: available_copies = {self.available_copies}")
    return self.available_copies <= 0
```

### 3. Use o Debugger Visual

- **Breakpoints**: Pause a execução em pontos específicos
- **Step Over (F10)**: Execute linha por linha
- **Watch**: Monitore valores de variáveis específicas
- **Call Stack**: Veja a sequência de chamadas de função

### 4. Teste Casos Extremos

Pense em casos especiais:
- O que acontece quando `available_copies = 0`?
- E se o usuário não estiver registrado?
- E se a data de vencimento for hoje?

### 5. Compare com o Comportamento Esperado

Para cada função, pergunte:
- O que ela **deveria** fazer?
- O que ela **está** fazendo?
- Onde está a diferença?

## 📝 Conceitos Relacionados

Este experimento aplica conceitos da apresentação:

- **Tipos de Bugs**: Sintaxe, Lógica, Runtime, Validação
- **Técnicas de Debugging**: Debugger, breakpoints, inspeção de variáveis
- **Validação com Testes**: Testes automatizados como ferramenta de validação
- **Debugging Sistemático**: Processo estruturado de investigação

## 🆘 Precisa de Ajuda?

- **Dicas progressivas**: Consulte `hints.md` para dicas sem revelar a solução
- **Solução completa**: Após completar, veja `solution/SOLUTION_GUIDE.md`
- **Código corrigido**: Compare com `solution/fixed_code.py`

## ✅ Checklist de Conclusão

- [ ] Erro 1 corrigido: `is_available()` retorna True quando há cópias
- [ ] Erro 2 corrigido: `return_book()` aumenta cópias disponíveis
- [ ] Erro 3 corrigido: `add_book()` não tem erro de sintaxe
- [ ] Erro 4 corrigido: `borrow_book()` valida se usuário está registrado
- [ ] Erro 5 corrigido: `calculate_fine()` retorna 0 se não está atrasado
- [ ] Erro 6 corrigido: `get_overdue_books()` não causa divisão por zero
- [ ] Erro 7 corrigido: `search_books()` funciona case-insensitive
- [ ] Todos os testes passam ✅

## 🎓 Próximos Passos

Após completar este experimento, você estará pronto para:
- **Experimento 2**: Observabilidade (análise de logs e métricas)
- **Experimento 3**: Concorrência (race conditions)
- **Experimento 4**: Análise de Incidente (técnica dos 5 Porquês)

Boa sorte! 🚀
