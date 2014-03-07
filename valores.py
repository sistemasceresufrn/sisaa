#-*- coding:utf-8 -*-

'''Este módulo contém valores em geral; qualquer valor que deva ser usado
em várias partes do código. Serve para definir constantes, strings, etc.'''

import os

# vale True se estiver em fase de desenvolvimento
debug = ('Development' == os.environ['SERVER_SOFTWARE'][:11])

# credenciais do usuário
adm = u'adm'
ava = u'ava'
alu = u'alu'
org = u'org'
list_credenciais = [adm, ava, alu, org]

# administrador do sistema
adm_nome = 'Administrador do sistema'
adm_email = 'ciromoraismedeiros@gmail.com'
adm_senha = '40bd001563085fc35165329ea1ff5c5ecbdbbeef'


# estados do grupo de trabalho
travado = u'travado'
aceitando_submissoes = u'aceitando submissoes'
aceitando_avaliacoes = u'aceitando avaliacoes'
finalizado = u'finalizado'
list_estados_gt = [travado, aceitando_submissoes, aceitando_avaliacoes, 
    finalizado]

# situações de artigos
aceito = u'aceito'
aceito_com_correcoes = u'aceito com correções'
recusado = u'recusado'
esperando_avaliacao = u'esperando avaliação'
list_situacoes_artigo = [aceito, aceito_com_correcoes, recusado, 
    esperando_avaliacao]

# expressões regulares para validações
email_regex_py = r'\w+@\w+\.\w+\.?\w*' #TODO: não aceitar caracteres estranhos
nome_regex_py = r'\w+' #TODO: não aceitar números ou caracteres estranhos
nome_gt_regex_py = r'\w+'
sigla_regex_py = r'\w+' #TODO: não aceitar / ? = e outros caracteres de url

# valores default
default_n_ava_por_art = 3
