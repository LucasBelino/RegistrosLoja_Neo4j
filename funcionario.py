from usuario import Usuario

class Funcionario(Usuario):
    def __init__(self, cpf, email, salario=None):
        super().__init__(cpf)
        self.email = email
        self.salario = salario
