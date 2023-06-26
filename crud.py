from py2neo import Graph, Node

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

    def registrarColaborador(self, nome, cpf, email):
        node = Node("Usuario", nome=nome, cpf=cpf, email=email)
        self.graph.create(node)

    def deletarColaborador(self, cpf):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' DELETE u"
        self.graph.run(query)

    def registrarCompra(self, cpf, valor, produto, id):
        query = f"MATCH (u:Usuario) WHERE u.cpf = '{cpf}' CREATE (u)-[:COMPRA {{valor: {valor}, produto: '{produto}', id: '{id}'}}]->(c:Compra)"
        self.graph.run(query)

    def deletarCompra(self, id):
        query = f"MATCH (u:Usuario)-[r:COMPRA]->(c:Compra) WHERE c.id = '{id}' DELETE r, c"
        self.graph.run(query)
