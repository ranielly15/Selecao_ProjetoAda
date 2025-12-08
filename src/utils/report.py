import os

def save_markdown_report(pdf_info, summary_text, output_dir):
    """
    Gera um relatório unificado em Markdown com todas as análises.
    Atende ao requisito opcional: Relatório final unificado em Markdown.
    """
    filename = pdf_info.get('filename', 'relatorio')
    # Remove a extensão do nome para usar no arquivo
    safe_name = os.path.splitext(filename)[0]
    report_path = os.path.join(output_dir, f"Relatorio_{safe_name}.md")

    # Construção do conteúdo Markdown
    md_content = f"""# Relatório de Análise: {filename}

## 1. Estatísticas Gerais
| Métrica | Valor |
|---------|-------|
| **Tamanho do Arquivo** | {pdf_info.get('filesize_bytes', 0)} bytes |
| **Total de Páginas** | {pdf_info.get('num_pages', 0)} |
| **Total de Palavras** | {pdf_info.get('total_words', 0)} |
| **Vocabulário** | {pdf_info.get('vocab_size', 0)} palavras únicas |

## 2. Top 10 Palavras Mais Comuns
As palavras mais frequentes encontradas no texto (ignorando stopwords):

| Palavra | Frequência |
|---------|------------|
"""
    
    # Adiciona as linhas da tabela de palavras
    for word, count in pdf_info.get('top_10_words', []):
        md_content += f"| {word} | {count} |\n"

    # Adiciona o Resumo da IA
    md_content += f"""
## 3. Resumo Inteligente (IA)
> {summary_text}

---
*Gerado automaticamente pelo Projeto ADA CLI.*
"""

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        return report_path
    except Exception as e:
        return None