from database import Database
from usuario import Usuario
from funcionario import Funcionario
from gerente import Gerente
from crud import CRUD

# Função principal
def main():
    # Criando uma instância da classe CRUD para interagir com o banco de dados
    crud = CRUD("bolt://3.80.138.131:7687", "neo4j", "captains-salutes-oxygens")

    # Criando uma instância da classe Gerente
    gerente = Gerente("Nome do Gerente", "CPF do Gerente", "Email do Gerente", "Salário do Gerente", "Departamento do Gerente")

    menu_options = {
        "1": gerente.registrarColaborador,
        "2": gerente.deletarColaborador,
        "3": None,  # Será atualizado após o login
        "4": None,  # Será atualizado após o login
        "5": exit
    }

    while True:
        print("==== Menu ====")
        print("1 - Registrar colaborador")
        print("2 - Deletar colaborador")
        print("3 - Logar como funcionário")
        print("4 - Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1" or opcao == "2":
            gerente.login()
            if gerente.estaLogado():
                if opcao == "1":
                    gerente.registrarColaborador(crud)
                else:
                    gerente.deletarColaborador(crud)
            else:
                print("Login inválido. Tente novamente.")

        elif opcao == "3":
            cpf = input("Digite o CPF do funcionário: ")
            email = input("Digite o email do funcionário: ")

            if crud.usuarioExiste(cpf, email):
                funcionario = Funcionario(cpf, email)
                menu_options["3"] = funcionario.registrarCompra
                menu_options["4"] = funcionario.deletarCompra
                print("Login realizado com sucesso!")
            else:
                print("CPF ou email inválidos. Tente novamente.")

        elif opcao == "5":
            break

        else:
            print("Opção inválida. Tente novamente.")

    # Fechando a conexão com o banco de dados
    crud.close()

# Executando a função principal
if __name__ == "__main__":
    main()
