# No que consiste a automação:
# abrir um arquivo TXT com vários CNPJS,
# consultar cada CNPJ na API do Invertexto
# salvar o resultado da consulta no banco MYSQL
# Só devem ser consultados os novos dados inseridos

import re
from os import close

import requests

from tokenCNPJ import API_TOKEN
import pymysql

def conectar_banco():
    conn =pymysql.connect(
        host='localhost',
        user='root',
        password='admin',
        port=3306,
        database='cnpjs'
    )

    conn_cursor = conn.cursor()
    return conn,conn_cursor

def consultar_cadastro(cnpj_procurado):
    # verificar se o CNPJ já está no banco
    conexao_consulta, cursor_consulta = conectar_banco()
    query = '''
        SELECT COUNT(*) FROM cnpjs
        WHERE cnpj = %s;
        '''
    cursor_consulta.execute(query, (cnpj_procurado,))
    resultado = int(cursor_consulta.fetchone()[0]) > 0
    cursor_consulta.close()
    conexao_consulta.close()
    return resultado

cnpjs = open(r'C:\Users\75911\Desktop\pythonProject\cnpj.txt','r').read().splitlines()

for cnpj in cnpjs:

    # remover caracteres não numéricos do CNPJ
    cnpj_corrigido = re.sub(r'\D', '', cnpj)

    if consultar_cadastro(cnpj_corrigido):
        print(f'cnpj {cnpj} já cadastrado')
        continue

    # consultar API
    url = f'https://api.invertexto.com/v1/cnpj/{cnpj_corrigido}?token={API_TOKEN}'
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        razao_social, data_inicio = dados['razao_social'],dados['data_inicio']
        print(cnpj, razao_social, data_inicio)
        conexao, cursor = conectar_banco()

        # instrução SQL para inserir no banco: %s serve como máscara para ser substituido no comando curso.execute
        query = 'INSERT INTO cnpjs (cnpj, razaoSocial, dataInicio) VALUES (%s,%s,%s);' #
        valores = (cnpj_corrigido,razao_social,data_inicio)

        cursor.execute(query,valores) # executar a instrução SQL
        conexao.commit()

        #fechar conexão e cursor
        cursor.close()
        conexao.close()
        continue
    if response.status_code == 422:
        print(f'CNPJ {cnpj} não foi encontrado')
        continue