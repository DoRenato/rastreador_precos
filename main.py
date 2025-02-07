import requests
import json
from bs4 import BeautifulSoup



def ler_site(url, salvar=True):
    """
    Vai buscar direto no site, o parametro salvar é para o caso de querer salvar
    o html do site em um arquivo dentro da pasta 'dados'.
    """
    get_nuuvem_promo_pc_page=requests.get(url).text
    if salvar:
        with open('dados/response_site.html','w',encoding='utf8') as f:
            f.write(get_nuuvem_promo_pc_page)
    return get_nuuvem_promo_pc_page
    

def ler_arquivo_site(arquivo='response_site.html'):
    """
    Para caso queira trabalhar com o arquivo salvo na pasta 'dados', sem precisar
    acessar o site novamente.
    """
    with open(f'dados/{arquivo}', 'r', encoding='utf8') as f:
        html=f.read()
    return html


url='https://www.nuuvem.com/br-pt/catalog/platforms/pc/price/promo/sort/bestselling/sort-mode/desc'
# html=ler_arquivo_site()   
html=ler_site(url, False)   
soup = BeautifulSoup(html, 'lxml')
jogos = soup.find_all("div", class_="grid-col-6 grid-col-sm-4 grid-col-md-4 grid-col-lg-3")
jogos_raspados=[]
for jogo in jogos:
    jogo_atual={
        "nome_jogo":jogo.find('a')["title"],
        "link_jogo":jogo.find('a')["href"],
        "plataforma":jogo.find('li', class_='drm-activation__item drm-activation--steam').find('span').text,
        "preco_original":jogo.find('span', class_="product-price--old").text,
        "desconto":jogo.find('span', class_="product-price--discount").text,
        "preco_final":f'R${jogo.find("span", class_="integer").text}{jogo.find("span", class_="decimal").text}'
    }
    jogos_raspados.append(jogo_atual)

with open('dados/dados.json', 'w', encoding='utf8') as f:
    json.dump(jogos_raspados, f, indent=4)