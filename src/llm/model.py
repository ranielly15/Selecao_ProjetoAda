import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class LLMLoader:
    """
    Classe responsável por carregar o modelo de linguagem (LLM) localmente.
    Utiliza a biblioteca Transformers da Hugging Face.
    """
    def __init__(self, model_id: str = "Qwen/Qwen2.5-0.5B-Instruct"):
        self.model_id = model_id
        self.pipeline = None
        self.tokenizer = None
        self.model = None

    def load_model(self):
        """
        Carrega o tokenizador e o modelo na memória.
        Detecta automaticamente se há GPU disponível ou usa CPU.
        """
        print(f"[INFO] Carregando modelo IA: {self.model_id}...")
        print("[INFO] Isso pode demorar na primeira vez (download)...")

        try:
            # Detecta dispositivo (placa de vídeo ou processador)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"[INFO] Dispositivo de processamento detectado: {device.upper()}")

            # Carrega o tokenizador (o tradutor de texto -> numeros)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)

            # Carrega o modelo (o cérebro)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                torch_dtype=torch.float32, # float32 é mais seguro para CPU
                device_map=device,
                low_cpu_mem_usage=True
            )

            # Cria o pipeline de geração de texto
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=500, # Tamanho máximo do resumo
                model_kwargs={"torch_dtype": torch.float32}
            )
            
            print("[SUCESSO] Modelo carregado com sucesso.")
            return self.pipeline

        except Exception as e:
            print(f"[ERRO CRITICO] Falha ao carregar modelo: {e}")
            return None