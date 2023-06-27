class Endereco:
    def __init__(self, rua, bairro, cidade):
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade

    def __str__(self):
        return f"Rua: {self.rua}, Bairro: {self.bairro}, Cidade: {self.cidade}"
