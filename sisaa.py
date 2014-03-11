# -*- coding:utf-8 -*-
from google.appengine.ext import webapp
from webapp2 import Route
from appengine_config import webapp_add_wsgi_middleware
from modelo import Usuario
from valores import adm_nome, adm_email, adm_senha, list_credenciais
from urls import url

app = webapp.WSGIApplication([
    Route('/', handler='handlers.InicioHandler'),
    
    Route(url['adm'], 'handlers.AdminHandler'), # TESTE: serão apagados
    Route(url['ava'], 'handlers.AvalHandler'), # TESTE: serão apagados
    Route(url['alu'], 'handlers.AlunoHandler'), # TESTE: serão apagados
    Route(url['org'], 'handlers.OrgHandler:teste'), # TESTE: serão apagados
    
    Route(url['cad_org'], 'handlers.OrgHandler:cadastrar_get'),
    Route(url['cad_org_salvar'], 'handlers.OrgHandler:cadastrar_post', methods=['POST']),
    Route(url['list_org'], 'handlers.OrgHandler:listar'),
    Route(url['confirmar_del_org_email'], 'handlers.OrgHandler:confirmar_excluir'),
    Route(url['del_org_email'], 'handlers.OrgHandler:excluir', methods=['POST']),
    
    Route(url['login'], 'handlers.LoginHandler:login'),
    Route(url['entrou'], 'handlers.EntrouHandler'),
    Route(url['logout'], 'handlers.LoginHandler:logout'),
    Route(url['requer_permissao'], 'handlers.LoginHandler:requer_permissao'),
    
    Route(url['cad_gt'], 'handlers.GTHandler:cadastrar_get'),
    Route(url['list_gt'], 'handlers.GTHandler:listar'),
    Route(url['meus_gt'], 'handlers.GTHandler:listar_meus'),
    Route(url['exibir_gt_sigla'], 'handlers.GTHandler:exibir'),
    Route(url['cad_gt_post'], 'handlers.GTHandler:cadastrar_post', methods=['POST']),
    Route(url['confirmar_del_gt_sigla'], 'handlers.GTHandler:confirmar_excluir'),
    Route(url['del_gt_sigla'], 'handlers.GTHandler:excluir', methods=['POST']),
    Route(url['alt_gt_get_sigla'], 'handlers.GTHandler:alterar_get'),
    Route(url['alt_gt_post_sigla'], 'handlers.GTHandler:alterar_post', methods=['POST']),
    Route(url['dist_sigla'], 'handlers.GTHandler:distribuir'),
    
    Route(url['enviar_sigla'], 'handlers.ArtigoHandler:enviar'),
    Route(url['list_art'], 'handlers.ArtigoHandler:listar'),
    Route(url['exibir_art'], 'handlers.ArtigoHandler:exibir'),
    Route(url['up_art'], 'handlers.UploadHandler:artigo', methods=['POST']),
    Route(url['baixar_key'], 'handlers.DownloadHandler'),
    
    Route(url['minhas_avaliacoes'], 'handlers.AvaliacaoHandler:listar_minhas_avaliacoes'),
    Route(url['exibir_avaliacao_key'], 'handlers.AvaliacaoHandler:avaliar_get'),
    Route(url['avaliar_key'], 'handlers.AvaliacaoHandler:avaliar_post'),
    ],
    debug=True)

app = webapp_add_wsgi_middleware(app) # Adicionando gaesessions


# cadastrando administrador do sistema
adm  = Usuario(nome = adm_nome, email = adm_email, senha = adm_senha, 
    criptografou_senha = True, credenciais = list_credenciais)
try:
    adm.put()
except:
    pass
