import requests

ceps = open('ceps.txt','r').read().splitlines()
for cep in ceps:
    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    if response.status_code == 200:
        dados = response.json()
        if 'erro' in dados.keys():
            print(f'CEP {cep} não encontrado')
            continue
        print(dados)
    else:
        print('Erro na consulta')