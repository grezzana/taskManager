from task_manager import TaskManager

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

def main():
    task_manager = TaskManager()
    
    # Adicionar algumas tarefas de exemplo
    task_manager.add_task("Estudar Python", "Revisar funções e classes", "2023-12-15", "alta")
    task_manager.add_task("Fazer compras", "Comprar frutas e vegetais")
    
    while True:
        print_menu()
        choice = input("Escolha uma opção (1-7): ")
        
        if choice == "1":
            title = input("Título da tarefa: ")
            description = input("Descrição (opcional): ")
            due_date = input("Data de vencimento (AAAA-MM-DD) (opcional): ")
            due_date = due_date if due_date else None
            priority = input("Prioridade (baixa/normal/alta) (padrão: normal): ")
            priority = priority if priority in ["baixa", "normal", "alta"] else "normal"
            
            task_manager.add_task(title, description, due_date, priority)
            print(f"Tarefa '{title}' adicionada com sucesso!")
            
        elif choice == "2":
            tasks = task_manager.get_all_tasks()
            if tasks:
                print("\nTodas as tarefas:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("Nenhuma tarefa encontrada.")
                
        elif choice == "3":
            tasks = task_manager.get_pending_tasks()
            if tasks:
                print("\nTarefas pendentes:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("Nenhuma tarefa pendente encontrada.")
                
        elif choice == "4":
            tasks = task_manager.get_completed_tasks()
            if tasks:
                print("\nTarefas concluídas:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("Nenhuma tarefa concluída encontrada.")
                
        elif choice == "5":
            title = input("Digite o título da tarefa a ser concluída: ")
            task = task_manager.find_task_by_title(title)
            if task:
                task.mark_as_completed()
                print(f"Tarefa '{title}' marcada como concluída!")
            else:
                print(f"Tarefa '{title}' não encontrada.")
                
        elif choice == "6":
            title = input("Digite o título da tarefa a ser excluída: ")
            if task_manager.delete_task(title):
                print(f"Tarefa '{title}' excluída com sucesso!")
            else:
                print(f"Tarefa '{title}' não encontrada.")
                
        elif choice == "7":
            print("Obrigado por usar o Sistema de Gerenciamento de Tarefas!")
            break
            
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()