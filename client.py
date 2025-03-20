import socket

# Função que exibe o menu e captura a opção do usuário
def exibir_menu():
    print("\n===== MENU =====")
    print("1. Criar Tarefa")
    print("2. Editar Tarefa")
    print("3. Deletar Tarefa")
    print("4. Listar Tarefas")
    print("5. Concluir Tarefa")
    print("6. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

# Função que envia comandos para o servidor e retorna a resposta
def enviar_comando(cliente, comando):
    cliente.sendall(comando.encode())
    resposta = cliente.recv(4096).decode()
    return resposta

# Função principal que conecta o cliente ao servidor e executa as opções
def main():
    # Conecta ao servidor na porta 5000
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('127.0.0.1', 5000))
    print("Conectado ao servidor de tarefas!")

    while True:
        opcao = exibir_menu()

        if opcao == "1":
            descricao = input("Digite a descrição da tarefa: ")
            # Envia o comando para criar uma nova tarefa
            resposta = enviar_comando(cliente, f"CRIAR_TAREFA {descricao}")
            print(resposta)
        
        elif opcao == "2":
            id_tarefa = input("Digite o ID da tarefa a ser editada: ")
            nova_descricao = input("Digite a nova descrição: ")
            resposta = enviar_comando(cliente, f"EDITAR_TAREFA {id_tarefa} {nova_descricao}")
            print(resposta)

        elif opcao == "3":
            id_tarefa = input("Digite o ID da tarefa a ser deletada: ")
            resposta = enviar_comando(cliente, f"DELETAR_TAREFA {id_tarefa}")
            print(resposta)

        elif opcao == "4":
            # Solicita a lista de tarefas ao servidor
            resposta = enviar_comando(cliente, "LISTAR_TAREFAS")
            print("\n===== TAREFAS =====")
            print(resposta)

        elif opcao == "5":
            id_tarefa = input("Digite o ID da tarefa a ser concluída: ")
            resposta = enviar_comando(cliente, f"CONCLUIR_TAREFA {id_tarefa}")
            print(resposta)

        elif opcao == "6":
            print("Encerrando o cliente...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    cliente.close()

if __name__ == "__main__":
    main()
