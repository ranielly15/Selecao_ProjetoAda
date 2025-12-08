from llm.model import LLMLoader

def generate_summary(text_content: str) -> str:
    """
    Recebe um texto bruto e retorna um resumo gerado por IA.
    """
    if not text_content:
        return "Erro: Texto vazio fornecido para resumo."

    # 1. Carregar a IA
    loader = LLMLoader()
    pipe = loader.load_model()

    if pipe is None:
        return "Erro: Não foi possível carregar o modelo de IA."

    # 2. Preparar o Prompt
    texto_para_analise = text_content[:2000] 

    messages = [
        {"role": "system", "content": "Você é um assistente especialista em resumir documentos técnicos em português do Brasil. Responda de forma direta e objetiva."},
        {"role": "user", "content": f"Faça um resumo detalhado dos principais pontos do seguinte texto:\n\n{texto_para_analise}"}
    ]

    print("[INFO] Gerando resumo... (Aguarde, processando)")

    # 3. Gerar a resposta
    try:
        outputs = pipe(
            messages,
            max_new_tokens=500,
            do_sample=False,
            temperature=0.1,
        )
        
        resumo = outputs[0]["generated_text"][-1]["content"]
        return resumo

    except Exception as e:
        return f"Erro na geração: {e}"