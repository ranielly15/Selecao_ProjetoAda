import os
import sys
import time  # <--- Nova importação para medir o tempo
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

# Funções auxiliares de formatação visual
def format_bytes(size):
    power = 2**10
    n = size
    power_labels = {0 : '', 1: 'KB', 2: 'MB', 3: 'GB'}
    count = 0
    while n > power:
        n /= power
        count += 1
    return f"{n:.2f} {power_labels.get(count, 'bytes')}"

def print_box(text):
    lines = text.split('\n')
    width = max(len(line) for line in lines) + 4
    print("╔" + "═" * width + "╗")
    for line in lines:
        print(f"║  {line:<{width-4}}  ║")
    print("╚" + "═" * width + "╝")

def main() -> None:
    args = get_arguments()
    logger.info("--- Iniciando Processamento ADA v1.0 ---")

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
    final_summary_text = "Resumo não gerado."

    # ==========================================
    # PASSO 1: Análise do PDF (Com Timer)
    # ==========================================
    logger.info("Iniciando Análise de Metadados...")
    
    start_time_meta = time.time() # Inicia cronômetro
    
    try:
        final_pdf_info = extract_pdf_info(pdf_path)
        
        # Para o cronômetro
        elapsed_meta = time.time() - start_time_meta
        logger.info(f"Análise de Metadados concluída em {elapsed_meta:.2f} segundos.")
        
        tamanho_humano = format_bytes(final_pdf_info.get('filesize_bytes', 0))

        # EXIBIÇÃO
        print("\n")
        print_box("RELATÓRIO DE ANÁLISE ESTATÍSTICA")
        print(f" [DADOS GERAIS] (Tempo de processamento: {elapsed_meta:.2f}s)")
        print(f"   {'Arquivo':<15} : {final_pdf_info.get('filename')}")
        print(f"   {'Tamanho':<15} : {tamanho_humano}")
        print(f"   {'Páginas':<15} : {final_pdf_info.get('num_pages')}")
        print(f"   {'Total Palavras':<15} : {final_pdf_info.get('total_words')}")
        print(f"   {'Vocabulário':<15} : {final_pdf_info.get('vocab_size')} termos únicos")
        print("-" * 50)
        
        print(f" [TOP 10 TERMOS MAIS FREQUENTES]")
        for i, (word, count) in enumerate(final_pdf_info.get('top_10_words', []), 1):
            print(f"   {i:<2}. {word:<20} ({count})")
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
    # PASSO 3: Geração de Resumo IA (Com Timer e Tokens)
    # ==========================================
    if generate_summary:
        logger.info("Iniciando Geração de Resumo com IA Local...")
        
        start_time_llm = time.time() # Inicia cronômetro da IA

        try:
            reader = PdfReader(pdf_path)
            full_text = ""
            for page in reader.pages:
                t = page.extract_text()
                if t: full_text += t + "\n"
            
            if not full_text.strip():
                logger.warning("PDF sem texto detectável para resumo.")
            else:
                # Chama a IA e recebe o dicionário com texto + métricas
                result_ia = generate_summary(full_text)
                
                # Para cronômetro
                elapsed_llm = time.time() - start_time_llm
                
                # Extrai os dados
                final_summary_text = result_ia.get("text", "")
                usage = result_ia.get("usage", {})
                
                # LOGS PROFISSIONAIS DE PERFORMANCE
                logger.info(f"Resumo gerado com sucesso em {elapsed_llm:.2f} segundos.")
                if usage:
                    logger.info(f"Métricas LLM: Entrada={usage.get('input_tokens')} tokens | "
                                f"Saída={usage.get('output_tokens')} tokens | "
                                f"Total={usage.get('total_tokens')} tokens")

                print("\n")
                print_box("RESUMO INTELIGENTE (IA)")
                print(final_summary_text)
                print(f"\n[Performance: {elapsed_llm:.2f}s | Tokens: {usage.get('total_tokens', '?')}]")
                print("=" * 60 + "\n")
        
        except Exception as e:
            logger.error(f"Falha na geração do resumo: {e}")
            final_summary_text = f"Erro ao gerar resumo: {e}"

    # ==========================================
    # Relatório Unificado
    # ==========================================
    logger.info("Gerando Relatório Final Unificado...")
    project_root = os.path.dirname(current_dir)
    
    # Passamos apenas o texto do resumo para o relatório
    report_file = save_markdown_report(final_pdf_info, final_summary_text, project_root)
    
    if report_file:
        logger.info(f"Relatório Markdown salvo em: {report_file}")
    else:
        logger.error("Falha ao salvar relatório Markdown.")

if __name__ == "__main__":
    main()