import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import json
import time
import heapq

# Função para salvar blocos temporários em arquivos
def salvar_bloco(bloco, nome_arquivo):
    with open(nome_arquivo, 'w') as f:
        for preco in bloco:
            f.write(f"{preco}\n")

# Função para carregar blocos de um arquivo
def carregar_bloco(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        return [float(linha.strip()) for linha in f]

# Função para fazer o merge dos blocos ordenados (arquivos temporários)
def merge_arquivos(arquivos_temp):
    min_heap = []
    handlers = []

    # Abrir cada arquivo temporário e inicializar o heap
    for nome_arquivo in arquivos_temp:
        f = open(nome_arquivo, 'r')
        handlers.append(f)
        preco = float(f.readline().strip())
        # Adiciona a tupla (preço, índice do arquivo) no heap, com o preço como chave de comparação
        heapq.heappush(min_heap, (preco, len(handlers) - 1))

    # Lista final ordenada
    precos_ordenados = []

    while min_heap:
        # Pega o menor preço do heap
        menor, index = heapq.heappop(min_heap)
        precos_ordenados.append(menor)

        # Pega o próximo valor do mesmo arquivo
        f = handlers[index]
        linha = f.readline().strip()
        if linha:
            heapq.heappush(min_heap, (float(linha), index))

    # Fecha os arquivos temporários
    for f in handlers:
        f.close()

    return precos_ordenados

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
    if 'currencyList' in conteudo_script:
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

            # Dividir os preços em blocos menores e salvar em arquivos temporários
            tamanho_bloco = 10  # Escolha o tamanho apropriado dos blocos com base na memória disponível
            arquivos_temp = []

            for i in range(0, len(precos), tamanho_bloco):
                bloco = precos[i:i + tamanho_bloco]
                bloco.sort()  # Ordena o bloco na memória
                nome_arquivo_temp = f"temp_{i}.txt"
                salvar_bloco(bloco, nome_arquivo_temp)
                arquivos_temp.append(nome_arquivo_temp)

            # Faz o merge dos arquivos temporários
            precos_ordenados = merge_arquivos(arquivos_temp)

            # Exibe os preços ordenados
            print("Preços ordenados:")
            print(precos_ordenados)

            # Limpa os arquivos temporários
            for arquivo in arquivos_temp:
                os.remove(arquivo)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
            print(dados_limpos)  # Imprime o conteúdo capturado para ajudar no diagnóstico
    else:
        print("Não foi possível encontrar um bloco JSON válido contendo 'currencyList'.")
else:
    print("Script contendo os dados não encontrado.")

# Fecha o navegador
driver.quit()
