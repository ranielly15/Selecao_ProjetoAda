import logging
import sys

def setup_logger():
    """
    Configura o logger para escrever no console e em arquivo.
    Atende ao requisito opcional: Uso de logs (arquivo ou console).
    """
    # Cria o logger com um nome específico
    logger = logging.getLogger("ProjetoADA")
    logger.setLevel(logging.INFO)

    # Evita duplicidade de logs se a função for chamada mais de uma vez
    if logger.handlers:
        return logger

    # Formato da mensagem (Hora - Nível - Mensagem)
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%H:%M:%S')

    # 1. Handler para Arquivo (salva o histórico em 'execucao.log')
    file_handler = logging.FileHandler("execucao.log", mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 2. Handler para Console (mostra na tela)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger