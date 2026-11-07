import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

class CipherAuditEngine:
    """Motor de Inferência Híbrido focado em Auditoria e Saída JSON."""
    
    def __init__(self, mode='web'):
        self.mode = mode.lower()
        if self.mode == 'cli':
            self._init_local()
        elif self.mode == 'web':
            self._init_cloud()
        else:
            raise ValueError("Modo inválido. Use 'cli' ou 'web'.")

    def _init_local(self):
        import ollama
        try:
            ollama.list()
            print("✅ [CLI] Conectado ao Ollama local.")
        except Exception as e:
            raise ConnectionError("Ollama não está rodando. Execute 'ollama serve'.")

    def _init_cloud(self):
        from groq import Groq
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY não encontrada no .env")
        self.client = Groq(api_key=api_key)
        print("✅ [WEB] Conectado à Groq API (Modelo: openai/gpt-oss-120b).")

    def audit(self, file_content, system_prompt, filename="config"):
        """Realiza a auditoria e retorna os dados estruturados."""
        user_prompt = f"Arquivo analisado: {filename}\n\nConteúdo:\n{file_content}\n\nRetorne APENAS o JSON de auditoria conforme as regras."
        
        if self.mode == 'cli':
            return self._generate_local(user_prompt, system_prompt)
        else:
            return self._generate_cloud(user_prompt, system_prompt)

    def _generate_local(self, user_prompt, system_prompt):
        import ollama
        response = ollama.chat(
            model='qwen2.5:1.5b',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": 0.0, "num_ctx": 2048} # Temperatura 0 para máxima consistência JSON
        )
        return self._clean_json(response['message']['content'])

    def _generate_cloud(self, user_prompt, system_prompt):
        response = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0, # Temperatura 0 para forçar JSON estrito
            response_format={"type": "json_object"} # Força a API a retornar JSON válido
        )
        return self._clean_json(response.choices[0].message.content)

    def _clean_json(self, raw_text):
        """Limpa markdown (```json) e converte para lista Python."""
        # Remove blocos de código markdown se a IA insistir em colocá-los
        clean_text = re.sub(r'^```json\s*', '', raw_text, flags=re.IGNORECASE)
        clean_text = re.sub(r'\s*```$', '', clean_text, flags=re.IGNORECASE)
        clean_text = clean_text.strip()
        
        try:
            data = json.loads(clean_text)
            # Garante que seja uma lista, mesmo que a IA retorne um objeto único
            if isinstance(data, dict):
                return [data]
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"Falha ao parsear JSON da IA: {e}\nTexto recebido: {clean_text}")
