from database import Database
from usuario import Usuario
from funcionario import Funcionario
from gerente import Gerente
from crud import CRUD

# Função principal
def main():
    # Criando uma instância da classe CRUD para interagir com o banco de dados
    crud = CRUD("bolt://3.85.171.53:7687", "neo4j", "cavity-thin-properties")

    # Criando uma instância da classe Gerente
    gerente = Gerente("76.833.186/0001-21")

    #Menu de opções
    menu_options = {
        "1": crud.registrarColaborador,
        "2": crud.deletarColaborador,
        "3": crud.buscarColaborador,  # Adiciona a opção "Localizar colaborador"
        "4": crud.buscarTodosColaboradores,  # Adiciona a opção "Localizar todos os colaboradores"
        "5": exit
    }

    #Loop enquanto não selecionarmos 5
    while True:
        print("---- Sistema de Gestão 1.0 ----")
        print("1 - Registrar colaborador")
        print("2 - Deletar colaborador")
        print("3 - Logar como funcionário")
        print("4 - Logar como gerente")
        print("5 - Sair")
        print("----------------------------")

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
                salario = float(input("Digite o salário do colaborador: "))
                menu_options["1"](nome, cpf, email, salario)  # Passando o objeto crud, nome, cpf e email como argumentos
                continue
            else:
                print("Login inválido. Tente novamente.")
                continue

        elif opcao == "3":
            cpf = input("Digite o CPF do funcionário: ")
            email = input("Digite o email do funcionário: ")

            if crud.usuarioExiste(cpf, email):

                print("\nLogin realizado com sucesso!")
                while True:
                    print("\n---- Menu do Funcionário ====")
                    print("1 - Registrar compra")
                    print("2 - Deletar compra")
                    print("3 - Atualizar endereço")
                    print("4 - Voltar")
                    print("----------------------------")

                    opcao_funcionario = input("Digite o número da opção desejada: ")

                    if opcao_funcionario == "1":
                        cpf_funcionario = input("Digite o CPF do funcionário: ")
                        valor = float(input("Digite o valor total da compra: "))
                        produto = input("Digite o produto comprado: ")
                        id_compra = input("Digite o ID da compra: ")
                        crud.registrarCompra(cpf_funcionario, id_compra, valor, [produto])

                    elif opcao_funcionario == "2":
                        id_delete = input("Digite o ID da compra que deseja deletar: ")
                        crud.deletarCompra(id_delete)

                    elif opcao_funcionario == "3":
                        cpf_funcionario = input("Digite o CPF do funcionário: ")
                        rua = input("Digite o nome da rua: ")
                        bairro = input("Digite o nome do bairro: ")
                        cidade = input("Digite o nome da cidade: ")
                        crud.atualizarEndereco(cpf_funcionario, rua, bairro, cidade)

                    elif opcao_funcionario == "4":
                        # Volte ao menu principal
                        break
                    else:
                        print("Opção inválida. Tente novamente.")

            else:
                print("CPF ou email inválidos. Tente novamente.")


        elif opcao == "4":
            senha = input("Digite a senha da gerencia: ")
            gerente.login(senha)
            if gerente.estaLogado():
                while True:
                    print("\n---- Menu do Gerente ----")
                    print("1 - Histórico de registros")
                    print("2 - Compra total")
                    print("3 - Atualizar funcionário")
                    print("4 - Localizar colaborador")  # Adiciona a opção "Localizar colaborador"
                    print("5 - Localizar todos os colaboradores")  # Adiciona a opção "Localizar todos os colaboradores"
                    print("6 - Voltar")
                    print("----------------------------")

                    opcao_gerente = input("Digite o número da opção desejada: ")
                    if opcao_gerente == "1":
                        crud.historicoRegistros()

                    elif opcao_gerente == "2":
                        crud.compraTotal()

                    elif opcao_gerente == "3":
                        cpf_funcionario = input("Digite o CPF do funcionário: ")
                        crud.atualizarFuncionario(cpf_funcionario)

                    elif opcao_gerente == "4":
                        cpf_funcionario = input("Digite o CPF do funcionário: ")
                        colaborador = crud.buscarColaborador(cpf_funcionario)
                        if colaborador:
                            print("\n -- Colaborador encontrado --")
                            print("Nome:", colaborador['nome'])
                            print("CPF:", colaborador['cpf'])
                            print("Email:", colaborador['email'])
                            print("Salário:", colaborador['salario'])
                        else:
                            print("Colaborador não encontrado, tente outro CPF!")
                    elif opcao_gerente == "5":
                        colaboradores = crud.buscarTodosColaboradores()
                        if colaboradores:
                            print("\n -- Todos os Colaboradores --")
                            for colaborador in colaboradores:
                                print("Nome:", colaborador['nome'])
                                print("CPF:", colaborador['cpf'])
                                print("Email:", colaborador['email'])
                                print("Salário:", colaborador['salario'])
                            print("-------------------\n")
                        else:
                            print("Nenhum colaborador encontrado.")

                    elif opcao_gerente == "6":
                        # Volte ao menu principal
                        break
                    else:

                        print("Opção inválida. Tente novamente.")
            else:
                print("CNPJ inválido. Tente novamente.")

        elif opcao == "5":
            crud.close()
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
