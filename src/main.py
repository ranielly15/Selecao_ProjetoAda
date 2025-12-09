import os
import sys
from pypdf import PdfReader

# Ajuste de path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from pdf.extractor import extract_pdf_info
from pdf.images import extract_images_from_pdf
from cli.arguments import get_arguments
from utils.logger import setup_logger
from utils.report import save_markdown_report

try:
    from llm.summarize import generate_summary
except ImportError:
    generate_summary = None

logger = setup_logger()

def format_bytes(size):
    """Converte bytes para KB ou MB para ficar legível."""
    power = 2**10
    n = size
    power_labels = {0 : '', 1: 'KB', 2: 'MB', 3: 'GB'}
    count = 0
    while n > power:
        n /= power
        count += 1
    return f"{n:.2f} {power_labels.get(count, 'bytes')}"

def print_box(text):
    """Cria uma caixa bonita ao redor do texto."""
    lines = text.split('\n')
    width = max(len(line) for line in lines) + 4
    print("╔" + "═" * width + "╗")
    for line in lines:
        print(f"║  {line:<{width-4}}  ║")
    print("╚" + "═" * width + "╝")

def main() -> None:
    args = get_arguments()
    
    logger.info("--- Iniciando Processamento ADA ---")

    # 1. Definição do Arquivo
    if args.input:
        pdf_path = args.input
    else:
        project_root = os.path.dirname(current_dir)
        filename = "Sistemas de Informação_ O Sistema Nervoso das Organizações Modernas.pdf"
        possible_paths = [
            os.path.join(project_root, "arquivos_teste", filename),
            os.path.join(project_root, filename)
        ]
        pdf_path = None
        for p in possible_paths:
            if os.path.exists(p):
                pdf_path = p
                break
        if not pdf_path:
             pdf_path = os.path.join(project_root, "arquivos_teste", filename)

    if not os.path.exists(pdf_path):
        logger.error(f"[ERRO CRÍTICO] Arquivo não encontrado: {pdf_path}")
        return

    logger.info(f"Processando arquivo: {pdf_path}")

    # Variáveis globais
    final_pdf_info = {}
    final_summary = "Resumo não gerado."

    # ==========================================
    # PASSO 1: Análise do PDF (Visual Profissional)
    # ==========================================
    logger.info("Iniciando Análise de Metadados...")
    try:
        final_pdf_info = extract_pdf_info(pdf_path)
        
        # Conversão de tamanho amigável
        tamanho_humano = format_bytes(final_pdf_info.get('filesize_bytes', 0))

        # --- EXIBIÇÃO PROFISSIONAL ---
        print("\n")
        print_box("RELATÓRIO DE ANÁLISE ESTATÍSTICA")
        
        print(f" [DADOS GERAIS]")
        # O :<15 garante que a coluna tenha sempre 15 espaços de largura
        print(f"   {'Arquivo':<15} : {final_pdf_info.get('filename')}")
        print(f"   {'Tamanho':<15} : {tamanho_humano}")
        print(f"   {'Páginas':<15} : {final_pdf_info.get('num_pages')}")
        print(f"   {'Palavras':<15} : {final_pdf_info.get('total_words')}")
        print(f"   {'Vocabulário':<15} : {final_pdf_info.get('vocab_size')} termos únicos")
        print("-" * 50)
        
        print(f" [TOP 10 TERMOS MAIS FREQUENTES]")
        print(f"   {'#':<3} {'PALAVRA':<20} {'FREQ'}")
        print(f"   {'-'*3} {'-'*20} {'-'*4}")
        
        for i, (word, count) in enumerate(final_pdf_info.get('top_10_words', []), 1):
            print(f"   {i:<3} {word:<20} {count}")
        print("-" * 50 + "\n")
            
    except Exception as e:
        logger.error(f"Falha nos metadados: {e}")

    # ==========================================
    # PASSO 2: Extração de Imagens
    # ==========================================
    logger.info("Iniciando Extração de Imagens...")
    try:
        pdf_filename = os.path.basename(pdf_path)
        pdf_name_no_ext = os.path.splitext(pdf_filename)[0]

        if args.image_dir:
            base_dir = args.image_dir
        else:
            project_root = os.path.dirname(current_dir)
            base_dir = os.path.join(project_root, "imagens")

        final_output_dir = os.path.join(base_dir, pdf_name_no_ext)
        
        qtd = extract_images_from_pdf(pdf_path, output_dir=final_output_dir)
        logger.info(f"[SUCESSO] {qtd} imagens salvas em: {final_output_dir}")

    except Exception as e:
        logger.error(f"Erro ao extrair imagens: {e}")

    # ==========================================
    # PASSO 3: Geração de Resumo (LLM Local)
    # ==========================================
    if generate_summary:
        logger.info("Iniciando Geração de Resumo com IA Local...")
        try:
            reader = PdfReader(pdf_path)
            full_text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t: full_text += t + "\n"
            
            if not full_text.strip():
                logger.warning("PDF sem texto detectável para resumo.")
            else:
                final_summary = generate_summary(full_text)
                
                print("\n")
                print_box("RESUMO INTELIGENTE (IA)")
                print(final_summary)
                print("=" * 60 + "\n")
        
        except Exception as e:
            logger.error(f"Falha na geração do resumo: {e}")
            final_summary = f"Erro ao gerar resumo: {e}"

    # ==========================================
    # PASSO EXTRA: Relatório Unificado
    # ==========================================
    logger.info("Gerando Relatório Final Unificado...")
    project_root = os.path.dirname(current_dir)
    report_file = save_markdown_report(final_pdf_info, final_summary, project_root)
    
    if report_file:
        logger.info(f"Relatório Markdown salvo em: {report_file}")
    else:
        logger.error("Falha ao salvar relatório Markdown.")

if __name__ == "__main__":
    main()