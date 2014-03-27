# -*- coding:utf-8 -*-
from base import BaseHandler
from google.appengine.ext import webapp, ndb
from auth import requer_ava
from modelo import Avaliacao
from valores import pendente
import urllib
from urls import url

__all__ = ['AvaliacaoHandler']

class AvaliacaoHandler(BaseHandler, webapp.RequestHandler):
    
    @requer_ava
    def listar_minhas_avaliacoes(self):
        avaliacoes = Avaliacao.query(Avaliacao.ava_key == self.usuario.key)
        self.responder('listar_minhas_avaliacoes.html',
                        {'avaliacoes' : avaliacoes})
    
    @requer_ava
    def avaliar_get(self, key):
        #TODO: proibir que outro avaliador pegue o link e altere aqui
        key = str(urllib.unquote(key))
        avaliacao = ndb.Key(urlsafe=key).get()
        self.responder('avaliacao.html', {'a' : avaliacao})
    
    @requer_ava
    def avaliar_post(self, key):
        #TODO: proibir que outro avaliador pegue o link e altere aqui
        key = str(urllib.unquote(key))
        nota = float(self.request.get('nota'))
        comentarios = self.request.get('comentarios')
        
        a = ndb.Key(urlsafe=key).get()
        a.nota = nota
        a.comentarios = comentarios
        a.put()
        
        self.redirecionar(url['entrou'], [u'Avaliação salva'])
    
    @requer_ava
    def menu(self):
        minhas = Avaliacao.query(Avaliacao.ava_key == self.usuario.key)
        pendentes = []
        for i in minhas:
            if not i.nota:
                pendentes += [i]
        self.responder('menu_avaliacao.html', {'minhas' : minhas,
            'pendentes' : pendentes})
        
        
        
