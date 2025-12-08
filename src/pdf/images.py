import os
from pypdf import PdfReader

def extract_images_from_pdf(pdf_path: str, output_dir: str) -> int:
    """
    Extrai imagens salvando-as no diretório especificado.
    Gera nomes simples e legíveis (Ex: pagina_1_img_1.jpg).
    """
    
    # Cria o diretório se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    reader = PdfReader(pdf_path)
    total_count = 0

    for page_num, page in enumerate(reader.pages):
        # Verifica se existem imagens na página
        if hasattr(page, 'images') and page.images:
            for img_index, image_file in enumerate(page.images):
                
                # Tenta descobrir a extensão original (.jpg, .png, etc)
                # O image_file.name geralmente traz algo como "Im1.jpg"
                filename = image_file.name
                ext = os.path.splitext(filename)[1]
                
                # Se por acaso não tiver extensão, definimos um padrão
                if not ext:
                    ext = ".jpg"
                
              
                unique_name = f"pagina_{page_num+1:02d}_img_{img_index+1:02d}{ext}"
                
                save_path = os.path.join(output_dir, unique_name)
                
                with open(save_path, "wb") as fp:
                    fp.write(image_file.data)
                
                total_count += 1
    
    return total_count