# -*- coding:utf-8 -*-
import util, re, urllib, valores

from google.appengine.ext import ndb

from google.appengine.ext import webapp, blobstore
from google.appengine.ext.webapp import blobstore_handlers

from modelo import Usuario, GrupoDeTrabalho, Artigo
from valores import org
from urls import url

from gaesessions import get_current_session
from auth import *
from webapp2_extras.security import hash_password

from base import BaseHandler

__all__ = ['AdminHandler', 'AvalHandler', 'AlunoHandler', 'OrgHandler']

class AdminHandler(BaseHandler, webapp.RequestHandler):
    '''Handler para testes'''
    @requer_adm
    def get(self):
        self.responder('admin.html')
        
class AvalHandler(BaseHandler, webapp.RequestHandler):
    '''Handler para testes'''
    @requer_ava
    def get(self):
        self.responder('aval.html')

class AlunoHandler(BaseHandler, webapp.RequestHandler):
    '''Handler para testes'''
    @requer_alu
    def get(self):
        self.responder('aluno.html')

class OrgHandler(BaseHandler, webapp.RequestHandler):
    '''Handler que gerencia organizadores.'''
    @requer_org
    def teste(self):
        '''Criado apenas para testar credenciais. Deve ser apagado depois.'''
        self.responder('org.html')
    
    @requer_adm
    def cadastrar_get(self):
        self.responder('cad_org.html')
    
    @requer_adm
    def cadastrar_post(self):
        self._validar_campos()
        nome = self.request.get('nome').strip()
        email = self.request.get('email').strip()
        #TODO: enviar email para o organizador
        o = Usuario.get_or_create(email = email, nome = nome)
        o.add_credencial(org)
        o.put()
        
        if o.key == self.usuario.key: # Caso o próprio usuário 
            self.usuario = o          # se cadastre como organizador,
                                      # atualiza a memória para 
                                      # ficar consistente com o banco
        self.redirect(url['entrou'])
    
    @requer_adm
    def listar(self):
        organizadores = Usuario.query(Usuario.credenciais == org)
        self.responder('listar_org.html', {'organizadores' : organizadores})
    
    @requer_adm
    def confirmar_excluir(self, email):
        email = str(urllib.unquote(email))
        valores = {
            'mensagem' : u'Você está excluindo a credencial de organizador'+
                        u' de ' + email + u', mas ele ainda poderá utilizar o '+
                        u'sistema, só não terá mais permissão de acessar ' +
                        u'páginas restritas a organizadores.',
            'uri_sim' : url['del_org'] + '/' + email,
            'uri_nao' : url['list_org']
            }
        self.responder('confirmacao.html', valores)
        
    @requer_adm
    def excluir(self, email):
        email = str(urllib.unquote(email))
        u = Usuario.find_by_email(email)
        u.del_credencial(org)
        u.put()
        if u.key == self.usuario.key: # Caso o próprio usuário exclua sua
            self.usuario = u          # credencial de organizador,
                                      # atualiza a memória para ficar
                                      # consistente com o banco
        self.redirecionar('/entrou')
    
    def _validar_campos(self):
        '''Valida os campos do formulário de cadastro de Organizador.'''
        assert isinstance(self.request, webapp.Request), 'Requisição inválida.'
        campos = ['nome','email']
        for i in campos:
            campo = self.request.get(i).strip()
            assert campo, 'Campo obrigatório não preenchido.'
        # TODO: validar email
        
