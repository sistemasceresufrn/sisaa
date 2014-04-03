# -*- coding:utf-8 -*-
'''Este módulo é responsável por fornecer emails.'''

from custom_jinja import jinja_env
from google.appengine.api import mail

def get_email(template, valores={}):
    '''Renderiza um template de email.
    :param template:
        O nome do template a ser carregado. Uma string.
    :param valores:
        Dicionário a ser usado para a renderização dos valores no template.
    :returns:
        O template renderizado. Uma string.'''
    assert isinstance(template, basestring), 'template deve ser uma string.'
    assert isinstance(valores, dict), 'valores deve ser um dict.'
    template = '/emails/' + template
    return jinja_env.get_template(template).render(valores)

def enviar_email(para, assunto, template, valores={}, 
    de='Sistemas CERES/UFRN <sistemas@ceresufrn.org>'):
    '''Envia um email.
    :param para:
        O destinatário (to) do email.
    :param assunto:
        O assunto (subject) do email.
    :param template:
        O nome do template a ser carregado para construir o corpo (body)
        do email. Uma string. Obs.: Não precisa colocar /emails/, pois 
        o próprio método já faz isso.
    :param valores:
        Dicionário a ser usado para a renderização dos valores no template.
    :param de:
        O remetente (from) do email.'''
    assert isinstance(assunto, basestring), 'assunto deve ser uma string.'
    assert isinstance(template, basestring), 'template deve ser uma string.'
    assert isinstance(valores, dict), 'valores deve ser um dict.'
    assert isinstance(de, basestring), 'de deve ser uma string.'
    corpo = get_email(template, valores)
    mail.send_mail(sender=de, to=para, subject=assunto, body=corpo)
