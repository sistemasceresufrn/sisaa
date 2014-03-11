# -*- coding:utf-8 -*-
from google.appengine.ext import ndb, blobstore
from engineauth.models import User

class GrupoDeTrabalho(ndb.Model):
    nome = ndb.StringProperty(required=True)
    
    #TODO: barrar siglas duplicadas com gatilho antes do put()
    sigla = ndb.StringProperty(required=True)
    
    organizador = ndb.StringProperty() # ReferenceProperty(User, required=True)
    
    edital = blobstore.BlobReferenceProperty(required=True)
    
    # : Data de início das submissões
    ini_sub = ndb.DateProperty(required=True)
    
    # : Data de fim das submissões
    fim_sub = ndb.DateProperty(required=True)
    
    # : Data de início das avaliações
    ini_ava = ndb.DateProperty(required=True) 
    
    # : Data de fim das avaliações
    fim_ava = ndb.DateProperty(required=True)
    
    # : Indica se os artigos já foram aprovados 
    finalizado = ndb.BooleanProperty(default=False)
    
    ''' Guarda quem finalizou o evento. 
    Em geral, é o próprio organizador, mas também pode ser
    finalizado pelo administrador.'''
    finalizador = ndb.StringProperty() # ndb.ReferenceProperty(User)
    
    avaliadores = ndb.StringProperty(repeated=True)

