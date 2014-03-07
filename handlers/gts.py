# -*- coding:utf-8 -*-
import util, re, urllib

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

__all__ = ['GTHandler']

class GTHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    '''Handler que gerencia grupos de trabalho'''

    @requer_org
    def cadastrar_get(self):
        valores = {'upload_url' : blobstore.create_upload_url(url_cad_gt_post)}
        self.responder('cad_gt.html',valores)
    
    @requer_org
    def cadastrar_post(self):
        #self._validar_campos()
        gt = self._get_gt_da_request()
        self._cadastrar_avaliadores(gt.avaliadores)
        gt.put()
        self.redirect(url_entrou)
    
    def _cadastrar_avaliadores(self, emails):
        for i in emails:
            a = Usuario.get_or_create(i)
            a.add_credencial(ava)
            a.put()
            if a.key == self.usuario.key: # Caso o próprio usuário 
                self.usuario = a          # se cadastre como avaliador,
                                          # atualiza a memória para 
                                          # ficar consistente com o banco
        
    @requer_org
    def confirmar_excluir(self, sigla):
        sigla = str(urllib.unquote(sigla))
        valores = {'uri_sim' : '/del/gt/' + sigla,
                   'uri_nao' : '/meus/gt/',
                   'mensagem' : u'''Você está excluindo o grupo de trabalho %s.
                   Esta ação não pode ser desfeita!''' % sigla}
        self.responder('confirmacao.html', valores)
    
    @requer_org
    def excluir(self, sigla):
        sigla = str(urllib.unquote(sigla))
        #TODO: implementar exclusão (excluir dependências)
        sigla = str(urllib.unquote(sigla))
        gt = GrupoDeTrabalho.find_by_sigla(sigla)
        gt.key.delete()
        
        self.redirecionar(url_meus_gt, [u'O grupo de trabalho %s foi excluído.' % sigla])
    
    @requer_org
    def alterar_get(self, sigla):
        sigla = str(urllib.unquote(sigla))
        g = GrupoDeTrabalho.find_by_sigla(sigla)
        
        upload_url = blobstore.create_upload_url(url_alt_gt_post+'/'+sigla)
        
        emails_ava = util.string_list_para_string_rn(g.avaliadores)
        
        travado_checked = 'checked' if g.estado == travado else ''
        finalizado_checked = 'checked' if g.estado == finalizado else ''
        aceitando_avaliacoes_checked = 'checked' if g.estado == aceitando_avaliacoes else ''
        aceitando_submissoes_checked = 'checked' if g.estado == aceitando_submissoes else ''
        
        
        self.responder('alt_gt.html', {'value_nome' : g.nome,
            'value_sigla' : g.sigla, 'value_emails_ava' : emails_ava, 
            'value_n_ava_por_art' : g.n_ava_por_art, 'edital_key' : g.edital,
            'value_ini_sub' : g.ini_sub, 'value_fim_sub' : g.fim_sub,
            'value_ini_ava' : g.ini_ava, 'value_fim_ava' : g.fim_ava,
            
            
            'upload_url' : upload_url,
            
            'trav_checked' : travado_checked, 'fin_checked' : finalizado_checked,
            'aceit_ava_checked' : aceitando_avaliacoes_checked,
            'aceit_sub_checked' : aceitando_submissoes_checked,
            
            'travado' : travado, 'aceitando_submissoes' : aceitando_submissoes,
            'aceitando_avaliacoes' : aceitando_avaliacoes, 'finalizado' : finalizado})
    
    @requer_org
    def alterar_post(self, sigla):
        # TODO: Terminar de implementar
        # alterar sigla cria um novo
        sigla = str(urllib.unquote(sigla))
        gt = self._get_gt_da_request()
        antigo_gt = GrupoDeTrabalho.find_by_sigla(sigla)

        if antigo_gt:
            gt.key = antigo_gt.key
            if not gt.edital:
                gt.edital = antigo_gt.edital
        else:
            self.erro_404()
            
        print sigla
        print antigo_gt.key
        print gt.key

        self._cadastrar_avaliadores(gt.avaliadores)
        gt.put()
        self.redirecionar(url_meus_gt, [u'Grupo de trabalho alterado.'])
    
    def _get_gt_da_request(self):
        '''Instancia um GrupoDeTrabalho através do formulário preenchido.'''
        #self._validar_campos()
        
        nome = self.request.get('nome').strip()
        sigla = self.request.get('sigla').strip()
        ini_sub = util.str_para_date(self.request.get('ini_sub'))
        fim_sub = util.str_para_date(self.request.get('fim_sub'))
        ini_ava = util.str_para_date(self.request.get('ini_ava'))
        fim_ava = util.str_para_date(self.request.get('fim_ava'))
        n_ava_por_art = int(self.request.get('n_ava_por_art'))
        emails_ava = self.request.get('emails_ava')
        emails_ava = emails_ava.split('\r\n') # quebrando os emails dos 
                                              # avaliadores em uma lista
        emails_ava = list(set(emails_ava)) # retirando elementos repetidos
        estado = self.request.get('estado')
        
        # cria o gt
        gt = GrupoDeTrabalho(nome = nome, sigla = sigla, ini_sub = ini_sub,
            fim_sub = fim_sub, ini_ava = ini_ava, fim_ava = fim_ava)
        
        gt.estado = estado if estado else travado
        gt.n_ava_por_art = n_ava_por_art if n_ava_por_art else default_n_ava_por_art
        
        # pega o edital
        edital = None
        try:
            upload_files = self.get_uploads('file')
            blob_info = upload_files[0]
            edital = blob_info.key()
        except:
            pass
        gt.edital = edital
        
        gt.avaliadores = []
        for e in emails_ava: # cadastrando avaliadores
            e = e.strip()
            if e and e not in gt.avaliadores:
                gt.avaliadores += [e]        
        
        gt.organizador = self.usuario.email
        
        return gt
    
    def _validar_campos(self):
        '''Valida os campos do formulário de cadastro de GT.'''
        #TODO: refazer validação
        assert isinstance(self.request, webapp.Request), 'Requisição inválida.'
        # validação dos campos obrigatórios
        campos = ['nome','sigla','ini_sub','fim_sub','ini_ava','fim_ava',
            'emails_ava']
        for i in campos:
            campo = self.request.get(i).strip()
            assert campo, 'Campo obrigatório %s não preenchido.' % i
        # TODO: validar emails
    
    @requer_org
    def listar(self):
        '''Lista todos os grupos de trabalho ativos.'''
        grupos = GrupoDeTrabalho.query(GrupoDeTrabalho.estado != finalizado)
        self.responder('listar_gt.html', {'grupos' : grupos})
    
    def listar_meus(self):
        '''Lista todos os grupos de trabalho de um organizador.'''
        grupos = GrupoDeTrabalho.query(ancestor=ndb.Key(Usuario, self.usuario.email))
        self.responder('listar_meus_gt.html', {'grupos' : grupos})
    
    @requer_org
    def exibir(self, sigla):
        '''Exibe um GT.'''
        sigla = str(urllib.unquote(sigla))
        g = GrupoDeTrabalho.query().filter(GrupoDeTrabalho.sigla == sigla).get()
        if g:
            self.responder('gt.html', {'grupo' : g})
        else:
            self.erro_404()

