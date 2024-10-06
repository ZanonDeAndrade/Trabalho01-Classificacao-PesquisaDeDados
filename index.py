from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import json
import time

# Configuração do Selenium para usar o Chrome
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico)

# Acessa o site da Epic Games
driver.get("https://www.epicgames.com/store/en-US/browse?sortBy=releaseDate&sortDir=DESC&count=40")
time.sleep(5)  # Espera para garantir que a página carregue completamente

# Encontra todos os scripts na página
scripts = driver.find_elements(By.TAG_NAME, 'script')

# Filtra o script que contém os dados de preços
dados = None
for script in scripts:
    conteudo_script = script.get_attribute('innerHTML')
    if 'currencyList' in conteudo_script:  # Ajuste aqui para capturar 'currencyList'
        dados = conteudo_script
        break

# Se dados foram encontrados
if dados:
    # Refinar a regex para capturar o bloco de JSON que contém 'currencyList' e fechar corretamente o bloco
    precos_json = re.search(r'\{"currencyList":.*\}\]}', dados, re.DOTALL)

    if precos_json:
        # Pega o texto do JSON encontrado
        dados_limpos = precos_json.group(0)

        try:
            # Converte o texto JSON em dicionário Python
            precos_dicionario = json.loads(dados_limpos)

            # Lista para armazenar preços
            precos = []

            # Extrai os preços por moeda
            for moeda in precos_dicionario['currencyList']:
                for tier in moeda['tierList']:
                    # Adiciona o preço à lista
                    precos.append(float(tier['price']))

            # Função para Selection Sort
            def selection_sort(prices):
                n = len(prices)
                for i in range(n):
                    min_index = i
                    for j in range(i + 1, n):
                        if prices[j] < prices[min_index]:
                            min_index = j
                    prices[i], prices[min_index] = prices[min_index], prices[i]

            # Ordena os preços
            selection_sort(precos)

            # Exibe os preços ordenados
            print("Preços ordenados:")
            print(precos)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            print(dados_limpos)  # Imprime o conteúdo capturado para ajudar no diagnóstico
    else:
        print("Não foi possível encontrar um bloco JSON válido contendo 'currencyList'.")
else:
    print("Script contendo os dados não encontrado.")

# Fecha o navegador
driver.quit()
