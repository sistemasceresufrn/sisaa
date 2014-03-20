# -*- coding:utf-8 -*-
import util, re, urllib, random

from google.appengine.ext import ndb
from google.appengine.ext import webapp, blobstore
from google.appengine.ext.webapp import blobstore_handlers

from modelo import *
from valores import *
from urls import url

from gaesessions import get_current_session
from auth import *
from webapp2_extras.security import hash_password

from base import BaseHandler

__all__ = ['GTHandler']

class GTHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    '''Handler que gerencia grupos de trabalho'''

    @requer_org
    def cadastrar_get(self):
        valores = {'upload_url' : blobstore.create_upload_url(url['cad_gt_post'])}
        self.responder('cad_gt.html',valores)
    
    @requer_org
    def cadastrar_post(self):
        #self._validar_campos()
        gt = self._get_gt_da_request()
        self._cadastrar_avaliadores(gt.avaliadores)
        gt.put()
        self.redirect(url['entrou'])
    
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
        
        self.redirecionar(url['meus_gt'], [u'O grupo de trabalho %s foi excluído.' % sigla])
    
    @requer_org
    def alterar_get(self, sigla):
        sigla = str(urllib.unquote(sigla))
        g = GrupoDeTrabalho.find_by_sigla(sigla)
        
        upload_url = blobstore.create_upload_url(url['alt_gt_post']+'/'+sigla)
        
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
        self.redirecionar(url['meus_gt'], [u'Grupo de trabalho alterado.'])
    
    def _get_gt_da_request(self):
        '''Instancia um GrupoDeTrabalho através do formulário preenchido.'''
        #self._validar_campos()
        
        nome = self.request.get('nome').strip()
        sigla = self.request.get('sigla').strip()
        ini_sub = util.str_para_date(self.request.get('ini_sub'))
        fim_sub = util.str_para_date(self.request.get('fim_sub'))
        ini_ava = util.str_para_date(self.request.get('ini_ava'))
        fim_ava = util.str_para_date(self.request.get('fim_ava'))
        n_ava_por_art = self.request.get('n_ava_por_art')
        emails_ava = self.request.get('emails_ava')
        emails_ava = emails_ava.split('\r\n') # quebrando os emails dos 
                                              # avaliadores em uma lista
        emails_ava = list(set(emails_ava)) # retirando elementos repetidos
        estado = self.request.get('estado')
        
        # cria o gt
        gt = GrupoDeTrabalho(nome = nome, sigla = sigla, ini_sub = ini_sub,
            fim_sub = fim_sub, ini_ava = ini_ava, fim_ava = fim_ava)
        
        gt.estado = estado if estado else travado
        gt.n_ava_por_art = int(n_ava_por_art) if n_ava_por_art else default_n_ava_por_art
        
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
        pass
    
    @requer_org
    def listar(self):
        '''Lista todos os grupos de trabalho ativos.'''
        grupos = GrupoDeTrabalho.query(GrupoDeTrabalho.estado != finalizado)
        self.responder('listar_gt.html', {'grupos' : grupos})
    
    @requer_org
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

    @requer_org
    def distribuir(self, sigla):
        '''Distribui os artigos para os avaliadores.'''
        sigla = str(urllib.unquote(sigla))
        gt = GrupoDeTrabalho.find_by_sigla(sigla)
        
        # pegando todos os avaliadores do gt como list de Usuario
        list_ava = []
        for email in gt.avaliadores:
            ava = Usuario.find_by_email(email)
            list_ava += [ava]
        
        if gt.n_ava_por_art > len(list_ava):
            self.responder('mensagem.html', {'titulo' : u'Erro', 
                'mensagem' : u'''O número de avaliadores por artigo excede
                             o total de avaliadores do grupo de trabalho.
                             Cadastre mais avaliadores ou diminua o número 
                             de avaliadores por artigo.''',
                'url_voltar' : url['meus_gt']})
            return
        
        # Aqui é a lógica em si de sorteio dos avaliadores para os artigos
        random.shuffle(list_ava)
        
        artigos = Artigo.query(Artigo.sigla_gt == sigla)
        
        i = 0 # índice de acesso aos elementos da lista de avaliadores
        tam = len(list_ava) # tamanho da lista de avaliadores
        
        for art in artigos:
             for n in range(gt.n_ava_por_art):
                Avaliacao(art_key = art.key,
                          ava_key = list_ava[i % tam].key).put()
                i += 1
        
        self.redirecionar(url['meus_gt'],
            [u'Os artigos foram distribuídos para os avaliadores'])
   
    @requer_org
    def ver_resultados(self, sigla):
        sigla = str(urllib.unquote(sigla))
        gt = GrupoDeTrabalho.find_by_sigla(sigla)
        
        self.responder('resultados.html',
            {'gt': gt, 'aceito' : aceito, 'recusado': recusado,
             'aceito_com_correcoes' : aceito_com_correcoes})
    
    @requer_org
    def salvar_resultados(self, sigla):
        sigla = str(urllib.unquote(sigla))
        gt = GrupoDeTrabalho.find_by_sigla(sigla)
        self._salvar_situacoes_da_request(gt)
        
        # TODO: descobrir por que se fizer isto, fica inconsistente com o banco
        # self.redirecionar(url['res'] % sigla, [u'Suas alterações foram salvas.'])
        self.redirecionar(url['entrou'])
    
    @requer_org
    def finalizar(self, sigla):
        sigla = str(urllib.unquote(sigla))
        gt = GrupoDeTrabalho.find_by_sigla(sigla)
        self._salvar_situacoes_da_request(gt)
        gt.estado = finalizado
        gt.put()
        self.redirecionar(url['meus_gt'],
            [u'O grupo de trabalho %s foi finalizado.' % gt.sigla])
    
    def _salvar_situacoes_da_request(self, gt):
        for art in gt.artigos: # marcando os artigos no banco
            selecao = self.request.get(art.key.urlsafe())
            art.situacao = selecao
            art.put()
