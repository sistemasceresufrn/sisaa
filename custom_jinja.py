# -*- coding:utf-8 -*-

'''Este módulo configura o ambiente do jinja (jinja_env) para renderizar
 os templates e define alguns filtros úteis.'''
import jinja2, os, util
from urls import url

def handle_url(var, key, *extra):
    '''Preenche urls automaticamente nos templates, basta usar::
        {{var | url("id_da_url", "parâmetros")}}
    As urls usadas vem do módulo urls para que fique tudo padronizado e 
    fácil de alterar.
    :param var:
        A variável do template (apenas ignore).
    :param key:
        A chave a ser usada no dicionário de urls.
    :param extra:
        Parâmetros de formatação da string.
    :returns:
        A string contendo a url.'''
    return url[key] % extra

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

jinja_env.filters['url'] = handle_url
