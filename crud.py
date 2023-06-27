from py2neo import Graph, Node
from endereco import Endereco
from database import Database
import re

class CRUD:
    def __init__(self, bolt_url, username, password):
        self.db = Database(bolt_url, username, password)
        self.graph = Graph(bolt_url, auth=(username, password))

    #Verificação da existencia do usuario
    def usuarioExiste(self, cpf, email):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' AND u.email = '{email}' RETURN count(u) as count"
        result = self.graph.run(query).data()
        return result[0]["count"] > 0

    #Buscando colaborador especifico através do CPF
    def buscarColaborador(self, cpf):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' RETURN u"
        result = self.graph.run(query).data()
        return result[0]["u"] if result else None

    #Buscando todos os colaboradores
    def buscarTodosColaboradores(self):
        query = "MATCH (u:Usuario) RETURN u"
        result = self.graph.run(query).data()
        return [record["u"] for record in result]

    #Validação de CPF
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

    #Validação de email
    def validar_email(self, email):
        # Expressão regular para validar o email
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        # Verifica se o email corresponde ao padrão
        return re.match(padrao, email) is not None

    #Registro de Colaborador
    def registrarColaborador(self, nome, cpf, email, salario):
        # Valida o CPF
        if not self.validar_cpf(cpf):
            print("CPF inválido. Insira um CPF válido no formato (123.456.789-00).")
            return

        # Valida o email
        if not self.validar_email(email):
            print("Email inválido. Insira um email válido no formato (nome@nome.nome).")
            return

        node = Node("Usuario", nome=nome, cpf=cpf, email=email, salario=salario) #nó do funcionário
        self.graph.create(node)
        print("\nColaborador registrado com sucesso!")
        print("Agora o colaborador pode logar usando seu CPF e email.\n")

    #Deletando um colaborador através do CPF
    def deletarColaborador(self, cpf):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' DELETE u"
        self.graph.run(query)
        print(f"Colaborador {cpf} deletado com sucesso!\n")

    #Registrando uma compra
    def registrarCompra(self, cpf, id_compra, valor, produtos):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' " \
                f"CREATE (u)-[:REGISTROU]->(c:Compra {{id: '{id_compra}', valor: '{valor}'}})"

        self.graph.run(query)

        for produto in produtos:
            query = f"MATCH (c:Compra) WHERE c.id = '{id_compra}' " \
                    f"CREATE (c)-[:PRODUTO]->(:Produto {{nome: '{produto}'}})"

            self.graph.run(query)
        print(f"Compra registrada no CPF {cpf} com sucesso!")

    #Deletando uma compra
    def deletarCompra(self, id_compra):
        query = f"MATCH (c:Compra)-[r:PRODUTO]->(p:Produto) WHERE c.id = '{id_compra}' DETACH DELETE c, r, p"
        self.graph.run(query)
        print("Compra deletada com sucesso.")

    #Atualizando o endereco de um funcionario
    def atualizarEndereco(self, cpf_funcionario, rua, bairro, cidade):
        endereco = Endereco(rua, bairro, cidade)
        query = (
            "MATCH (u:Usuario {cpf: $cpf_funcionario}) "
            "CREATE (u)-[:MORA_EM]->(:Endereco {rua: $rua, bairro: $bairro, cidade: $cidade})"
        )
        parameters = {
            "cpf_funcionario": cpf_funcionario,
            "rua": endereco.rua,
            "bairro": endereco.bairro,
            "cidade": endereco.cidade
        }
        self.graph.run(query, parameters)
        print("Endereço atualizado com sucesso!")

    #Puxando o historico de todas as compras registradas
    def historicoRegistros(self):
        query = "MATCH (f:Usuario)-[:REGISTROU]->(c:Compra) RETURN f, c"
        result = self.graph.run(query).data()

        if not result:
            print("Nenhum registro de compra encontrado.")
            return

        print("\n---- Histórico de Registros ----")
        for record in result:
            funcionario = record['f']
            compra = record['c']
            print("CPF de quem registrou:", funcionario['cpf'])
            print("Nome do funcionário:", funcionario['nome'])
            print("ID da compra:", compra['id'])
            print("Valor da compra:", compra['valor'])
            print("\n")
        print("---------------------------------")

    #Total em valor de todas as compras
    def compraTotal(self):
        query = "MATCH (c:Compra) RETURN toFloat(sum(toFloat(c.valor))) as total"
        result = self.graph.run(query).data()

        if not result or not result[0]['total']:
            print("Nenhum registro de compra encontrado.")
            return

        total = result[0]['total']
        print("\n---- Compra Total ----")
        print("Valor total das compras R$", total)

    #Atualizando Funcionario através da busca pelo cpf
    def atualizarFuncionario(self, cpf):
        node = self.buscarColaborador(cpf)
        if not node:
            print("Funcionário não encontrado.")
            return

        print("Atualizando informações do funcionário:")
        print("Nome:", node['nome'])
        print("CPF:", node['cpf'])
        print("Email:", node['email'])
        print("Salário:", node['salario'])

        print("\nInsira as novas informações do funcionário:")
        nome = input("Nome: ")
        email = input("Email: ")
        salario = input("Salário: ")

        query = (
            f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' "
            f"SET u.nome = '{nome}', u.email = '{email}', u.salario = '{salario}'"
        )
        self.graph.run(query)
        print("Informações do funcionário atualizadas com sucesso!")
