import torch
from transformers import pipeline

def generate_summary(text):
    """
    Gera um resumo do texto fornecido usando um modelo LLM local.
    Atende aos requisitos de execução local e uso de Hugging Face.
    """
    print("\n   [IA] Carregando modelo LLM local... (Isso pode demorar na primeira vez)")
    
    # Modelo sugerido: Qwen (leve e eficiente para CPU)
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    
    try:
        # Configura o pipeline de geração de texto
        # device_map="auto" usa GPU se tiver, ou CPU se não tiver
        pipe = pipeline(
            "text-generation",
            model=model_id,
            torch_dtype=torch.float32, # float32 é mais compatível com CPUs comuns
            device_map="auto"
        )

        # PREPARAÇÃO DO TEXTO
        # Modelos locais pequenos têm limite de tamanho (contexto).
        # Vamos pegar os primeiros 3000 caracteres para resumir a introdução/corpo principal.
        limit_chars = 3000
        text_chunk = text[:limit_chars]

        # Prompt (Instrução para a IA)
        messages = [
            {"role": "system", "content": "Você é um assistente útil que resume textos em português."},
            {"role": "user", "content": f"Resuma o seguinte texto em um parágrafo conciso:\n\n{text_chunk}"}
        ]

        # Geração da resposta
        outputs = pipe(
            messages,
            max_new_tokens=400, # Tamanho máximo da resposta
            do_sample=False     # Resposta mais direta e consistente
        )

        # Extrai apenas o texto gerado
        summary_text = outputs[0]["generated_text"][-1]["content"]
        
        return summary_text

    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"