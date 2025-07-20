import requests
import ast
import re
import time

class AvaliadorIA:
    def __init__(self, modelo: str, tokens: int = 1000, temperature: float = 0.1, url: str = "http://localhost:1234/v1/chat/completions"):
        self.modelo = modelo
        self.tokens = tokens
        self.temperature = temperature
        self.url = url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer lm-studio"
        }

    def avaliar(self, pergunta: str, resposta: str, tokens: int, temperature: float) -> dict:
        messages = [
            {
                "role": "system",
                "content": (
                    "Você é um avaliador de respostas acadêmicas. "
                    "Forneça apenas um feedback objetivo e motivador seguido da nota de 0 a 20. "
                    "Formate a saída exatamente como JSON no estilo Python: {'feedback': '...', 'nota': ...}. "
                    "Não inclua comentários, explicações ou texto fora do dicionário."
                )
            },
            {
                "role": "user",
                "content": f"A resposta: {resposta} responde à pergunta: {pergunta}? Qual nota você atribui a essa resposta?"
            }
        ]

        payload = {
            "model": self.modelo,
            "messages": messages,
            "max_tokens": self.tokens,
            "temperature": self.temperature
        }

        try:
            inicio = time.time()
            response = requests.post(self.url, headers=self.headers, json=payload)
            fim = time.time()

            tempo_execucao = (fim - inicio)  # ms
            print(f" ({tempo_execucao:.3f} segundos)")

            content = response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print("Erro ao se comunicar com o modelo:", e)
            try:
                print("Resposta bruta:", response.text)
            except:
                pass
            return {"feedback": "Erro ao se comunicar com o modelo.", "nota": 0}

        return self._extrair_dados(content)

    def _extrair_dados(self, content: str) -> dict:
        try:
            parsed = ast.literal_eval(content)
            if isinstance(parsed, dict) and "feedback" in parsed and "nota" in parsed:
                return parsed
        except:
            pass

        match = re.search(r"\{[^{}]*['\"]feedback['\"].*?['\"]nota['\"].*?\}", content, re.DOTALL)
        if match:
            trecho = match.group()
            try:
                parsed = ast.literal_eval(trecho)
                if isinstance(parsed, dict) and "feedback" in parsed and "nota" in parsed:
                    return parsed
            except Exception as e:
                print("Erro ao interpretar o trecho extraído:", e)
                print("Trecho:", trecho)
                return {"feedback": "Erro ao interpretar a resposta.", "nota": 0}

        print("Nenhum dicionário válido foi encontrado.")
        print("Resposta bruta do modelo:\n", content)
        return {"feedback": "Resposta fora do padrão.", "nota": 0}
