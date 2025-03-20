import socket
import threading
from threading import Semaphore

# Classe que representa uma tarefa na lista encadeada
class Tarefa:
    def __init__(self, id, descricao):
        self.id = id
        self.descricao = descricao
        self.concluida = False
        self.proxima = None
        self.anterior = None

# Lista duplamente encadeada para armazenar as tarefas
class ListaTarefas:
    def __init__(self):
        self.head = None
        self.tail = None
        self.lock = Semaphore()
        self.proximo_id = 1

    # Adiciona uma nova tarefa à lista
    def adicionar_tarefa(self, descricao):
        self.lock.acquire()
        try:
            nova = Tarefa(self.proximo_id, descricao)
            self.proximo_id += 1

            if self.head is None:
                self.head = self.tail = nova
            else:
                self.tail.proxima = nova
                nova.anterior = self.tail
                self.tail = nova
            return nova.id
        finally:
            self.lock.release()

    # Edita a descrição de uma tarefa existente
    def editar_tarefa(self, id_tarefa, nova_descricao):
        self.lock.acquire()
        try:
            atual = self.head
            while atual:
                if atual.id == id_tarefa:
                    atual.descricao = nova_descricao
                    return True
                atual = atual.proxima
            return False
        finally:
            self.lock.release()

    # Deleta uma tarefa da lista pelo ID
    def deletar_tarefa(self, id_tarefa):
        self.lock.acquire()
        try:
            atual = self.head
            while atual:
                if atual.id == id_tarefa:
                    if atual.anterior:
                        atual.anterior.proxima = atual.proxima
                    else:
                        self.head = atual.proxima
                    if atual.proxima:
                        atual.proxima.anterior = atual.anterior
                    else:
                        self.tail = atual.anterior
                    return True
                atual = atual.proxima
            return False
        finally:
            self.lock.release()

    # Lista todas as tarefas
    def listar_tarefas(self):
        self.lock.acquire()
        try:
            resultado = ""
            atual = self.head
            while atual:
                status = "CONCLUÍDA" if atual.concluida else "PENDENTE"
                resultado += f"{atual.id}: {atual.descricao} [{status}]\n"
                atual = atual.proxima
            return resultado if resultado else "Nenhuma tarefa cadastrada."
        finally:
            self.lock.release()

    # Marca uma tarefa como concluída
    def concluir_tarefa(self, id_tarefa):
        self.lock.acquire()
        try:
            atual = self.head
            while atual:
                if atual.id == id_tarefa:
                    atual.concluida = True
                    return True
                atual = atual.proxima
            return False
        finally:
            self.lock.release()

# Classe principal do servidor de tarefas
class ServidorTarefas:
    def __init__(self, host='127.0.0.1', porta=5000):
        self.host = host
        self.porta = porta
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.host, self.porta))
        self.servidor.listen()
        print(f"Servidor rodando em {self.host}:{self.porta}")
        self.lista_tarefas = ListaTarefas()

    # Lida com cada cliente em uma thread separada
    def lidar_com_cliente(self, conn, addr):
        print(f"Conexão estabelecida com {addr}")
        with conn:
            while True:
                try:
                    dados = conn.recv(1024)
                    if not dados:
                        break
                    comando = dados.decode().strip()
                    resposta = self.processar_comando(comando)
                    conn.sendall(resposta.encode())
                except Exception as e:
                    print(f"Erro na conexão com {addr}: {e}")
                    break

    # Processa o comando recebido do cliente
    def processar_comando(self, comando):
        partes = comando.split(" ", 2)
        acao = partes[0]

        if acao == "CRIAR_TAREFA" and len(partes) == 2:
            id_tarefa = self.lista_tarefas.adicionar_tarefa(partes[1])
            return f"OK Tarefa criada com ID {id_tarefa}: {partes[1]}"

        elif acao == "EDITAR_TAREFA" and len(partes) == 3:
            try:
                id_tarefa = int(partes[1])
            except ValueError:
                return "ERRO ID inválido"
            sucesso = self.lista_tarefas.editar_tarefa(id_tarefa, partes[2])
            return "OK Tarefa editada" if sucesso else "ERRO Tarefa não encontrada"

        elif acao == "DELETAR_TAREFA" and len(partes) == 2:
            try:
                id_tarefa = int(partes[1])
            except ValueError:
                return "ERRO ID inválido"
            sucesso = self.lista_tarefas.deletar_tarefa(id_tarefa)
            return "OK Tarefa deletada" if sucesso else "ERRO Tarefa não encontrada"

        elif acao == "LISTAR_TAREFAS":
            return self.lista_tarefas.listar_tarefas()

        elif acao == "CONCLUIR_TAREFA" and len(partes) == 2:
            try:
                id_tarefa = int(partes[1])
            except ValueError:
                return "ERRO ID inválido"
            sucesso = self.lista_tarefas.concluir_tarefa(id_tarefa)
            return "OK Tarefa concluída" if sucesso else "ERRO Tarefa não encontrada"

        else:
            return "ERRO Comando inválido"

    # Inicia o loop principal do servidor aceitando conexões
    def iniciar(self):
        while True:
            conn, addr = self.servidor.accept()
            thread = threading.Thread(target=self.lidar_com_cliente, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    servidor = ServidorTarefas()
    servidor.iniciar()
