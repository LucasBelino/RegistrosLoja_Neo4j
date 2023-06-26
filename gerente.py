from funcionario import Funcionario

class Gerente(Funcionario):
    def __init__(self, nome, cpf, email, salario, departamento):
        super().__init__(nome, cpf, email, salario)
        self.departamento = departamento
        self.logado = False

    def login(self):
        self.logado = True

    def estaLogado(self):
        return self.logado

    def registrarColaborador(self, crud):


    def deletarColaborador(self, crud):


    def registrarCompra(self, crud):


    def deletarCompra(self, crud):

