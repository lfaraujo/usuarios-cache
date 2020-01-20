import os
import sys
import csv
import requests


# Exibe os dados do usuario consultado
def exibir_dados_usuario(dados):
    print("Dados do usuario %s:" % dados[0])
    print("- E-mail: %s" % dados[1])
    print("- Website: %s" % dados[2])
    print("- Hemisferio: %s" % dados[3])


# Indica hemisferio de acordo com a latitude
def calcular_hemisferio(latitude):
    if latitude > 0:
        return "norte"
    elif latitude < 0:
        return "sul"


# Armazena dados em cache para o usuario
def armazenar_cache(dados):
    with open('cache.csv', 'a', newline='') as cache:
        fieldnames = ['username', 'email', 'website', 'hemisferio']
        writer = csv.DictWriter(cache, delimiter=',', fieldnames=fieldnames)
        writer.writerow({'username': dados[0], 'email': dados[1], 'website': dados[2], 'hemisferio': dados[3]})
        cache.close()


# Formata dados do json obtido
def formatar_dados(dados):
    usuario = dados['username']
    email = dados['email']
    website = dados['website']
    hemisferio = calcular_hemisferio(float(dados['address']['geo']['lat']))

    return usuario, email, website, hemisferio


# Efetua requisicao para obter dados do usuario
def efetuar_requisicao(usuario):
    data = {'username': usuario}
    response = requests.get("https://jsonplaceholder.typicode.com/users", params=data)

    return response.json()


# Valida a existencia de dados em cache para o usuario
def validar_cache(usuario):
    with open('cache.csv', 'r', newline='') as cache:
        reader = csv.DictReader(cache)
        for linha in reader:
            if linha['username'].upper() == usuario.upper():
                return linha['username'], linha['email'], linha['website'], linha['hemisferio']


# Cria arquivo csv vazio para armazenamento de cache
def criar_arquivo_cache():
    if os.path.isfile('cache.csv'):
        pass
    else:
        with open('cache.csv', 'w', newline='') as cache:
            fieldnames = ['username', 'email', 'website', 'hemisferio']
            writer = csv.DictWriter(cache, fieldnames=fieldnames)
            writer.writeheader()
            cache.close()


# Obtem dados do usuario em cache/requisicao
def obter_dados(usuario):
    criar_arquivo_cache()
    retorno_validacao = validar_cache(usuario)

    if not retorno_validacao:
        response_json = efetuar_requisicao(usuario)

        if not response_json:
            print("Nao foram identificados usuarios com esse username.")
        else:
            dados = response_json[0]
            dados_formatados = formatar_dados(dados)

            armazenar_cache(dados_formatados)
            exibir_dados_usuario(dados_formatados)
    else:
        exibir_dados_usuario(retorno_validacao)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        obter_dados(username)
    else:
        print("Informe um nome de usuario para consulta!")
