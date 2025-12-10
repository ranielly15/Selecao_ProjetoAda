# Projeto ADA: Assistente Digital de Análise de PDF

Este projeto é uma ferramenta de linha de comando (CLI) desenvolvida para o processo seletivo da bolsa Trainee LLM do Projeto ADA. O objetivo é processar arquivos PDF, extrair metadados estatísticos, imagens e gerar resumos inteligentes utilizando Modelos de Linguagem (LLM) rodando localmente.

## 📋 Funcionalidades Implementadas

O projeto atende a todos os requisitos obrigatórios e inclui diversas funcionalidades extras:

### 1. Análise Estatística (Sem IA)
- **Contagem de Palavras:** Análise bruta e limpa (removendo *stopwords*).
- **Vocabulário:** Cálculo de palavras únicas com normalização (lematização básica).
- **Top 10 Termos:** Identificação das palavras mais frequentes no texto.
- **Metadados:** Tamanho do arquivo, número de páginas e bytes.

### 2. Manipulação de Arquivos
- **Extração de Imagens:** Detecta e salva automaticamente todas as imagens do PDF em pastas organizadas.
- **Logs de Execução:** Registro detalhado de operações e erros em arquivo (`execucao.log`) e console.
- **Relatório Unificado:** Geração automática de um relatório final em Markdown (`.md`) contendo todas as estatísticas e o resumo gerado.

### 3. Inteligência Artificial (LLM Local)
- **Resumo Automático:** Utiliza o modelo **Qwen2.5-0.5B-Instruct** (via Hugging Face) para ler e resumir o conteúdo do PDF.
- **Métricas de Performance:** Monitoramento de tempo de execução e contagem de tokens (entrada/saída) para análise de custo computacional.
- **Execução Otimizada:** Carregamento inteligente do modelo para evitar estouro de memória.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.9+
- **PDF:** `pypdf` (Leitura e extração)
- **IA:** `transformers`, `torch` (Hugging Face)
- **CLI:** `argparse` (Interface de linha de comando)
- **Logs:** `logging` (Rastreabilidade)

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos
Certifique-se de ter o Python instalado. Recomenda-se criar um ambiente virtual:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

Instale as dependências:
pip install torch transformers pypdf accelerate

Executando a Ferramenta
Para analisar um PDF, execute o arquivo principal apontando para o seu documento:

python src/main.py --input "caminho/do/seu_arquivo.pdf"

Opcionalmente, defina onde salvar as imagens extraídas:
python src/main.py --input "documento.pdf" --image_dir "./minhas_imagens"
```

### Estrutura do Projeto
A organização segue padrões de modularização para separar responsabilidades:


```Plaintext

├── src/
│   ├── cli/           # Tratamento de argumentos (argparse)
│   ├── pdf/           # Lógica de extração de texto e imagens
│   ├── llm/           # Integração com modelo de IA 
│   ├── utils/         # Logs e geração de relatórios
│   └── main.py        # Orquestrador principal
├── imagens/           # Destino automático das imagens extraídas
├── execucao.log       # Histórico de operações
└── README.md          # Documentação
```


## Pontos de Destaque para Avaliação
Gostaria de destacar os seguintes pontos na implementação:

- **Qualidade de Código e Tipagem:** O código prioriza clareza, com nomes de variáveis descritivos e uso de Type Hints (opcional do edital) em módulos chave.

- **Monitoramento de Recursos:** Implementação de cronômetros para medir o tempo de cada etapa (extração vs IA) e contagem de tokens, demonstrando preocupação com performance.

- **Algoritmo de Normalização Próprio:** Criação de uma lógica manual de singularização de palavras em extractor.py para evitar dependências externas pesadas apenas para limpeza de texto.

- **Robustez:** Tratamento de erros (try/except) em todas as etapas críticas para garantir que uma falha na extração de imagem não pare a geração do resumo.