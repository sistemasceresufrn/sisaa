# -*- coding:utf-8 -*-
import util, re, urllib, valores

from google.appengine.ext import ndb

from google.appengine.ext import webapp, blobstore
from google.appengine.ext.webapp import blobstore_handlers

from modelo import Usuario, GrupoDeTrabalho, Artigo
from valores import *
from urls import *

from gaesessions import get_current_session
from auth import *
from webapp2_extras.security import hash_password

from base import BaseHandler

__all__ = ['UploadHandler', 'DownloadHandler']

class UploadHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    #TODO: Levar este método para o ArtigoHandler e apagar este handler.
    '''Trata do upload de artigos.'''
    @requer_alu
    def artigo(self):
        # TODO: validar campos
        
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        key = blob_info.key()
        
        artigo = Artigo(titulo = self.request.get('titulo'),
            autor_email=self.usuario.email,
            versao_inicial=key,
            sigla_gt = self.request.get('gt'))
        artigo.put()
        
        self.redirect('/art/%s' % artigo.key.urlsafe())

class DownloadHandler(BaseHandler, blobstore_handlers.BlobstoreDownloadHandler):
    '''Handler genérico que trata do download de quaisquer blobs.'''
    def get(self, key):
        key = str(urllib.unquote(key))
        blob_info = blobstore.BlobInfo.get(key)
        self.send_blob(blob_info)
