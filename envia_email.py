# Envia o e-mail com o resultado
import pandas as pd
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Envia e-mails com as avaliações para cada aluno
def enviar_email(df_transformado, email_coluna="Endereço de e-mail", smtp_server="smtp.gmail.com", smtp_port=587, remetente="", senha="", avaliacao=None):
    # Agrupar por email (um aluno por vez)
    alunos = df_transformado[email_coluna].unique()
    
    # Contador para as perguntas
    contador = 1

    for aluno in alunos:
         # Filtra as linhas do aluno pelo e-mail
        df_aluno = df_transformado[df_transformado[email_coluna] == aluno]
    
        # Tenta obter o nome correspondente àquele aluno (primeira ocorrência)
        nome = df_aluno["Nome"].iloc[0] if "Nome" in df_aluno.columns else "Aluno(a)"
        
        # Corpo do e-mail
        corpo = f"Prezado(a) {nome.upper()},<br><br>Segue abaixo a avaliação das suas respostas:<br><br>"
        soma_notas = 0

        for _, linha in df_aluno.iterrows():
            pergunta = str(linha['Pergunta']).replace("\n", " ").strip()
            resposta = str(linha['Resposta']).replace("\n", " ").strip()
            feedback = str(linha['Feedback']).replace("\n", " ").strip()
            nota = linha['Nota'] if pd.notna(linha['Nota']) else 0
            soma_notas += nota

            corpo += (
                f"🟦 <b>Pergunta {contador}</b>: {pergunta}<br>"
                f"📝 <b>Resposta</b>: {resposta}<br>"
                f"💬 <b>Feedback</b>: {feedback}<br>"
                f"📊 <b>Nota</b>: {nota}/20<br><br><br>"
            )
            contador += 1

        corpo += f"🔢 <b>Nota da sua avaliação: {soma_notas}</b>/100<br><br>"
        corpo += "Atenciosamente,<br>Prof. Edson Melo de Souza<br>"

        # Monta o e-mail
        msg = MIMEMultipart()
        msg["From"] = remetente
        msg["To"] = aluno  
        msg["Subject"] = f"Avaliação das suas respostas - {avaliacao}"
        msg.attach(MIMEText(corpo, "html"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(remetente, senha)
                server.send_message(msg)
                print(f"E-mail enviado para {aluno}")
        except Exception as e:
            print(f"Erro ao enviar e-mail para {aluno}: {e}")

def main():
    # Verifica se o arquivo de entrada foi passado como argumento
    if len(sys.argv) < 2:
        print("Uso: python envia_email.py data/<respostas_simuladas.xlsx>")
        sys.exit(1)

    # Arquivo de entrada passado como argumento na linha de comando
    nome_arquivo_entrada = sys.argv[1]

    # Lê o arquivo Excel transformado
    df_transformado = pd.read_excel(nome_arquivo_entrada)

    enviar_email(
        df_transformado,
        email_coluna="Endereço de e-mail",
        remetente="prof.edson.melo@gmail.com",
        senha="ifquwmsiaoambaya", # senha do APP
        avaliacao="Teste de Correção por IA"
    )

# Ponto de entrada
if __name__ == "__main__":
    main()

# wanderleyjrr1@gmail.com