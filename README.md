# Experimentos Práticos de Debugging e Investigação de Falhas

Bem-vindo aos experimentos práticos hands-on! Este repositório contém quatro experimentos independentes que permitirão aplicar técnicas de investigação e correção de falhas em software.

## 🎯 Objetivos de Aprendizado

Ao completar estes experimentos, você será capaz de:
- Identificar e corrigir diferentes tipos de bugs (sintaxe, lógica, runtime)
- Usar ferramentas de debugging integradas ao VS Code
- Analisar logs estruturados e métricas de observabilidade
- Identificar e corrigir race conditions em código concorrente
- Aplicar a técnica dos 5 Porquês para análise de causa raiz

## 📚 Experimentos Disponíveis

### [Experimento 1: Debugging Multi-Tipo](./experiment-1-debugging/)
Pratique a identificação e correção de três tipos diferentes de bugs usando o debugger do VS Code.

**Conceitos:** Syntax errors, logic errors, runtime errors, breakpoints, variable inspection

**Duração estimada:** 30-45 minutos

### [Experimento 2: Observabilidade](./experiment-2-observability/)
Analise logs estruturados e métricas (Golden Signals) de um serviço em execução para identificar problemas.

**Conceitos:** Structured logging, Golden Signals (latency, traffic, errors, saturation), log analysis

**Duração estimada:** 45-60 minutos

### [Experimento 3: Concorrência](./experiment-3-concurrency/)
Identifique e corrija race conditions em código concorrente usando mecanismos de sincronização.

**Conceitos:** Race conditions, thread safety, locks, concurrent testing

**Duração estimada:** 45-60 minutos

### [Experimento 4: Análise de Incidente](./experiment-4-incident-analysis/)
Analise um cenário realista de falha em produção usando a técnica dos 5 Porquês.

**Conceitos:** Root cause analysis, Five Whys technique, incident investigation, preventive actions

**Duração estimada:** 30-45 minutos

## 🚀 Como Começar

### Pré-requisitos

- Python 3.8 ou superior
- VS Code com extensão Python instalada
- Git

### Setup Rápido (GitHub Codespace)

1. Abra este repositório no GitHub Codespace
2. O ambiente será configurado automaticamente com todas as dependências
3. Navegue até o experimento desejado e siga as instruções no README

### Setup Local

1. Clone este repositório:
```bash
git clone <repository-url>
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Verifique a instalação:
```bash
pytest --version
python --version
```

## 🧪 Executando os Testes

Cada experimento inclui testes automatizados para validar suas correções:

```bash
# Executar todos os testes
pytest

# Executar testes de um experimento específico
pytest experiment-1-debugging/

# Executar com saída detalhada
pytest -v

# Executar com cobertura
pytest --cov=. --cov-report=html
```

## 🐛 Usando o Debugger

Este projeto inclui configurações de debug pré-configuradas para VS Code:

1. Abra o arquivo que deseja debugar
2. Clique na margem esquerda para adicionar breakpoints
3. Pressione `F5` ou vá em "Run and Debug"
4. Selecione a configuração apropriada
5. Use os controles de debug para step over, step into, inspect variables

## 📖 Estrutura dos Experimentos

Cada experimento segue a mesma estrutura:

```
experiment-X-nome/
├── README.md              # Instruções e objetivos
├── código_principal.py    # Código para trabalhar
├── test_*.py             # Testes automatizados
├── hints.md              # Dicas progressivas
└── solution/             # Solução de referência
    ├── código_corrigido.py
    └── SOLUTION_GUIDE.md
```

## 💡 Dicas Gerais

- **Leia o README de cada experimento** antes de começar
- **Use o debugger** ao invés de apenas ler o código
- **Execute os testes frequentemente** para validar seu progresso
- **Consulte as hints** se ficar travado, mas tente resolver sozinho primeiro
- **Compare com a solução** apenas depois de completar o experimento

## 🤝 Suporte

Se encontrar problemas técnicos ou tiver dúvidas sobre os conceitos:

1. Verifique o README do experimento específico
2. Consulte o arquivo hints.md
3. Revise o material da apresentação
4. Entre em contato com o instrutor

## 📝 Licença

Este material é fornecido para fins educacionais.

---

**Pronto para começar?** Escolha um experimento acima e divirta-se aprendendo! 🎓
