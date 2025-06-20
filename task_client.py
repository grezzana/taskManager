# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime
from task import Task

class TaskClient:
    def __init__(self, api_url="http://localhost:8080"):
        self.api_url = api_url
        self.tasks_endpoint = f"{api_url}/api/tasks"
    
    def get_all_tasks(self):
        """Obtém todas as tarefas da API"""
        try:
            response = requests.get(self.tasks_endpoint)
            response.raise_for_status()  # Lança exceção para erros HTTP
            
            data = response.json()
            if data.get('success') and data.get('data'):
                return [Task.from_dict(task) for task in data['data']]
            return []
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter tarefas: {e}")
            return []
    
    def get_task_by_id(self, task_id):
        """Obtém uma tarefa específica pelo ID"""
        try:
            response = requests.get(f"{self.tasks_endpoint}/{task_id}")
            response.raise_for_status()
            
            data = response.json()
            if data.get('success') and data.get('data'):
                return Task.from_dict(data['data'])
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter tarefa {task_id}: {e}")
            return None
    
    def create_task(self, task):
        """Cria uma nova tarefa na API"""
        try:
            task_data = task.to_dict(for_create=True)
            response = requests.post(
                self.tasks_endpoint,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(task_data)
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('success') and data.get('data'):
                return Task.from_dict(data['data'])
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar tarefa: {e}")
            return None
    
    def update_task(self, task_id, task):
        """Atualiza uma tarefa existente na API"""
        try:
            task_data = task.to_dict()
            response = requests.put(
                f"{self.tasks_endpoint}/{task_id}",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(task_data)
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get('success') and data.get('data'):
                return Task.from_dict(data['data'])
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro ao atualizar tarefa {task_id}: {e}")
            return None
    
    def delete_task(self, task_id):
        """Exclui uma tarefa da API"""
        try:
            response = requests.delete(f"{self.tasks_endpoint}/{task_id}")
            response.raise_for_status()
            
            data = response.json()
            return data.get('success', False)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao excluir tarefa {task_id}: {e}")
            return False
    
    def get_tasks_by_status(self, completed=False):
        """Obtém tarefas filtradas por status (concluídas ou pendentes)"""
        try:
            status = "true" if completed else "false"
            response = requests.get(f"{self.tasks_endpoint}/status/{status}")
            response.raise_for_status()
            
            data = response.json()
            if data.get('success') and data.get('data'):
                return [Task.from_dict(task) for task in data['data']]
            return []
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter tarefas por status: {e}")
            return []
    
    def mark_task_as_completed(self, task_id):
        """Marca uma tarefa como concluída"""
        task = Task(completed=True)
        return self.update_task(task_id, task)