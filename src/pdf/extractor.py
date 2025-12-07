import fitz  # PyMuPDF
import os
import re
from collections import Counter
from typing import Dict, Any, List, Set

def extract_pdf_info(pdf_path: str) -> Dict[str, Any]:
    """
    Extrai metadados estruturais e estatísticas textuais de um arquivo PDF.

    Args:
        pdf_path (str): Caminho absoluto ou relativo para o arquivo PDF.

    Returns:
        Dict[str, Any]: Dicionário contendo:
            - num_pages (int): Total de páginas.
            - file_size_bytes (int): Tamanho do arquivo em bytes.
            - text_content (str): Texto completo extraído (bruto).
            - total_words (int): Contagem total de palavras.
            - vocab_size (int): Quantidade de palavras únicas (vocabulário).
            - top_10_words (List[Tuple]): Lista das 10 palavras mais frequentes.
            - erro (str, optional): Mensagem de erro caso a leitura falhe.
    """
    # Validação de existência do arquivo antes de tentar abrir
    if not os.path.exists(pdf_path):
        return {"erro": f"Arquivo não encontrado: {pdf_path}"}

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        return {"erro": f"Falha ao abrir PDF: {str(e)}"}

    info: Dict[str, Any] = {
        "num_pages": len(doc),
        "file_size_bytes": os.path.getsize(pdf_path),
        "text_content": ""
    }

    # Extração de texto (Iteração otimizada)
    full_text_list = [page.get_text() for page in doc]
    full_text = "".join(full_text_list)
    info["text_content"] = full_text

    # Processamento de NLP básico (Tokenização e Limpeza)
    # Regex para capturar palavras inteiras, ignorando pontuação
    raw_words = re.findall(r'\b\w+\b', full_text.lower())
    
    # Stopwords (palavras funcionais sem carga semântica relevante)
    stopwords: Set[str] = {
        'a', 'e', 'o', 'as', 'os', 'de', 'do', 'da', 'dos', 'das', 
        'em', 'no', 'na', 'nos', 'nas', 'um', 'uma', 'uns', 'umas', 
        'por', 'para', 'com', 'que', 'se', 'é', 'foi', 'são', 'não',
        'como', 'mais', 'pela', 'pelo'
    }

    # Filtragem: remove stopwords e palavras curtas (< 3 caracteres)
    valid_words = [w for w in raw_words if w not in stopwords and len(w) > 2]

    # Cálculo de estatísticas
    info["total_words"] = len(raw_words)
    info["vocab_size"] = len(set(valid_words))
    info["top_10_words"] = Counter(valid_words).most_common(10)

    doc.close()
    return info

if __name__ == "__main__":
    print("Módulo extractor.py configurado.")