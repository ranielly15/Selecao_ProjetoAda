import os
import sys
from pypdf import PdfReader

# Ajuste de path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from pdf.extractor import extract_pdf_info
from pdf.images import extract_images_from_pdf
from cli.arguments import get_arguments
from utils.logger import setup_logger # Importando nossa nova ferramenta

# Tenta importar IA
try:
    from llm.summarize import generate_summary
except ImportError:
    generate_summary = None

# Inicializa o Logger (substitui os prints do sistema)
logger = setup_logger()

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

    # ==========================================
    # PASSO 1: Análise do PDF
    # ==========================================
    logger.info("Iniciando Análise de Metadados...")
    try:
        pdf_info = extract_pdf_info(pdf_path)
        
        # Usamos logger para fluxo, mas print para exibir os DADOS finais ao usuário
        print("\n" + "-"*30)
        print("RESULTADOS DA ANÁLISE:")
        print(f"Arquivo: {pdf_info.get('filename')}")
        print(f"Páginas: {pdf_info.get('num_pages')}")
        print(f"Palavras Totais: {pdf_info.get('total_words')}")
        print(f"Bytes: {pdf_info.get('filesize_bytes')}")
        print(f"Vocabulário: {pdf_info.get('vocab_size')}")
        print("-" * 30 + "\n")
        
        print("Top 10 Palavras:")
        for p, q in pdf_info.get('top_10_words', []):
            print(f"   - {p}: {q}")
            
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
                
                print("\n" + "="*50)
                print("RESUMO IA:")
                print(final_summary)
                print("="*50 + "\n")

                # Salva TXT simples
                output_file = os.path.join(project_root, f"resumo_{pdf_name_no_ext}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(f"Resumo do arquivo: {pdf_filename}\n\n{final_summary}")
                logger.info(f"Resumo salvo em arquivo: {output_file}")

        except Exception as e:
            logger.error(f"Falha na geração do resumo: {e}")

if __name__ == "__main__":
    main()