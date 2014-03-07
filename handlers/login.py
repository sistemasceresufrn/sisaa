# -*- coding:utf-8 -*-
from google.appengine.ext import webapp
from modelo import Usuario
from auth import requer_login
from webapp2_extras.security import hash_password
from base import BaseHandler

__all__ = ['LoginHandler']

class LoginHandler(BaseHandler, webapp.RequestHandler):
    '''Handler que trata de login e logout.'''
    
    def login(self):
        email = self.request.get('email')
        senha = hash_password(self.request.get('senha'), 'sha1')
        usuario = Usuario.query().filter(Usuario.email == email)\
            .filter(Usuario.senha == senha).get()
            
        if usuario:
            self.usuario = usuario
            self.redirect('/entrou')
        else:
            self.redirecionar('/', [u'Login ou senha incorretos.'])

    @requer_login
    def logout(self):
        '''Desloga o usuário do sistema.'''
        if self.sessao.has_key('usuario'):
            self.sessao.terminate()
        self.redirecionar('/', [u'Você saiu do sistema'])

