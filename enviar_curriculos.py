import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Função para enviar o email
def enviar_email(destinatario, assunto, corpo, anexo_path):
    remetente = "pessoalluiz15@gmail.com"  # Substitua pelo seu email
    senha = "arxx cgvw mwhj bmwx"  # Substitua pela sua senha do email (pode ser necessário gerar uma senha específica para apps no Gmail)
    
    # Configuração do servidor SMTP
    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()  # Ativa a criptografia
    servidor.login(remetente, senha)
    
    # Construir a mensagem
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = assunto
    
    # Adicionar o corpo do email
    corpo_email = MIMEText(corpo, "plain")  # Corpo como texto simples
    msg.attach(corpo_email)
    
    # Adicionar o arquivo de currículo
    try:
        with open(anexo_path, "rb") as arquivo:
            anexo = MIMEBase("application", "octet-stream")
            anexo.set_payload(arquivo.read())
        encoders.encode_base64(anexo)
        anexo.add_header("Content-Disposition", f"attachment; filename={anexo_path.split('/')[-1]}")  # Extraí o nome do arquivo
        msg.attach(anexo)
    except FileNotFoundError:
        print(f"Erro: O arquivo {anexo_path} não foi encontrado.")
        return
    
    # Enviar o email
    try:
        servidor.sendmail(remetente, destinatario, msg.as_string())
        print(f"Currículo enviado para: {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar o e-mail para {destinatario}: {e}")
    finally:
        servidor.quit()

# Carregar emails de RH
with open("emails_rh.txt", "r") as f:
    emails = [linha.strip() for linha in f.readlines()]

# Enviar o currículo para todos os emails
assunto = "Currículo para vaga de RH"
corpo_email = "Olá, estou interessado na vaga de RH. Em anexo está o meu currículo."
anexo_path = "C:\\Users\\xtrem\\Desktop\\luiz borges.pdf"  # Substitua pelo caminho do seu currículo

for email in emails:
    enviar_email(email, assunto, corpo_email, anexo_path)

print("Todos os currículos foram enviados!")
