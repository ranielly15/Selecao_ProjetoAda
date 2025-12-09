import torch
from transformers import pipeline

def generate_summary(text):
    """
    Gera resumo e calcula métricas de uso (tokens).
    Retorna um dicionário com: texto, tokens_entrada, tokens_saida.
    """
    print("\n   [IA] Carregando modelo LLM local... (Aguarde)")
    
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    
    try:
        # Carrega o pipeline
        pipe = pipeline(
            "text-generation",
            model=model_id,
            torch_dtype=torch.float32,
            device_map="auto"
        )

        # 1. Preparação do Texto e Prompt
        limit_chars = 3000
        text_chunk = text[:limit_chars]

        messages = [
            {"role": "system", "content": "Você é um assistente útil que resume textos em português."},
            {"role": "user", "content": f"Resuma o seguinte texto em um parágrafo conciso:\n\n{text_chunk}"}
        ]

        # 2. Contagem de Tokens de ENTRADA (Prompt + Texto)
        # O tokenizer transforma o texto em números que o modelo entende
        input_tokens = len(pipe.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True))

        # 3. Geração
        outputs = pipe(
            messages,
            max_new_tokens=400,
            do_sample=False
        )
        
        summary_text = outputs[0]["generated_text"][-1]["content"]

        # 4. Contagem de Tokens de SAÍDA (O resumo gerado)
        output_tokens = len(pipe.tokenizer.encode(summary_text))

        # Retorna tudo num dicionário
        return {
            "text": summary_text,
            "usage": {
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens
            }
        }

    except Exception as e:
        return {"text": f"Erro na IA: {str(e)}", "usage": {}}