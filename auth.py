# -*- coding:utf-8 -*-

def requer_login(metodo):
    """Decorador que requer que o usuário esteja logado para acessar o 
    método do handler.
    """
    def check_login(self, *args, **kwargs):
        if not self.usuario:
            return self.redirect('/requer_permissao')
        else:
            metodo(self, *args, **kwargs)
    return check_login

#TODO: implementar daqui pra baixo
def requer_adm(metodo):
    def check_login(self, *args, **kwargs):
        if not self.usuario:
            return self.redirect('/requer_permissao')
        elif 'adm' not in self.usuario.credenciais:
            return self.redirect('/requer_permissao')
        else:
            metodo(self, *args, **kwargs)
    return check_login
    
def requer_ava(metodo):
    def check_login(self, *args, **kwargs):
        if not self.usuario:
            return self.redirect('/requer_permissao')
        elif 'ava' not in self.usuario.credenciais:
            return self.redirect('/requer_permissao')
        else:
            metodo(self, *args, **kwargs)
    return check_login
    
def requer_alu(metodo):
    def check_login(self, *args, **kwargs):
        if not self.usuario:
            return self.redirect('/requer_permissao')
        elif 'alu' not in self.usuario.credenciais:
            return self.redirect('/requer_permissao')
        else:
            metodo(self, *args, **kwargs)
    return check_login
    
def requer_org(metodo):
    def check_login(self, *args, **kwargs):
        if not self.usuario:
            return self.redirect('/requer_permissao')
        elif 'org' not in self.usuario.credenciais:
            return self.redirect('/requer_permissao')
        else:
            metodo(self, *args, **kwargs)
    return check_login
