# -*- coding:utf-8 -*-
from google.appengine.ext import webapp
from urls import url
from valores import *
from auth import requer_login
from base import BaseHandler

__all__ = ['EntrouHandler']

class EntrouHandler(BaseHandler, webapp.RequestHandler):
    '''Handler criado para testes. Será apagado futuramente.'''
    @requer_login
    def get(self):
        user = self.usuario
        self.responder('entrou.html', dict(u = user,
            admin_checked = 'checked' if adm in user.credenciais else '',
            aluno_checked = 'checked' if alu in user.credenciais else '',
            aval_checked = 'checked' if ava in user.credenciais else '',
            org_checked = 'checked' if org in user.credenciais else '',))
    
    @requer_login
    def post(self):
        u = self.usuario
        
        cred = [] # credenciais marcadas
        if self.request.get(adm) == 'on': # on é a constante passada pelo html
            cred += [adm]
        if self.request.get(alu) == 'on':
            cred += [alu]
        if self.request.get(ava) == 'on':
            cred += [ava]
        if self.request.get(org) == 'on':
            cred += [org]
        
        u.credenciais = cred
        self.usuario = u
        self.usuario.put()
        
        self.redirect(url['entrou'])

