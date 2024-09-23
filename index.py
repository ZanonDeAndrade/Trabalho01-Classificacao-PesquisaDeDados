import requests
from bs4 import BeautifulSoup

url = 'https://store.epicgames.com/pt-BR/'

def buscar_dados(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    produtos = []
    for item in soup.find_all('div', class_='nome_da_classe_do_produto'):
        nome = item.find('h2').text
        preco = item.find('span', class_='preco').text
        produtos.append((nome, float(preco.replace('$', ''))))
    
    return produtos

def selection_sort(lista):
    for i in range(len(lista)):
        min_idx = i
        for j in range(i+1, len(lista)):
            if lista[j][1] < lista[min_idx][1]:
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
    return lista

def main():
    produtos = buscar_dados(url)
    produtos_ordenados = selection_sort(produtos)
    
    for produto in produtos_ordenados:
        print(f'{produto[0]}: ${produto[1]:.2f}')

if __name__ == "__main__":
    main()
