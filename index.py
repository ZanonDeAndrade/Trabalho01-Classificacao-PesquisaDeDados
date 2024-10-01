from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Configurando o WebDriver do Chrome com o WebDriver Manager (baixa automaticamente)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Abrir o site da Epic Games
url = "https://store.epicgames.com/pt-BR/browse?sortBy=releaseDate&sortDir=DESC&priceTier=tierDiscouted&category=Game&count=40"
driver.get(url)

# Esperar um tempo para garantir que a página e o JavaScript tenham carregado
time.sleep(5)

# Capturar o HTML da página carregada
html = driver.page_source

# Fechar o navegador
driver.quit()

# Usar BeautifulSoup para fazer o parsing do HTML
soup = BeautifulSoup(html, 'html.parser')

# Exemplo: Coletar nome e preço dos produtos (ajuste os seletores conforme necessário)
produtos = []
for item in soup.find_all('div', class_='css-1m0503p'):
    nome_produto = item.find('span', class_='css-2ucwu').text.strip()
    preco_produto = item.find('span', class_='css-1y1g2xn').text.strip().replace("R$", "").replace(",", ".")
    if nome_produto and preco_produto:
        produtos.append((nome_produto, float(preco_produto)))

# Exibir os produtos coletados
for produto in produtos:
    print(f"Nome: {produto[0]}, Preço: R$ {produto[1]:.2f}")
