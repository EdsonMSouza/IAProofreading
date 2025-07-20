# Avaliador de Respostas com LLM

Este projeto tem como objetivo avaliar automaticamente respostas dissertativas utilizando um Modelo de Linguagem (LLM). Ele foi desenvolvido para processar uma planilha com respostas, gerar feedbacks e atribuir notas com base em critérios definidos, integrando-se a um endpoint local de LLM.

## 🗂 Estrutura do Projeto

```
app/
├── avaliar.py                      # Script principal para executar a avaliação via terminal
├── core.py                         # Funções centrais de processamento e avaliação
├── llm.py                          # Comunicação com o modelo de linguagem (LLM)
├── gera_notas.ipynb               # Notebook para testes e geração de notas
└── data/
    ├── respostas_simuladas.xlsx               # Planilha de entrada com respostas
    └── respostas_simuladas_avaliado.xlsx      # Resultado com notas e feedbacks
```

## 🚀 Como Executar

### 1. Requisitos

- Python 3.9+
- Dependências do projeto (`requirements.txt`)
- Um servidor LLM local (como o LM Studio ou equivalente) escutando na URL configurada

### 2. Execução via linha de comando

Execute a avaliação de uma planilha `.xlsx`:

```bash
python avaliar.py data/respostas_simuladas.xlsx
```

### 3. Execução via notebook

Abra o arquivo `gera_notas.ipynb` para testar ou visualizar o processo passo a passo.

## ⚙️ Configurações

O modelo e a URL do endpoint são configuráveis nos scripts, especialmente em `llm.py` e `avaliar.py`. Certifique-se de que o endpoint esteja acessível e configurado corretamente.

## 🧠 Sobre o LLM

O projeto assume que um modelo de linguagem é capaz de:

- Analisar perguntas e respostas
- Atribuir notas coerentes
- Gerar feedback textual personalizado

O modelo utilizado pode ser o `qwen2.5-7b-instruct-1m`, `gemma`, `mistral`, entre outros, desde que compatível com o formato de requisição da OpenAI API.

## 📂 Dados

- `respostas_simuladas.xlsx`: Arquivo com colunas `Endereço de e-mail`, `Nome`, e perguntas com as respectivas respostas.
- `respostas_simuladas_avaliado.xlsx`: Resultado da avaliação contendo feedback e nota para cada resposta.

## 📌 Observações

- Este projeto é de uso acadêmico e pode ser adaptado para diversas finalidades educacionais.
- Certifique-se de validar eticamente o uso de modelos de IA para avaliações.

## Como citar este conteúdo

```
DE SOUZA, Edson Melo (2025, July 20). IAProofreading.
Available in: https://github.com/EdsonMSouza/IAProofreading
```

Or BibTeX for LaTeX:

```latex
@misc{desouza2020IAProofreading,
  author = {DE SOUZA, Edson Melo},
  title = {IAProofreading v.1.0},
  url = {https://github.com/EdsonMSouza/IAProofreading},
  year = {2025},
  month = {July},
  publisher = {GitHub}
}
```

## 📝 Licença

Esta obra está licenciada com uma Licença [Creative Commons ShareAlike 4.0 Internacional](http://creativecommons.org/licenses/by-sa/4.0/).

[![CC BY-SA 4.0](https://licensebuttons.net/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)
