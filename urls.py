#-*- coding:utf-8 -*-
'''Definição das urls do sistema para que fiquem padronizadas, fáceis de
alterar e utilizáveis em qualquer parte do código.'''

from valores import email_regex_py, sigla_regex_py

#Urls base
url = {}
url['cad'] = '/cad'
url['alt'] = '/alt'
url['del'] = '/del'
url['confirmar'] = '/confirmar'
url['meus'] = '/meus'
url['salvar'] = '/salvar'
url['up'] = '/up'
url['enviar'] = '/enviar'
url['down'] = '/down'
url['fin'] = '/finalizar'

url['alu'] = '/alu'
url['adm'] = '/adm'
url['ava'] = '/ava'

# Urls com regex
url['sigla'] = '/<sigla:'+ sigla_regex_py +'>'
url['email'] = '/<email:'+ email_regex_py +'>'

# Urls relacionadas a organizadores
url['org'] = '/org'
url['cad_org'] = url['cad'] + url['org']
url['cad_org_salvar'] = url['cad_org'] + url['salvar']
url['list_org'] = url['org'] + '/'
url['del_org'] = url['del'] + url['org']
url['del_org_email'] = url['del_org'] + url['email']
url['confirmar_del_org'] = url['confirmar'] + url['del_org'] + '/%s'
url['confirmar_del_org_email'] = url['confirmar_del_org'] % url['email'][1:] # pega a url de email sem a /

# Urls relacionadas a grupos de trabalho
url['gt'] = '/gt'
url['dist'] = '/dist/%s'
url['dist_sigla'] = url['dist'] % url['sigla'][1:]
url['res'] = '/resultados/%s'
url['res_sigla'] = url['res'] % url['sigla'][1:] 

url['cad_gt'] = url['cad'] + url['gt']
url['cad_gt_post'] = url['up'] + url['gt']

url['list_gt'] = url['gt'] + '/'
url['meus_gt'] = url['meus'] + url['list_gt']
url['exibir_gt'] = url['gt'] + '/%s'
url['exibir_gt_sigla'] = url['exibir_gt'] % url['sigla'][1:] # pega a url de sigla sem a /

url['del_gt'] = url['del'] + url['gt']
url['del_gt_sigla'] = url['del_gt'] + url['sigla']
url['confirmar_del_gt'] = url['confirmar'] + url['del_gt'] + '/%s'
url['confirmar_del_gt_sigla'] = url['confirmar_del_gt'] % url['sigla'][1:]

url['alt_gt_get'] = url['alt'] + url['gt'] + '/%s'
url['alt_gt_get_sigla'] = url['alt_gt_get'] % url['sigla'][1:]
url['alt_gt_post'] =  url['salvar'] + url['alt_gt_get']
url['alt_gt_post_sigla'] = url['alt_gt_post'] + url['sigla']

url['salvar_res'] = url['salvar'] + url['res']
url['salvar_res_sigla'] = url['salvar'] + url['res_sigla']

url['fin_res'] = url['fin'] + url['res']
url['fin_res_sigla'] = url['fin'] + url['res_sigla']

# Urls relacionadas a artigos
url['art'] = '/art'
url['enviar_sigla'] = url['enviar'] + url['sigla']
url['list_art'] = url['art'] + '/'
url['exibir_art'] = url['art'] + '/<key:>'
url['up_art'] = url['up'] + url['art']

# Urls relacionadas a avaliações
url['avaliacao'] = '/avaliacao'
url['exibir_avaliacao'] = url['avaliacao'] + '/%s'
url['exibir_avaliacao_key'] = url['avaliacao'] + '/<key:>'
url['avaliar'] = '/avaliar/%s'
url['avaliar_key'] = url['avaliar'] % '<key:>'
url['minhas_avaliacoes'] = url['meus'] + url['avaliacao']

# Outras urls
url['login'] = '/login'
url['entrou'] = '/entrou'
url['logout'] = '/logout'
url['requer_permissao'] = '/requer_permissao'
url['baixar'] = url['down'] + '/%s'
url['baixar_key'] = url['baixar'] % '<key:>'
