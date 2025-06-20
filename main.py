# -*- coding: utf-8 -*-
from datetime import datetime
from task import Task
from task_client import TaskClient

def print_menu():
    print("\n===== Sistema de Gerenciamento de Tarefas =====")
    print("1. Adicionar nova tarefa")
    print("2. Listar todas as tarefas")
    print("3. Listar tarefas pendentes")
    print("4. Listar tarefas concluídas")
    print("5. Marcar tarefa como concluída")
    print("6. Excluir tarefa")
    print("7. Sair")
    print("==============================================")

def parse_date(date_str):
    """Converte uma string de data para objeto datetime"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        print("Formato de data inválido. Use AAAA-MM-DD.")
        return None

def main():
    # Inicializa o cliente da API
    api_url = input("Digite a URL da API (ou pressione Enter para usar http://localhost:8080): ")
    if not api_url:
        api_url = "http://localhost:8080"
    
    client = TaskClient(api_url)
    print(f"Conectando à API em: {api_url}")
    
    # Testa a conexão com a API
    try:
        tasks = client.get_all_tasks()
        print(f"Conexão estabelecida com sucesso! {len(tasks)} tarefas encontradas.")
    except Exception as e:
        print(f"Erro ao conectar à API: {e}")
        print("Verifique se a API está em execução e tente novamente.")
        return
    
    while True:
        print_menu()
        choice = input("Escolha uma opção (1-7): ")
        
        if choice == "1":
            # Adicionar nova tarefa
            title = input("Título da tarefa: ")
            if not title:
                print("O título é obrigatório.")
                continue
                
            description = input("Descrição (opcional): ")
            due_date_str = input("Data de vencimento (AAAA-MM-DD) (opcional): ")
            due_date = parse_date(due_date_str)
            
            priority = input("Prioridade (baixa/normal/alta) (padrão: normal): ")
            if priority not in ["baixa", "normal", "alta"]:
                priority = "normal"
            
            task = Task(title=title, description=description, due_date=due_date, priority=priority)
            created_task = client.create_task(task)
            
            if created_task:
                print(f"Tarefa '{title}' adicionada com sucesso!")
            else:
                print("Falha ao adicionar tarefa.")
                
        elif choice == "2":
            # Listar todas as tarefas
            tasks = client.get_all_tasks()
            if tasks:
                print("\nTodas as tarefas:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("Nenhuma tarefa encontrada.")
                
        elif choice == "3":
            # Listar tarefas pendentes
            tasks = client.get_tasks_by_status(completed=False)
            if tasks:
                print("\nTarefas pendentes:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("Nenhuma tarefa pendente encontrada.")
                
        elif choice == "4":
            # Listar tarefas concluídas
            tasks = client.get_tasks_by_status(completed=True)
            if tasks:
                print("\nTarefas concluídas:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("Nenhuma tarefa concluída encontrada.")
                
        elif choice == "5":
            # Marcar tarefa como concluída
            # Primeiro, listar tarefas pendentes para o usuário escolher
            tasks = client.get_tasks_by_status(completed=False)
            if not tasks:
                print("Não há tarefas pendentes para marcar como concluídas.")
                continue
                
            print("\nTarefas pendentes:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
                
            try:
                task_index = int(input("\nDigite o número da tarefa a ser concluída: ")) - 1
                if task_index < 0 or task_index >= len(tasks):
                    print("Número de tarefa inválido.")
                    continue
                    
                task_id = tasks[task_index].id
                updated_task = client.mark_task_as_completed(task_id)
                
                if updated_task:
                    print(f"Tarefa '{tasks[task_index].title}' marcada como concluída!")
                else:
                    print("Falha ao marcar tarefa como concluída.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
                
        elif choice == "6":
            # Excluir tarefa
            # Primeiro, listar todas as tarefas para o usuário escolher
            tasks = client.get_all_tasks()
            if not tasks:
                print("Não há tarefas para excluir.")
                continue
                
            print("\nTodas as tarefas:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
                
            try:
                task_index = int(input("\nDigite o número da tarefa a ser excluída: ")) - 1
                if task_index < 0 or task_index >= len(tasks):
                    print("Número de tarefa inválido.")
                    continue
                    
                task_id = tasks[task_index].id
                confirm = input(f"Tem certeza que deseja excluir a tarefa '{tasks[task_index].title}'? (s/n): ")
                
                if confirm.lower() == 's':
                    success = client.delete_task(task_id)
                    if success:
                        print(f"Tarefa '{tasks[task_index].title}' excluída com sucesso!")
                    else:
                        print("Falha ao excluir tarefa.")
                else:
                    print("Operação cancelada.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
                
        elif choice == "7":
            print("Obrigado por usar o Sistema de Gerenciamento de Tarefas!")
            break
            
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()