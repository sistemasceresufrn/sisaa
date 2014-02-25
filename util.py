# -*- coding:utf-8 -*- 
from datetime import datetime
import string, random

def str_para_date(valor, formato='%Y-%m-%d'):
    '''Retorna um objeto datetime no formato escolhido.
    Obs.: utiliza o método strip() para retirar espaços em branco antes e
    depois das strings de valor e formato.
    :param: valor
        Uma string contendo o valor formatado da data.
    :param: formato
        Uma string que descreve o formato do parâmetro valor.
    :returns:
        Um objeto date com dia, mês e ano setados de acordo com o valor.'''
    valor = valor.strip()
    formato = formato.strip()
    return (datetime.strptime(valor, formato)).date()
    
def random_string(conjunto=string.uppercase, tamanho=8):
    '''Retorna uma string aleatória. Pode ser usada para criar senhas.
    :param: conjunto
        String contendo os caracteres a sortear.
    :param: tamanho
        Tamanho da string retornada.
    :returns:
        Uma string aleatória do tamanho informado e contendo apenas os
        caracteres do conjunto.'''
    return ''.join(random.sample(conjunto, tamanho))

def string_list_para_string_rn(lista):
    '''Converte uma lista de string para uma única string que separa os
    elementos com um \r\n (para ser usada por exemplo em páginas html).
    :param lista:
        A list de strings que será usada para criar a string formatada com
        \\r\\n.
    :returns:
        A string formatada.'''
    result = ''
    for i in lista:
        result += i + '\r\n'
    return result
