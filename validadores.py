#-*- coding:utf-8 -*-
import re, urllib, modelo
from valores import *
from google.appengine.ext import blobstore

email_regex = re.compile(email_regex_py)
nome_regex = re.compile(nome_regex_py)

sigla_regex = re.compile(sigla_regex_py)
nome_gt_regex = re.compile(nome_gt_regex_py)

def validar_credencial(cred):
    '''Valida uma credencial.'''
    if cred not in list_credenciais:
        raise ValueError(u'Credencial inválida.')

def validar_credenciais(creds):
    '''Valida uma lista de credenciais.'''
    for c in creds:
        validar_credencial(c)

def validar_email(email):
    '''Valida um email.'''
    if not email_regex.match(email):
        raise ValueError(u'O email %s deve ter o formato nome@exemplo.com' 
            % email)

def validar_email_unico(email, usuario_key):
    validar_email(email)
    u = modelo.Usuario.find_by_email(email)
    if u:
        if usuario_key != u.key.urlsafe():
            raise ValueError(u'O email deve ser único.')

def validar_nome(nome):
    '''Valida um nome de usuário.'''
    if nome:
        if not nome_regex.match(nome):
            raise ValueError(u'O nome %s deve conter apenas letras' % nome)

def validar_usuario(u):
    '''Valida um usuário.'''
    validar_email_unico(u.email, u.key.urlsafe())
    validar_nome(u.nome)
    validar_credenciais(u.credenciais)

def validar_sigla(sigla):
    '''Valida uma sigla.'''
    if not sigla_regex.match(sigla):
        raise ValueError(u'A sigla', sigla, u'deve conter apenas caracteres ' +
            u' alfanuméricos.')

def validar_sigla_unica(sigla, key_gt):
    '''Valida uma sigla e garante que ela seja única.
    :param sigla:
        A sigla para validar.
    :param key_gt:
        A key do GT que possui essa sigla. É uma string, portanto use
        seu_gt.key.urlsafe()'''
    validar_sigla(sigla)
    gt = modelo.GrupoDeTrabalho.find_by_sigla(sigla)
    if gt:
        if key_gt != gt.key.urlsafe():
            raise ValueError(u'A sigla deve ser única')
    
def validar_organizador(email_org):
    '''Valida um organizador, garantindo que o email é válido, o usuário
    existe e tem a credencial.
    :param email_org:
        O e-mail do organizador.'''
    validar_email(email_org)
    usuario = modelo.Usuario.find_by_email(email_org)
    if usuario:
        if org not in usuario.credenciais:
            raise ValueError(u'O usuário %s não é organizador.' % email_org)
    else:
        raise ValueError(u'O usuário %s não existe' % email_org)

def validar_nome_gt(nome):
    '''Valida um nome de GT.'''
    if nome:
        if not nome_regex.match(nome):
            raise ValueError(u'O nome %s deve conter apenas caracteres' +
                u' alfanuméricos' % nome)

def validar_estado(estado):
    '''Garante que o estado do gt é um dos possíveis (veja valores.py)'''
    if estado not in list_estados_gt:
        raise ValueError(u'O estado %s é inválido.' % estado)

def validar_avaliador(email_ava):
    '''Valida um avaliador, garantindo que o email é válido, o usuário
    existe e tem a credencial.
    :param email_ava:
        E-mail do avaliador.'''
    validar_email(email_ava)
    usuario = modelo.Usuario.find_by_email(email_ava)
    if usuario:
        if ava not in usuario.credenciais:
            raise ValueError(u'O usuário %s não é avaliador.' % email_ava)
    else:
        raise ValueError(u'O usuário %s não existe' % email_ava)

def validar_avaliadores(emails_ava):
    '''Valida uma lista de avaliadores.
    :param emails_ava:
        list contendo os emails dos avaliadores a validar.'''
    for e in emails_ava:
        validar_avaliador(e)

def validar_n_ava_por_art(n):
    '''Valida o n_ava_por_art (número de avaliadores por artigo) de um gt.
    :param n:
        O n_ava_por_art. Um float.'''
    assert isinstance(n, int), u'O número de avaliadores por artigo ' +\
                                 u'deve ser um número natural maior que 0.'
    if n < 1 or n > 10:
        raise ValueError(u'O número de avaliadores por artigo deve ser '
                         + u' maior que 0.')

def validar_gt(gt):
    '''Valida um GT'''
    validar_nome_gt(gt.nome)
    validar_sigla_unica(gt.sigla, gt.key.urlsafe())
    validar_organizador(gt.organizador)
    validar_blob(gt.edital)
    validar_estado(gt.estado)
    validar_avaliadores(gt.avaliadores)
    validar_n_ava_por_art(gt.n_ava_por_art)

def validar_situacao_art(s):
    '''Valida a situação de um artigo.
    :param s:
        A situação do artigo.'''
    for i in list_situacoes_artigo:
        if s == i:
            return
    raise ValueError('A situação deve ser uma das seguintes' + 
                      str(list_situacoes_artigo))
    
def validar_blob(key):
    '''Valida um blob verificando se ele existe no blobstore.
    :param key:
        A chave do blob a ser buscado. Uma BlobKey.'''
    if not blobstore.BlobInfo.get(key):
        raise ValueError(u'Arquivo inexistente.' +
                         u' A key não corresponde a nenhum blob.')

def validar_artigo(art):
    '''Valida um artigo.'''
    validar_email(art.autor_email)
    validar_sigla(art.sigla_gt)
    validar_situacao_art(art.situacao)
    validar_blob(art.versao_inicial)
    if art.versao_final:
        validar_blob(art.versao_final)

def validar_comentarios(s):
    '''Valida os comentários de uma avaliação.
    :param s:
        A string que representa os comentários.'''
    assert isinstance(s, unicode), u'Os comentários devem ser unicode.'
    
def validar_avaliacao(a):
    '''Valida uma avaliação.'''
    validar_usuario(a.avaliador)
    validar_blob(a.art_key)
    validar_comentarios(a.comentarios)
    
