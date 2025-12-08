import os
import re
from collections import Counter
from pypdf import PdfReader

def extract_pdf_info(pdf_path):
    info = {
        'filename': os.path.basename(pdf_path),
        'filesize_bytes': 0,
        'num_pages': 0,
        'total_words': 0,
        'top_10_words': [],
        'vocab_size': 0
    }

    try:
        # 1. Tamanho em bytes
        if os.path.exists(pdf_path):
            info['filesize_bytes'] = os.path.getsize(pdf_path)

        # 2. Leitura do PDF
        reader = PdfReader(pdf_path)
        info['num_pages'] = len(reader.pages)

        # 3. Processamento de Texto
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + " "

        # Limpeza e Tokenização
        words = re.findall(r'\b\w+\b', full_text.lower())

        stopwords = {
            'a', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas',
            'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas',
            'e', 'ou', 'que', 'se', 'por', 'para', 'com', 'não', 'ao', 'aos',
            'é', 'são', 'foi', 'pelo', 'pela', 'como', 'mais', 'mas', 'foi'
        }

        # Filtra stopwords e números
        filtered_words = [w for w in words if w not in stopwords and not w.isdigit() and len(w) > 1]

        # Estatísticas
        info['total_words'] = len(filtered_words)
        word_counts = Counter(filtered_words)
        info['top_10_words'] = word_counts.most_common(10)
        
        # Tamanho do vocabulário (palavras únicas)
        info['vocab_size'] = len(word_counts)

    except Exception as e:
        print(f"Erro no extrator de texto: {e}")
        
    return info