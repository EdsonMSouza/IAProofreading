import sys
import os
from core import AvaliadorPlanilha

def main():
    # Verifica se o arquivo de entrada foi passado como argumento
    if len(sys.argv) < 2:
        print("Uso: python avaliar.py data\<respostas_simuladas.xlsx>")
        sys.exit(1)

    # Arquivo de entrada passado como argumento na linha de comando
    nome_arquivo_entrada = sys.argv[1]

    avaliador = AvaliadorPlanilha(
        arquivo_entrada=nome_arquivo_entrada,
        arquivo_saida=f"{os.path.splitext(nome_arquivo_entrada)[0]}_avaliado.xlsx",
        modelo= "qwen2.5-7b-instruct-1m",  # Verifique os modelos disponíveis no LM Studio
        tokens=1000,
        temperature=0.1,
        url="http://localhost:1234/v1/chat/completions"
    )

    # Executa a avaliação com tratamento de exceções
    print(f"Avaliando o arquivo: {nome_arquivo_entrada}")
    try:
        avaliador.executar()
    except Exception as e:
        print("❌ Ocorreu um erro durante a execução da avaliação.")
        print("Detalhes do erro:", str(e))
        sys.exit(2)

# Ponto de entrada
if __name__ == "__main__":
    main()
