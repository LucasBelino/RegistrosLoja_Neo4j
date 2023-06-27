from usuario import Usuario

class Gerente(Usuario):
    def __init__(self, cnpj):
        self.cnpj = cnpj
        self.logado = False  # Atributo para indicar se o gerente está logado

    def login(self, senha):
        # Verifica se a senha está correta
        if senha == "SYSTEM23!":
            self.logado = True
            print("Login realizado com sucesso!")
        else:
            self.logado = False
            print("Login inválido. Tente novamente.")

    def estaLogado(self):
        return self.logado