# -*- coding:utf-8 -*-
'''Este módulo configura o ambiente do jinja (jinja_env) para renderizar
 os templates e define alguns filtros úteis.'''
import jinja2, os, util

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
