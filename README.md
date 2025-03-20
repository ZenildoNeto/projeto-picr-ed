# Gerenciador de Tarefas Compartilhado

## Título do Projeto
**Gerenciador de Tarefas Compartilhado**

## Autores
- **[Seu Nome]** - [Seu E-mail]
- **[Outros Integrantes]** - [E-mail]

## Disciplinas Envolvidas
- **Estruturas de Dados** - Prof. [Nome do Docente]
- **Protocolos de Interconexão de Redes de Computadores** - Prof. [Nome do Docente]

---

## Descrição do Problema
Este projeto é um **Gerenciador de Tarefas Compartilhado**, onde múltiplos usuários podem criar, editar, concluir e remover tarefas em um ambiente colaborativo. Utilizando **Sockets TCP/IP**, o servidor gerencia as requisições simultâneas dos clientes e mantém a consistência dos dados.

---

## Arquivos do Projeto
| Nome do Arquivo | Descrição |
|----------------|-----------|
| `server.py` | Implementação do servidor que gerencia as tarefas e responde às requisições dos clientes. |
| `client.py` | Implementação do cliente, que permite interação com o servidor via terminal. |
| `README.md` | Documentação do projeto, explicando seu funcionamento e como rodá-lo. |
| `tarefas.py` | Estruturas de dados utilizadas para armazenar e gerenciar as tarefas. |

---

## Pré-requisitos para Execução
Para rodar o projeto, é necessário instalar os seguintes pacotes:

| Pacote | Propósito | Comando de Instalação |
|--------|----------|----------------------|
| Python 3 | Interpretador necessário para rodar os scripts. | [Baixar e instalar](https://www.python.org/) |

Se Python já estiver instalado, verifique a versão com:
```sh
python --version
```

---

## Instruções para Execução
### 1. Clonar o Repositório
```sh
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA>
```

### 2. Executar o Servidor
```sh
python server.py
```
O servidor rodará no **IP 127.0.0.1** e na **porta 5000**.

### 3. Executar o Cliente
Abra um novo terminal e rode:
```sh
python client.py
```
Agora você pode interagir com o sistema e gerenciar suas tarefas!

---

## Protocolo da Aplicação
A comunicação entre cliente e servidor segue um protocolo baseado em mensagens de texto:

### Comandos do Cliente
| Comando | Descrição | Exemplo |
|---------|-------------|---------|
| `CRIAR_TAREFA <descricao>` | Cria uma nova tarefa. | `CRIAR_TAREFA "Finalizar relatório"` |
| `EDITAR_TAREFA <id> <nova_descricao>` | Edita uma tarefa. | `EDITAR_TAREFA 1 "Revisar relatório"` |
| `DELETAR_TAREFA <id>` | Remove uma tarefa. | `DELETAR_TAREFA 2` |
| `LISTAR_TAREFAS` | Lista todas as tarefas. | `LISTAR_TAREFAS` |
| `CONCLUIR_TAREFA <id>` | Marca uma tarefa como concluída. | `CONCLUIR_TAREFA 3` |

### Respostas do Servidor
| Resposta | Significado |
|----------|-------------|
| `OK Tarefa criada com ID <id>: <descricao>` | Confirma a criação da tarefa |
| `OK Tarefa editada` | Confirma a edição da tarefa |
| `OK Tarefa deletada` | Confirma a exclusão da tarefa |
| `OK Tarefa concluída` | Confirma a conclusão da tarefa |
| `ERRO <motivo>` | Retorna um erro (exemplo: ID inexistente) |

---

## Melhorias Futuras
- Implementar **armazenamento em banco de dados**.
- Criar **interface gráfica (GUI)** para facilitar o uso.
- Adicionar **autenticação de usuários**.

---
