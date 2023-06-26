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
    gerente = Gerente("76.833.186/0001-21")

    menu_options = {
        "1": crud.registrarColaborador,
        "2": crud.deletarColaborador,
        "3": None,  # Será atualizado após o login
        "4": None,  # Será atualizado após o login
        "5": exit
    }

    while True:
        print("==== Menu ====")
        print("1 - Registrar colaborador")
        print("2 - Deletar colaborador")
        print("3 - Logar como funcionário")
        print("4 - Sair\n")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            senha = input("Digite a senha do Gerente: ")
            gerente.login(senha)
            if gerente.estaLogado():
                cpf = input("Digite o CPF do colaborador: ")
                if not crud.validar_cpf(cpf):
                    print("CPF inválido. Insira um CPF válido no formato (123.456.789-00).")
                    continue
                email = input("Digite o email do colaborador: ")
                if not crud.validar_email(email):
                    print("Email inválido. Insira um email válido no formato (nome@nome.nome).")
                    continue
                nome = input("Digite o nome do colaborador: ")
                menu_options["1"](nome, cpf, email)  # Passando o objeto crud, nome, cpf e email como argumentos
                continue
            else:
                print("Login inválido. Tente novamente.")
                continue

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

        elif opcao == "4":
            crud.close()  # Fechando a conexão com o banco de dados
            break

        else:
            print("Opção inválida. Tente novamente.")

    # Executando a função principal
if __name__ == "__main__":
    main()


