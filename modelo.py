# -*- coding:utf-8 -*-
from google.appengine.ext import ndb, blobstore
from webapp2_extras.security import hash_password
import util, os, re
from valores import *
from validadores import *

class Usuario(ndb.Model):
    '''Usuário do sistema. Possui o email único e tem a senha gerada 
    automaticamente se chamar o put() sem antes setar a senha.'''
    nome = ndb.StringProperty(default=u'Usuário sem nome')
    email = ndb.StringProperty(required=True)
    senha = ndb.StringProperty()
    criptografou_senha = ndb.BooleanProperty(default=False)
    credenciais = ndb.StringProperty(repeated=True)
    
    def _pre_put_hook(self):
        validar_usuario(self)
        
        if not self.senha:
            self.senha = util.random_string()
        
        if debug: # exibindo a senha somente na máquina local
            print self.senha

        # Caso o usuário possa alterar a senha, a variável criptografou_senha
        # deverá ser setada como False.
        if not self.criptografou_senha:
            self.senha = hash_password(self.senha, 'sha1')
            self.criptografou_senha = True
        
        self.key = ndb.Key(Usuario, self.email)
    
    def add_credencial(self, cred):
        '''Adiciona uma credencial ao usuário. Mas NÃO salva no banco,
        faça isso manualmente.
        :param cred:
            A constante que representa a credencial desejada. Importe
            valores.py e use ava, org, alu ou adm.'''
        validar_credencial(cred)
        if cred not in self.credenciais:
            self.credenciais += [cred]
    
    def del_credencial(self, cred):
        '''Retira uma credencial do usuário. Mas NÃO salva no banco,
        faça isso manualmente.
        :param cred:
            A constante que representa a credencial desejada. Importe
            valores.py e use ava, org, alu ou adm.'''
        validar_credencial(cred)
        novas_credenciais = []
        for c in self.credenciais:
            if c != cred:
                novas_credenciais += [c]
        self.credenciais = novas_credenciais
    
    @classmethod
    def get_or_create(cls, email, **kwds):
        '''Busca por um usuário através do email e, caso não encontre, cria
        um novo passando o e-mail e os **kwds, salva no banco e retorna.
        :returns:
            O usuário com aquele e-mail.'''
        u = cls.find_by_email(email)
        if not u:
            u = cls(email = email, **kwds)
            u.put()
        return u
    
    @classmethod
    def find_by_email(cls, email):
        '''Busca um usuário pelo email.
        :returns:
            O usuário com aquele email ou None.'''
        return cls.query().filter(cls.email == email).get()

class GrupoDeTrabalho(ndb.Model):
    '''Grupo de Trabalho. Possui a sigla única.'''
    nome = ndb.StringProperty(required=True)
    
    sigla = ndb.StringProperty(required=True)
    
    organizador = ndb.StringProperty()
    
    edital = ndb.BlobKeyProperty(required=True)
    
    # : Data de início das submissões
    ini_sub = ndb.DateProperty(required=True)
    
    # : Data de fim das submissões
    fim_sub = ndb.DateProperty(required=True)
    
    # : Data de início das avaliações
    ini_ava = ndb.DateProperty(required=True) 
    
    # : Data de fim das avaliações
    fim_ava = ndb.DateProperty(required=True)
    
    # : Indica a situação do gt (travado, aceitando submissões, etc)
    estado = ndb.StringProperty(default=travado, required=True)
    
    # : Número de avaliadores por artigo
    n_ava_por_art = ndb.IntegerProperty(default=default_n_ava_por_art)
    
    #TODO: refatorar para ndb.KeyProperty(kind=Usuario, repeated=True)
    avaliadores = ndb.StringProperty(repeated=True)
    
    @property
    def artigos(self):
        return Artigo.query(Artigo.sigla_gt == self.sigla)
    
    @classmethod
    def find_by_sigla(cls, sigla):
        return cls.query().filter(cls.sigla == sigla).get()
    
    def _pre_put_hook(self):
        validar_gt(self)
        
        antigo = GrupoDeTrabalho.find_by_sigla(self.sigla)
        if antigo: # Se alterar o edital, exclui o blob anterior
            if antigo.edital != self.edital:
                blobstore.BlobInfo.get(antigo.edital).delete()
        
        # Talvez seja melhor colocar um if aqui pra não recriar a key no alterar
        self.key = ndb.Key(Usuario, self.organizador, GrupoDeTrabalho, self.sigla)

    @classmethod
    def _pre_delete_hook(cls, key):
        self = key.get()
        blobstore.BlobInfo.get(self.edital).delete() # Excluindo o edital
        artigos = Artigo.query(ancestor=ndb.Key(GrupoDeTrabalho,
                               self.sigla)).iter(keys_only=True)
        ndb.delete_multi(artigos)
        
class Artigo(ndb.Model):
    '''Artigo enviado pelos alunos.'''
    titulo = ndb.StringProperty(required=True)
    autor_email = ndb.StringProperty(required=True)
    sigla_gt = ndb.StringProperty(required=True)
    situacao = ndb.StringProperty(default=esperando_avaliacao)
    versao_inicial = ndb.BlobKeyProperty(required=True)
    versao_final = ndb.BlobKeyProperty()
    
    @property
    def avaliacoes(self):
        return Avaliacao.query(Avaliacao.art_key == self.key)
    
    @property
    def autor(self):
        return Usuario.find_by_email(self.autor_email)
    
    @property
    def ultima_versao(self):
        '''Pega a versão do artigo enviada por último.
        :returns:
            A versão final do artigo OU a versão inicial, caso a versão 
            final não tenha sido enviada.'''
        if self.versao_final:
            return self.versao_final
        elif self.versao_inicial:
            return self.versao_inicial
        else:
            None
    
    def _pre_put_hook(self):
        validar_artigo(self)
        self.key = ndb.Key(GrupoDeTrabalho, self.sigla_gt, Artigo,
                           self.autor_email)
    
    @classmethod
    def _pre_delete_hook(cls, key):
        self = key.get()
        # Excluindo os blobs
        if self.versao_final:
            blobstore.BlobInfo.get(self.versao_final).delete()
        if self.versao_inicial:
            blobstore.BlobInfo.get(self.versao_inicial).delete()
        # excluindo as avaliações
        avaliacoes = Avaliacao.query(Avaliacao.art_key == self.key).iter(keys_only=True)
        ndb.delete_multi(avaliacoes)

class Avaliacao(ndb.Model):
    '''Guarda a avaliação feita no artigo.'''
    ava_key = ndb.KeyProperty(required = True, kind = Usuario)
    art_key = ndb.KeyProperty(required = True, kind = Artigo)
    comentarios = ndb.StringProperty(default='')
    nota = ndb.FloatProperty(default=0)
    
    def _pre_put_hook(self):
        #TODO: validação
        pass

    @property
    def situacao(self):
        if self.nota:
            s = feita
        else:
            s = pendente
        return s
    
    @property
    def avaliador(self):
        return self.ava_key.get()
    
    @property
    def artigo(self):
        return self.art_key.get()
    
    
