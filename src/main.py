import os
import sys
from pypdf import PdfReader # Necessário para ler o texto completo para a IA

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from pdf.extractor import extract_pdf_info
from pdf.images import extract_images_from_pdf
from llm.summarize import generate_summary # Importando nosso novo módulo
from cli.arguments import get_arguments

def main() -> None:
    args = get_arguments()
    
    print("--- Iniciando Processamento ADA ---")

    # --- Definição do Arquivo ---
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
        print(f"[ERRO CRÍTICO] Arquivo não encontrado: {pdf_path}")
        return

    print(f"Processando arquivo: {pdf_path}")

    # ==========================================
    # PASSO 1: Análise do PDF (Metadados)
    # ==========================================
    print("\n--- 1. Análise do PDF ---")
    try:
        pdf_info = extract_pdf_info(pdf_path)
        
        print(f"Arquivo: {pdf_info.get('filename')}")
        print(f"Número total de páginas: {pdf_info.get('num_pages')}")
        print(f"Número total de palavras: {pdf_info.get('total_words')}")
        print(f"Tamanho do arquivo: {pdf_info.get('filesize_bytes')} bytes")
        print(f"Tamanho do vocabulário: {pdf_info.get('vocab_size')}")
        
        print("\nLista das 10 palavras mais comuns:")
        for p, q in pdf_info.get('top_10_words', []):
            print(f"   - {p}: {q}")
            
    except Exception as e:
        print(f"[ERRO] Metadados: {e}")

    # ==========================================
    # PASSO 2: Extração de Imagens
    # ==========================================
    print("\n--- 2. Extração de Imagens ---")
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
        print(f"[SUCESSO] {qtd} imagens salvas.")
        print(f"          Local: {final_output_dir}")

    except Exception as e:
        print(f"[ERRO] Imagens: {e}")

    # ==========================================
    # PASSO 3: Geração de Resumo (LLM Local)
    # ==========================================
    print("\n--- 3. Geração de Resumo (LLM Local) ---")
    try:
        # 1. Extrair texto bruto para a IA ler
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t: full_text += t + "\n"
        
        if not full_text.strip():
            print("[AVISO] PDF sem texto detectável para resumo.")
        else:
            # 2. Gerar Resumo
            resumo = generate_summary(full_text)
            
            # 3. Imprimir na saída padrão (Requisito Obrigatório)
            print("\n" + "="*50)
            print("RESUMO DO DOCUMENTO:")
            print("="*50)
            print(resumo)
            print("="*50)

            # 4. Salvar em arquivo .txt (Requisito Opcional/Pontos Extras)
            # Salva na raiz do projeto
            output_file = os.path.join(project_root, f"resumo_{pdf_name_no_ext}.txt")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"Resumo do arquivo: {pdf_filename}\n\n{resumo}")
            
            print(f"\n[INFO] Resumo salvo em arquivo: {output_file}")

    except Exception as e:
        print(f"[ERRO] Falha na geração do resumo: {e}")

if __name__ == "__main__":
    main()