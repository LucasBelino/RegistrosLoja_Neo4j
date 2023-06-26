from usuario import Usuario

class Funcionario(Usuario):
    def __init__(self, nome, cpf, email, salario):
        super().__init__(nome, cpf, email)
        self.salario = salario
