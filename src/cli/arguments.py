import argparse

def get_arguments():
    """
    Define e analisa os argumentos passados pela linha de comando.
    """
    parser = argparse.ArgumentParser(description="Ferramenta de Análise de PDF (Projeto ADA)")

    # Argumento para o arquivo de entrada (PDF)
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Caminho para o arquivo PDF a ser processado'
    )

    # Argumento para o diretório de saída das imagens 
    parser.add_argument(
        '--image_dir', '-d',
        type=str,
        help='Caminho do diretório onde as imagens extraídas serão salvas'
    )

    return parser.parse_args()