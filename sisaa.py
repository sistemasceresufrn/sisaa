# -*- coding:utf-8 -*-
from google.appengine.ext import webapp
from webapp2 import Route
from appengine_config import webapp_add_wsgi_middleware
from modelo import Usuario
from valores import adm_nome, adm_email, adm_senha, list_credenciais
from urls import *

app = webapp.WSGIApplication([
    Route('/', handler='handlers.InicioHandler'),
    
    Route(url_adm, 'handlers.AdminHandler'), # TESTE: serão apagados
    Route(url_ava, 'handlers.AvalHandler'), # TESTE: serão apagados
    Route(url_alu, 'handlers.AlunoHandler'), # TESTE: serão apagados
    Route(url_org, 'handlers.OrgHandler:teste'), # TESTE: serão apagados
    
    Route(url_cad_org, 'handlers.OrgHandler:cadastrar_get'),
    Route(url_cad_org_salvar, 'handlers.OrgHandler:cadastrar_post', methods=['POST']),
    Route(url_list_org, 'handlers.OrgHandler:listar'),
    Route(url_confirmar_del_org_email, 'handlers.OrgHandler:confirmar_excluir'),
    Route(url_del_org_email, 'handlers.OrgHandler:excluir', methods=['POST']),
    
    Route(url_login, 'handlers.LoginHandler:login'),
    Route(url_entrou, 'handlers.EntrouHandler'),
    Route(url_logout, 'handlers.LoginHandler:logout'),
    Route(url_requer_permissao, 'handlers.LoginHandler:requer_permissao'),
    
    Route(url_cad_gt, 'handlers.GTHandler:cadastrar_get'),
    Route(url_list_gt, 'handlers.GTHandler:listar'),
    Route(url_meus_gt, 'handlers.GTHandler:listar_meus'),
    Route(url_exibir_gt_sigla, 'handlers.GTHandler:exibir'),
    Route(url_cad_gt_post, 'handlers.GTHandler:cadastrar_post', methods=['POST']),
    Route(url_confirmar_del_gt_sigla, 'handlers.GTHandler:confirmar_excluir'),
    Route(url_del_gt_sigla, 'handlers.GTHandler:excluir', methods=['POST']),
    Route(url_alt_gt_get_sigla, 'handlers.GTHandler:alterar_get'),
    Route(url_alt_gt_post_sigla, 'handlers.GTHandler:alterar_post', methods=['POST']),
    
    Route(url_enviar_sigla, 'handlers.ArtigoHandler:enviar'),
    Route(url_list_art, 'handlers.ArtigoHandler:listar'),
    Route(url_exibir_art, 'handlers.ArtigoHandler:exibir'),
    Route(url_up_art, 'handlers.UploadHandler:artigo', methods=['POST']),
    Route(url_baixar, 'handlers.DownloadHandler'),
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
