import requests
from bs4 import BeautifulSoup
import re

print("Iniciando a execução do buscador de emails...")

# Lista de sites para buscar emails
urls = [
    "https://brasiliaempregos.com.br/vagas/", 
    "https://www.horadoempregodf.com.br/",
    "https://www.vagasbsb.com.br/search/label/Vagas?&max-results=8",
    "https://www.vagasbsb.com.br/2025/02/bonagrao-esta-com-diversas.html"
]

# Expressão regular ajustada para capturar apenas emails válidos
padrao_email = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?=\s|$)"

# Conjunto global para armazenar os emails únicos
emails_unicos = set()

# Função para buscar emails em uma página
def buscar_emails(url):
    try:
        print(f"Acessando {url}...")  # Verificar se a URL está sendo acessada
        resposta = requests.get(url, timeout=5)
        
        if resposta.status_code == 200:
            print(f"Página {url} carregada com sucesso!")
            soup = BeautifulSoup(resposta.text, "html.parser")
            texto = soup.get_text()
            emails = re.findall(padrao_email, texto)
            print(f"Emails encontrados: {emails}")  # Mostrar emails encontrados
            return set(emails)  # Remove duplicatas temporárias
        else:
            print(f"Erro ao acessar {url} (Status: {resposta.status_code})")
            return set()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return set()

# Função para buscar vagas por palavra-chave
def buscar_vagas_com_palavra_chave(url, palavras_chave):
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, "html.parser")
            vagas = soup.find_all("a", href=True)  # Encontrar todos os links das vagas
            for vaga in vagas:
                vaga_url = vaga['href']
                if any(palavra in vaga_url.lower() for palavra in palavras_chave):  # Verifica se a palavra-chave está no link
                    print(f"Vaga encontrada: {vaga_url}")
                    emails = buscar_emails(vaga_url)
                    if emails:
                        # Remover o email de contato@brasiliaempregos.com.br da lista de emails
                        emails.discard('contato@brasiliaempregos.com.br')
                        print(f"Emails encontrados na vaga {vaga_url}: {emails}")
                        salvar_emails(emails)
                else:
                    print(f"Vaga ignorada: {vaga_url}")
            return True
        else:
            print(f"Erro ao acessar {url} (Status: {resposta.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return False

# Função para salvar emails em um arquivo
def salvar_emails(emails):
    global emails_unicos  # Usar o conjunto global
    emails_unicos.update(emails)  # Adiciona os novos emails ao conjunto global sem duplicatas

    # Salvar os emails únicos no arquivo
    with open("emails_rh.txt", "w") as f:
        for email in emails_unicos:
            f.write(email + "\n")
    print(f"Emails salvos com sucesso!")

# Função para navegar entre as páginas
def navegar_pelas_paginas(url_base, palavras_chave):
    pagina = 1
    while True:
        print(f"Acessando página {pagina}...")
        url = f"{url_base}?page={pagina}"
        encontrou_vagas = buscar_vagas_com_palavra_chave(url, palavras_chave)
        if not encontrou_vagas:
            print("Nenhuma vaga encontrada nesta página.")
            break
        pagina += 1  # Avança para a próxima página

# URL base para começar a busca
url_base = "https://brasiliaempregos.com.br/vagas/"
palavras_chave = ["python", "desenvolvedor", "fullstack", "TI", "informática", "programador", "Auxiliar de Serviços Gerais", "tecnico"]

# Começar a navegar pelas páginas e buscar as vagas
navegar_pelas_paginas(url_base, palavras_chave)
