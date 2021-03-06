#-*- coding:utf-8 -*-
from valores import *
from gaesessions import get_current_session
from custom_jinja import jinja_env

__all__ = ['BaseHandler']

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

