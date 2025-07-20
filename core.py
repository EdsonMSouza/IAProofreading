import pandas as pd
from llm import AvaliadorIA

class AvaliadorPlanilha:
    def __init__(self, arquivo_entrada: str, arquivo_saida: str, modelo: str, tokens: int, temperature: float, url: str):
        self.arquivo_entrada = arquivo_entrada
        self.arquivo_saida = arquivo_saida
        self.avaliador = AvaliadorIA(modelo=modelo, tokens=tokens, temperature=temperature, url=url)

    def executar(self):
        # Carrega os dados da planilha
        df = pd.read_excel(self.arquivo_entrada)

        # Evita conflito com a coluna "Resposta"
        if "Resposta" in df.columns:
            df = df.rename(columns={"Resposta": "Resposta_Original"})

        # Extrai colunas que contêm as questões (todas exceto Carimbo de data/hora, email e nome)
        colunas_questoes = [col for col in df.columns if col not in ["Carimbo de data/hora", "Endereço de e-mail", "Nome"]]

        # Transforma a planilha no formato longo (cada linha = 1 resposta)
        df_transformado = df.melt(
            id_vars=["Carimbo de data/hora", "Endereço de e-mail", "Nome"],
            value_vars=colunas_questoes,
            var_name="Pergunta",
            value_name="Resposta"
        )

        # Avaliação das respostas
        feedbacks, notas = [], []

        for idx, row in df_transformado.iterrows():
            pergunta = row["Pergunta"]
            resposta = str(row["Resposta"]) if pd.notna(row["Resposta"]) else ""

            print(f"🔍 Avaliação da resposta {idx + 1}/{len(df_transformado)}", end=" ")

            try:
                if resposta.strip():
                    resultado = self.avaliador.avaliar(pergunta, resposta, self.avaliador.tokens, self.avaliador.temperature)
                else:
                    resultado = {"feedback": "Sem resposta.", "nota": 0}
            except Exception as e:
                print(f"❌ Erro ao avaliar a linha {idx + 1}: {e}")
                resultado = {"feedback": "Erro na avaliação.", "nota": 0}

            feedbacks.append(resultado["feedback"])
            notas.append(resultado["nota"])
            
        # Adiciona os resultados ao DataFrame transformado
        df_transformado["Feedback"] = feedbacks
        df_transformado["Nota"] = notas

        # Salva o DataFrame resultante em um novo arquivo
        df_transformado.to_excel(self.arquivo_saida, index=False)
        print("✅ Avaliações concluídas.")
        print(f"💾 Arquivo salvo como: {self.arquivo_saida}")
