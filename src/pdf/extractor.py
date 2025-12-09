import os
import re
from collections import Counter
from pypdf import PdfReader

def normalize_word(word):
    """
    Reduz a palavra ao singular (Lematização manual).
    Usado apenas para o cálculo do Vocabulário e Top 10.
    """
    # Regras de singularização do português
    if word.endswith('oes'):
        return word[:-3] + 'ao'
    elif word.endswith('res'):
        return word[:-2]
    elif word.endswith('s') and not word.endswith('ss'):
        return word[:-1]
    return word

def extract_pdf_info(pdf_path):
    info = {
        'filename': os.path.basename(pdf_path),
        'filesize_bytes': 0,
        'num_pages': 0,
        'total_words': 0,  # Contagem BRUTA
        'top_10_words': [], # Baseado na contagem LIMPA
        'vocab_size': 0     # Baseado na contagem LIMPA
    }

    try:
        # 1. Tamanho em bytes
        if os.path.exists(pdf_path):
            info['filesize_bytes'] = os.path.getsize(pdf_path)

        # 2. Leitura do PDF
        reader = PdfReader(pdf_path)
        info['num_pages'] = len(reader.pages)

        # 3. Extração do Texto
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + " "

        # 4. Tokenização (Quebrar texto em palavras)
        # Regex captura palavras com acentos, ignorando pontuação (. , ! ?)
        raw_words = re.findall(r'\b[a-zA-ZáàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ]+\b', full_text.lower())

        # --- CORREÇÃO AQUI ---
        # Total de palavras conta TUDO (incluindo 'a', 'de', 'o', repetidas, etc)
        info['total_words'] = len(raw_words)

        # 5. Processamento para Vocabulário (Limpeza + Normalização)
        stopwords = {
            'a', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas',
            'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 'nos', 'nas',
            'e', 'ou', 'que', 'se', 'por', 'para', 'com', 'sem', 'sob',
            'ao', 'aos', 'pelo', 'pela', 'pelos', 'pelas', 'ante', 'até',
            'é', 'são', 'foi', 'foram', 'era', 'eram', 'ser', 'sendo',
            'está', 'estão', 'esteve', 'estava', 'estavam',
            'tem', 'têm', 'tinha', 'tinham', 'ter', 'tido',
            'há', 'havia', 'houve', 'vai', 'vão', 'ir', 'pode', 'podem',
            'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
            'meu', 'minha', 'seu', 'sua', 'nosso', 'nossa',
            'este', 'esta', 'esse', 'essa', 'aquele', 'aquela', 'isso', 'isto', 'aquilo',
            'qual', 'quais', 'quem', 'onde', 'como', 'quando', 'quanto',
            'mas', 'porém', 'todavia', 'entretanto', 'portanto', 'pois', 'então', 'assim',
            'muito', 'muita', 'muitos', 'muitas',
            'pouco', 'pouca', 'poucos', 'poucas',
            'todo', 'toda', 'todos', 'todas', 'tudo',
            'outro', 'outra', 'outros', 'outras',
            'algum', 'alguma', 'alguns', 'algumas',
            'cada', 'vários', 'várias',
            'apenas', 'somente', 'só', 'tão',
            'vez', 'vezes', 'geral', 'caso', 'tipo', 'forma', 'exemplo',
            'sobre', 'entre', 'através', 'durante', 'após', 'antes', 'depois',
            'agora', 'ainda', 'já', 'mais', 'menos', 'bem', 'mal' , 'não', 'sim'
        }

        clean_vocab_list = []
        for w in raw_words:
            # Ignora stopwords iniciais e palavras muito curtas
            if w in stopwords or len(w) < 2:
                continue
            
            # Aplica a normalização ("lemming")
            normalized = normalize_word(w)
            
            # Verifica de novo se a palavra normalizada não virou uma stopword
            if normalized not in stopwords and len(normalized) > 1:
                clean_vocab_list.append(normalized)

        # Estatísticas do Vocabulário Limpo
        word_counts = Counter(clean_vocab_list)
        
        info['top_10_words'] = word_counts.most_common(10)
        info['vocab_size'] = len(word_counts) # Conta palavras DISTINTAS e NORMALIZADAS

    except Exception as e:
        print(f"Erro no extrator de texto: {e}")
        
    return info