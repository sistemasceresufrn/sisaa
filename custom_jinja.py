# -*- coding:utf-8 -*-

'''Este módulo configura o ambiente do jinja (jinja_env) para renderizar
 os templates e define alguns filtros úteis.'''
import jinja2, os, util
from urls import url

def handle_url(var, key, *extra):
    '''Preenche urls automaticamente nos templates. As urls usadas vem do
    módulo urls para que fique tudo padronizado e fácil de alterar.
    :param var:
        A variável do template (apenas ignore).
    :param key:
        A chave a ser usada no dicionário de urls.
    :param extra:
        Algo a ser adicionado no fim da string.
    :returns:
        A string contendo a url.'''
    return url[key] % extra

# TODO: Estes filtros não estão funcionando corretamente ou não são mais 
# necessários. Apagar depois.
def handle_textarea_duplo_crlf(texto):
    '''Filtro usado em textareas para resolver um bug que duplicava as 
    novas linhas. Ele substitui o \\r\\n por \\n apenas.
    :param texto:
        O valor do textarea a ser formatado.'''
    if texto:
        print texto
        res = texto.replace('\r\n','\n')
    else:
        res = ''
    return res

def handle_lf_como_br(texto):
    if texto:
        print texto.split('\r\n')
        res = util.string_list_para_string_rn(texto.split('\r\n'))
    else:
        res = ''
    return res

jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

jinja_env.filters['textarea_duplo_crlf'] = handle_textarea_duplo_crlf
jinja_env.filters['lf_como_br'] = handle_lf_como_br
jinja_env.filters['url'] = handle_url

