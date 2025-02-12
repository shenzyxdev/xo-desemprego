
print("Iniciando o teste...")

import requests
from bs4 import BeautifulSoup

print("Testando as bibliotecas...")

url = "https://www.terra.com.br"
resposta = requests.get(url)

if resposta.status_code == 200:
    print("Página carregada com sucesso!")
    soup = BeautifulSoup(resposta.text, "html.parser")
    print(soup.title)
else:
    print(f"Erro ao acessar a página (Status: {resposta.status_code})")