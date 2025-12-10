#  Projeto ADA: Assistente Digital de Análise de PDF

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/Status-Finalizado-green)
![IA](https://img.shields.io/badge/AI-Local-orange)

Este projeto é uma ferramenta de linha de comando (CLI) desenvolvida como parte do processo seletivo para a bolsa **Trainee LLM do Projeto ADA**.

O objetivo é processar arquivos PDF, extrair metadados estatísticos, imagens e gerar resumos inteligentes utilizando **Modelos de Linguagem (LLM)** rodando 100% localmente, sem dependência de APIs externas.

---

##  Sumário

1. [Sobre o Projeto](#-sobre-o-projeto)
2. [Funcionalidades Principais (Obrigatórias)](#-funcionalidades-principais-obrigatórias)
3. [ Funcionalidades Opcionais Implementadas](#-funcionalidades-opcionais-implementadas)
4. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
5. [Como Rodar o Projeto](#-como-rodar-o-projeto)
6. [Estrutura de Pastas](#-estrutura-do-projeto)
7. [Destaques para Avaliação](#-destaques-para-avaliação)

---

## Funcionalidades Principais (Obrigatórias)

O projeto atende integralmente aos requisitos mandatórios do desafio:

*  **Análise de PDF:** Extração de contagem de palavras, tamanho do arquivo, número de páginas e lista das 10 palavras mais comuns.
* **Extração de Imagens:** Identificação e salvamento automático de todas as imagens contidas no documento em diretórios organizados.
* **Integração com LLM:** Carregamento de modelo Hugging Face local (**Qwen2.5-0.5B-Instruct**) para geração de resumos contextuais do documento.

---

##  Funcionalidades Opcionais Implementadas

Além do escopo básico, foram implementadas as seguintes funcionalidades listadas como diferenciais no edital:

### 1. Relatório Final Unificado
Geração automática de um arquivo **Markdown (`.md`)** ao final da execução. Este relatório consolida:
* As estatísticas extraídas.
* A tabela de frequência de palavras.
* O resumo gerado pela Inteligência Artificial.

### 2. Sistema de Logs (Rastreabilidade)
Implementação de um **Logger (`logger.py`)** robusto que opera em dois níveis:
* **Arquivo (`execucao.log`):** Grava o histórico completo de operações para auditoria.
* **Console:** Exibe feedback visual formatado e limpo para o usuário durante o processamento.

### 3. Limpeza e Normalização de Texto
Desenvolvimento de um algoritmo próprio em `extractor.py` para tratamento avançado de texto:
* **Remoção de Stopwords:** Filtragem contextual de artigos e preposições.
* **Lematização Manual:** Regras de singularização para agrupar termos (ex: "sistemas" conta como "sistema"), garantindo métricas de vocabulário mais precisas.

### 4. Tratamento de Exceções e Robustez
O código é protegido por blocos `try/except` em pontos críticos (leitura de arquivo, download do modelo, salvamento de imagem), garantindo que falhas parciais não interrompam o fluxo principal da aplicação.

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.9+
- **Bibliotecas Principais:**
  - `pypdf`: Parsing e leitura de arquivos binários PDF.
  - `transformers` & `torch`: Pipeline de inferência para IA Generativa.
  - `argparse`: Construção da interface de linha de comando (CLI).
  - `logging`: Sistema de monitoramento.

---

## Como Rodar o Projeto

### Pré-requisitos
Como este projeto executa uma Rede Neural localmente, recomenda-se:
- **RAM:** Mínimo de 8GB.
- **Espaço em Disco:** Aprox. 2GB livres (para o modelo).

### Instalação

1. Clone o repositório e acesse a pasta:
```bash
git clone https://github.com/ranielly15/Selecao_ProjetoAda.git
cd <NOME_DA_PASTA>
 ```
Crie e ative um ambiente virtual (Recomendado):



### Windows
```bash
python -m venv venv
venv\Scripts\activate
```
### Linux/Mac
```
source venv/bin/activate
```
Instale as dependências:
```
pip install -r requirements.txt
(Dependências: torch, transformers, pypdf, accelerate)
```
Executando a Ferramenta
Para analisar um PDF, execute o comando abaixo:

Comando Básico:
```
python src/main.py --input "arquivos_teste/documento.pdf"
```
Comando Personalizado (Salvando imagens em outra pasta):

```
python src/main.py --input "documento.pdf" --image_dir "./minhas_imagens"
```
---
## Estrutura do Projeto
A organização segue o princípio de Separação de Responsabilidades (SoC):

```

├── src/
│   ├── cli/           # Interface com o usuário (Argument Parsing)
│   ├── pdf/           # Camada de extração de dados e imagens
│   ├── llm/           # Camada de IA (Model Loading & Inference)
│   ├── utils/         # Ferramentas (Logger, Report Builder)
│   └── main.py        # Entrypoint (Unidade de Controle)
├── arquivos_teste/    # PDFs para validação
├── requirements.txt   # Dependências do projeto
├── execucao.log       # Log de auditoria
└── README.md          # Documentação
```

## Destaques para Avaliação

**Arquitetura e Modularização:** O código não é um script único. Ele foi estruturado como uma aplicação modular, separando a lógica de I/O, processamento de dados e IA em pacotes distintos (src.pdf, src.llm, src.cli).

**Algoritmos e Lógica ("Pythonico"):** Implementação de algoritmo próprio em extractor.py para normalização de palavras (singularização) sem depender de bibliotecas pesadas como NLTK, demonstrando capacidade de resolver problemas com lógica pura.

**Tratamento de Erros e Logs (Robustez):** Uso extensivo de blocos try/except para garantir que o programa não quebre (crash) se encontrar uma imagem corrompida ou falha no modelo, além de sistema de Logs (logger.py) para auditoria.

**Performance e Métricas:** Implementação de benchmarking (medição de tempo) para cada etapa do processo e contagem de tokens, mostrando preocupação com a eficiência do código.
