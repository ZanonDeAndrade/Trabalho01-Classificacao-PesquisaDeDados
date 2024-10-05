from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configurando o navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://store.epicgames.com/pt-BR/'
driver.get(url)

# Capturando o HTML da página renderizada
html = driver.page_source

# Agora você pode buscar pelos links no conteúdo capturado
import re
search = re.search(r'<a\s+href=["\'](https://[\w\-._/]+)["\']', html)

if search:
    print(search.group(1))  # Imprime o link encontrado
else:
    print("Nenhum link encontrado.")

driver.quit()
