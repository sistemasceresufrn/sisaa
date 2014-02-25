#-*- coding:utf-8 -*-
import jinja2, os, util, re, urllib, valores

from google.appengine.ext import ndb

from google.appengine.ext import webapp, blobstore
from google.appengine.ext.webapp import blobstore_handlers

from modelo import Usuario, GrupoDeTrabalho, Artigo
from valores import *
from urls import *

from gaesessions import get_current_session
from auth import *
from webapp2_extras.security import hash_password


jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler():
    '''Handler base que todos os outros devem extender. Possui os métodos
    implementados, mas não pode ser usado diretamente porque não extende
    nenhum handler (do webapp ou blobstore). Isso acontece justamente para
    deixar o programador livre para escolher qual handler extender junto
    com este.'''
    
    @property
    def sessao(self):
        '''Propriedade que dá acesso à sessão.
        :returns:
                A sessão.'''
        return get_current_session()
    
    def requer_permissao(self):
        '''Exibe uma página dizendo que o usuário não tem permissão para
        acessar uma parte do sistema.'''
        self.responder('req_permissao.html')
    
    def responder(self, pagina, valores={}):
        '''Exibe uma página para o usuário.
        - Se existirem mensagens no handler, as mensagens são exibidas na 
        página e apagadas do self.
        - O parâmetro self.usuário é automaticamente passado para os 
        valores com a chave 'usuario'.
        :param pagina:
            String dizendo o nome da página a ser renderizada.
        :param valores:
            Dicionário contendo os valores a serem renderizados na página.
        '''
        valores['usuario'] = self.usuario
        valores['msgs'] = self.mensagens
        self.mensagens = []
        self.response.out.write(jinja_env.get_template(pagina).render(valores))

    def _get_usuario(self):
        '''Acessa o usuário na sessão. Não use esse método diretamente;
        em vez disso, faça self.usuario.
        :returns:
            O usuário atual.'''
        if self.sessao.is_active():
            try:
                u = self.sessao['usuario']
            except:
                u = None
            return u
        else:
            None

    def _set_usuario(self, usuario):
        '''Seta o usuário na sessão. Não use esse método diretamente;
        em vez disso, faça self.usuario = alguma_coisa.'''
        self.sessao['usuario'] = usuario

    def _get_mensagens(self):
        '''Acessa as mensagens na sessão. Não use esse método diretamente;
        em vez disso, faça self.mensagens.
        :returns:
            As mensagens. Uma list.'''
        if self.sessao.is_active():
            try:
                m = self.sessao['mensagens']
            except:
                m = []
            return m
        else:
            return []

    def _set_mensagens(self, mensagens):
        '''Seta as mensagens na sessão. Não use esse método diretamente;
        em vez disso, faça self.mensagens = alguma_coisa.'''
        self.sessao['mensagens'] = mensagens
        
    usuario = property(_get_usuario, _set_usuario)
    
    mensagens = property(_get_mensagens, _set_mensagens)

    def erro_404(self):
        '''Renderiza uma página de erro 404 amigável para o usuário.'''
        self.responder('erro_404.html')
        
    def requer_permissao(self):
        '''Exibe a página que diz que o usuário não tem permissão para fazer algo.'''
        self.responder('req_permissao.html')

    def redirecionar(self, uri, mensagens=[]):
        '''Redireciona o usuário para uma url.
        :param uri:
            A uri aonde irá redirecionar. Uma string.
        :param mensagens:
            Mensagens a serem exibidas na página. Uma list.'''
        self.mensagens = mensagens
        self.redirect(uri)

class EntrouHandler(BaseHandler, webapp.RequestHandler):
    '''Handler criado para testes. Será apagado futuramente.'''
    @requer_login
    def get(self):
        user = self.usuario
        self.responder('entrou.html', dict(u = user,
            admin_checked = 'checked' if adm in user.credenciais else '',
            aluno_checked = 'checked' if alu in user.credenciais else '',
            aval_checked = 'checked' if ava in user.credenciais else '',
            org_checked = 'checked' if org in user.credenciais else '',))
    
    @requer_login
    def post(self):
        u = self.usuario
        
        cred = [] # credenciais marcadas
        if self.request.get(adm) == 'on': # on é a constante passada pelo html
            cred += [adm]
        if self.request.get(alu) == 'on':
            cred += [alu]
        if self.request.get(ava) == 'on':
            cred += [ava]
        if self.request.get(org) == 'on':
            cred += [org]
        
        u.credenciais = cred
        self.usuario = u
        self.usuario.put()
        
        self.redirect(url_entrou)

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

class InicioHandler(BaseHandler, webapp.RequestHandler):
    '''Trata as requisições da página inicial'''
    def get(self):
        self.responder('inicio.html')

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
        self.redirect('/entrou')
    
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
            'uri_sim' : url_del_org + '/' + email,
            'uri_nao' : url_list_org
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

class GTHandler(BaseHandler, blobstore_handlers.BlobstoreUploadHandler):
    '''Handler que gerencia grupos de trabalho'''

    @requer_org
    def cadastrar_get(self):
        valores = {'upload_url' : blobstore.create_upload_url('/up/gt')}
        self.responder('cad_gt.html',valores)
    
    @requer_org
    def cadastrar_post(self):
        self._validar_campos()
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
            'value_sigla' : g.sigla, 'value_ini_sub' : g.ini_sub,
            'value_fim_sub' : g.fim_sub, 'value_ini_ava' : g.ini_ava,
            'value_fim_ava' : g.fim_ava, 'value_emails_ava' : emails_ava, 
            'edital_key' : g.edital,
            
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
        emails_ava = self.request.get('emails_ava')
        emails_ava = emails_ava.split('\r\n') # quebrando os emails dos 
                                              # avaliadores em uma lista
        emails_ava = list(set(emails_ava)) # retirando elementos repetidos
        estado = self.request.get('estado')
        
        # cria o gt
        gt = GrupoDeTrabalho(nome = nome, sigla = sigla, ini_sub = ini_sub,
            fim_sub = fim_sub, ini_ava = ini_ava, fim_ava = fim_ava)
        
        gt.estado = estado if estado else travado
        
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
        
class ArtigoHandler(BaseHandler, webapp.RequestHandler):
    #TODO: fazer upload de artigos através deste handler.
    '''Gerencia as páginas relacionadas a artigos. Não trada do upload 
    ainda, esse trabalho é feito no UploadHandler.'''
    @requer_alu
    def enviar(self, sigla):
        sigla = str(urllib.unquote(sigla))
        url = blobstore.create_upload_url(url_up_art)
        grupo = GrupoDeTrabalho.find_by_sigla(sigla)
        if grupo:
            self.responder('enviar_artigo.html', {'upload_url' : url,
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
        artigos = Artigo.query(Artigo.autor == self.usuario.email)
        self.responder('listar_artigos.html', {'artigos' : artigos})

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
            autor=self.usuario.email,
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

#TODO: implementar UsuarioHandler para alterar seus dados
