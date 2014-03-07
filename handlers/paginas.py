#-*- coding:utf-8 -*-
from google.appengine.ext import webapp

from base import BaseHandler

__all__ = ['InicioHandler']

class InicioHandler(BaseHandler, webapp.RequestHandler):
    '''Trata as requisições da página inicial'''
    def get(self):
        self.responder('inicio.html')
