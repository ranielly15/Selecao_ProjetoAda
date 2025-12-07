import os
import sys
from typing import Dict, Any

# Configuração dinâmica do PYTHONPATH para permitir importação dos módulos irmãos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from pdf.extractor import extract_pdf_info
# from pdf.images import extract_images_from_pdf       # Futuro módulo para extração de imagens

def main() -> None:
    """
    Função principal (Entry Point) da CLI do Projeto ADA.
    Gerencia o fluxo de leitura, extração e exibição de dados.
    """
    print("--- Iniciando Processamento ADA ---")

    # Definição de caminhos relativos à raiz do projeto
    project_root = os.path.dirname(current_dir)
    filename = "Sistemas de Informação_ O Sistema Nervoso das Organizações Modernas.pdf"
    pdf_path = os.path.join(project_root, "arquivos_teste", filename)

    # Verifica existência do recurso
    if not os.path.exists(pdf_path):
        print(f"❌ Erro Crítico: Arquivo alvo não encontrado em: {pdf_path}")
        return

    print(f"Processando arquivo: {filename}")

    # 1. Execução do módulo de extração de texto
    print("\n🔍 --- Análise Estrutural e Textual ---")
    results: Dict[str, Any] = extract_pdf_info(pdf_path)

    if "erro" in results:
        print(f"❌ Falha na extração: {results['erro']}")
        return

    # Exibição dos resultados (Report)
    print(f"✅ Status: Sucesso")
    print(f"📄 Páginas: {results['num_pages']}")
    print(f"💾 Tamanho: {results['file_size_bytes']} bytes")
    print(f"🔤 Palavras Totais: {results['total_words']}")
    print(f"📚 Vocabulário Único: {results['vocab_size']}")
    print(f"🔝 Top 10 Termos: {results['top_10_words']}")

    # 2. Futura integração de Imagens e LLM virá aqui
    # ...

if __name__ == "__main__":
    main()