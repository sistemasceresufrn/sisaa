#-*- coding:utf-8 -*-
'''Definição das urls do sistema para que fiquem padronizadas, fáceis de
alterar e utilizáveis em qualquer parte do código.'''

from valores import email_regex_py, sigla_regex_py

#Urls base
url_cad = '/cad'
url_alt = '/alt'
url_del = '/del'
url_confirmar = '/confirmar'
url_meus = '/meus'
url_salvar = '/salvar'
url_up = '/up'
url_enviar = '/enviar'
url_down = '/down'

url_alu = '/alu'
url_adm = '/adm'
url_ava = '/ava'

# Urls com regex
url_sigla = '/<sigla:'+ sigla_regex_py +'>'
url_email = '/<email:'+ email_regex_py +'>'

# Urls relacionadas a organizadores
url_org = '/org'
url_cad_org = url_cad + url_org
url_cad_org_salvar = url_cad_org + url_salvar
url_list_org = url_org + '/'
url_del_org = url_del + url_org
url_del_org_email = url_del_org + url_email
url_confirmar_del_org = url_confirmar + url_del_org
url_confirmar_del_org_email = url_confirmar_del_org + url_email

# Urls relacionadas a grupos de trabalho
url_gt = '/gt'

url_cad_gt = url_cad + url_gt
url_cad_gt_post = url_up + url_gt

url_list_gt = url_gt + '/'
url_meus_gt = url_meus + url_list_gt
url_exibir_gt = url_gt
url_exibir_gt_sigla = url_exibir_gt + url_sigla

url_del_gt = url_del + url_gt
url_del_gt_sigla = url_del_gt + url_sigla
url_confirmar_del_gt = url_confirmar + url_del_gt
url_confirmar_del_gt_sigla = url_confirmar_del_gt + url_sigla

url_alt_gt_get = url_alt + url_gt
url_alt_gt_get_sigla = url_alt_gt_get + url_sigla
url_alt_gt_post =  url_salvar + url_alt_gt_get
url_alt_gt_post_sigla = url_alt_gt_post + url_sigla

# Urls relacionadas a artigos
url_art = '/art'
url_enviar_sigla = url_enviar + url_sigla
url_list_art = url_art + '/'
url_exibir_art = url_art + '/<key:>'
url_up_art = url_up + url_art


# Outras urls
url_login = '/login'
url_entrou = '/entrou'
url_logout = '/logout'
url_requer_permissao = '/requer_permissao'
url_baixar = url_down + '/<key:>'
