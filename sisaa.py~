# -*- coding:utf-8 -*-
from google.appengine.ext import webapp
from webapp2 import Route

app = webapp.WSGIApplication([
    Route('/', handler='handlers.InicioHandler'),
    
    Route('/adm', handler='handlers.AdminHandler'), # TESTE: serão apagados
    Route('/ava', handler='handlers.AvalHandler'), # TESTE: serão apagados
    Route('/alu', handler='handlers.AlunoHandler'), # TESTE: serão apagados
    Route('/org', handler='handlers.OrgHandler:teste'), # TESTE: serão apagados
    
    Route('/cad/org', handler='handlers.OrgHandler'),
    Route('/org/', handler='handlers.OrgHandler'),
    
    Route('/entrou', handler='handlers.EntrouHandler'),
    Route('/saiu', handler='handlers.SaiuHandler'),
    Route('/logout', handler='handlers.LogoutHandler'),
    
    Route('/cad/gt', handler='handlers.GTHandler'),
    Route('/gt/', handler='handlers.GTHandler:listar'),
    Route('/gt/<sigla:>', handler='handlers.GTHandler:exibir'),
    
    Route('/cadastrarOrg', handler='handlers.OrgHandler'),
    ],
    debug=True)
