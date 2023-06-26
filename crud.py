from py2neo import Graph, Node
import re

class CRUD:
    def __init__(self, uri, username, password):
        self.graph = Graph(uri, auth=(username, password))

    def usuarioExiste(self, cpf, email):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' AND u.email = '{email}' RETURN count(u) as count"
        result = self.graph.run(query).data()
        return result[0]["count"] > 0

    def buscarColaborador(self, cpf):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' RETURN u"
        result = self.graph.run(query).data()
        return result[0]["u"] if result else None

    def buscarTodosColaboradores(self):
        query = "MATCH (u:Usuario) RETURN u"
        result = self.graph.run(query).data()
        return [record["u"] for record in result]

    def validar_cpf(self, cpf):
        # Remove caracteres especiais do CPF
        cpf = re.sub(r'[^0-9]', '', cpf)

        # Verifica se o CPF possui 11 dígitos
        if len(cpf) != 11:
            return False

        # Verifica se todos os dígitos do CPF são iguais
        if cpf == cpf[0] * 11:
            return False

        # Verifica se o CPF é válido utilizando a fórmula de validação
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = (soma * 10) % 11
        if resto == 10:
            resto = 0
        if resto != int(cpf[9]):
            return False
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = (soma * 10) % 11
        if resto == 10:
            resto = 0
        if resto != int(cpf[10]):
            return False

        return True

    def validar_email(self, email):
        # Expressão regular para validar o email
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        # Verifica se o email corresponde ao padrão
        return re.match(padrao, email) is not None

    def registrarColaborador(self, nome, cpf, email):
        # Valida o CPF
        if not self.validar_cpf(cpf):
            print("CPF inválido. Insira um CPF válido no formato (123.456.789-00).")
            return

        # Valida o email
        if not self.validar_email(email):
            print("Email inválido. Insira um email válido no formato (nome@nome.nome).")
            return

        node = Node("Usuario", nome=nome, cpf=cpf, email=email)
        self.graph.create(node)
        print("\nColaborador registrado com sucesso!")
        print("Agora o colaborador pode logar usando seu CPF e email.\n")

    def deletarColaborador(self, cpf):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' DELETE u"
        self.graph.run(query)

    def registrarCompra(self, cpf, valor, produto, id):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' CREATE (u)-[:COMPRA {{valor: {valor}, produto: '{produto}', id: '{id}'}}]->(c:Compra)"
        self.graph.run(query)

    def deletarCompra(self, id):
        query = f"MATCH (u:Usuario)-[r:COMPRA]->(c:Compra) WHERE c.id = '{id}' DELETE r, c"
        self.graph.run(query)
