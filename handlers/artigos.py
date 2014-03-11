# -*- coding:utf-8 -*-
import util, re, urllib, valores

from google.appengine.ext import ndb

from google.appengine.ext import webapp, blobstore
from google.appengine.ext.webapp import blobstore_handlers

from modelo import Usuario, GrupoDeTrabalho, Artigo
from valores import *
from urls import url

from gaesessions import get_current_session
from auth import *
from webapp2_extras.security import hash_password

from base import BaseHandler

__all__ = ['ArtigoHandler']

class ArtigoHandler(BaseHandler, webapp.RequestHandler):
    #TODO: fazer upload de artigos através deste handler.
    '''Gerencia as páginas relacionadas a artigos. Não trada do upload 
    ainda, esse trabalho é feito no UploadHandler.'''
    @requer_alu
    def enviar(self, sigla):
        sigla = str(urllib.unquote(sigla))
        upload_url = blobstore.create_upload_url(url['up_art'])
        grupo = GrupoDeTrabalho.find_by_sigla(sigla)
        if grupo:
            self.responder('enviar_artigo.html', {'upload_url' : upload_url,
                                                  'grupo' : grupo})
        else:
            self.erro_404()
    
    @requer_alu
    def exibir(self, key):
        key = str(urllib.unquote(key))
        artigo = ndb.Key(urlsafe=key).get()
        self.responder('artigo.html', {'artigo' : artigo})
    
    @requer_alu
    def listar(self):
        artigos = Artigo.query(Artigo.autor_email == self.usuario.email)
        self.responder('listar_artigos.html', {'artigos' : artigos})

