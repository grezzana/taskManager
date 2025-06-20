# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil import parser

class Task:
    def __init__(self, id=None, title="", description="", due_date=None, priority="normal", completed=False, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
        self.created_at = created_at
        self.updated_at = updated_at
    
    @classmethod
    def from_dict(cls, data):
        """Cria uma instância de Task a partir de um dicionário (resposta da API)"""
        # Converter strings de data para objetos datetime, se existirem
        due_date = None
        if data.get('dueDate'):
            try:
                due_date = parser.isoparse(data['dueDate'])
            except (ValueError, TypeError):
                # Se o parsing falhar, deixa como None
                pass
        
        created_at = None
        if data.get('createdAt'):
            try:
                created_at = parser.isoparse(data['createdAt'])
            except (ValueError, TypeError):
                pass
        
        updated_at = None
        if data.get('updatedAt'):
            try:
                updated_at = parser.isoparse(data['updatedAt'])
            except (ValueError, TypeError):
                pass
        
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            due_date=due_date,
            priority=data.get('priority', 'normal'),
            completed=data.get('completed', False),
            created_at=created_at,
            updated_at=updated_at
        )
    
    def to_dict(self, for_create=False):
        """Converte a tarefa para um dicionário para envio à API"""
        task_dict = {}
        
        # Para criação, enviamos apenas os campos necessários
        if for_create:
            task_dict = {
                'title': self.title,
                'description': self.description,
                'priority': self.priority
            }
            if self.due_date:
                # Formatar a data como string ISO 8601 com 'Z' para indicar UTC
                if hasattr(self.due_date, 'isoformat'):
                    iso_date = self.due_date.isoformat()
                    # Garantir que a data termine com 'Z' para indicar UTC
                    if iso_date.endswith('+00:00'):
                        iso_date = iso_date.replace('+00:00', 'Z')
                    elif not iso_date.endswith('Z'):
                        iso_date += 'Z'
                    task_dict['dueDate'] = iso_date
        else:
            # Para atualização, enviamos apenas campos não-nulos
            if self.title:
                task_dict['title'] = self.title
            if self.description is not None:  # Permitir descrição vazia
                task_dict['description'] = self.description
            if self.priority:
                task_dict['priority'] = self.priority
            if self.due_date:
                # Formatar a data como string ISO 8601 com 'Z' para indicar UTC
                if hasattr(self.due_date, 'isoformat'):
                    iso_date = self.due_date.isoformat()
                    # Garantir que a data termine com 'Z' para indicar UTC
                    if iso_date.endswith('+00:00'):
                        iso_date = iso_date.replace('+00:00', 'Z')
                    elif not iso_date.endswith('Z'):
                        iso_date += 'Z'
                    task_dict['dueDate'] = iso_date
            if self.completed is not None:
                task_dict['completed'] = self.completed
                
        return task_dict
    
    def __str__(self):
        status = "✓" if self.completed else "□"
        due_date_str = f", Prazo: {self.due_date.strftime('%d/%m/%Y')}" if self.due_date else ""
        return f"[{status}] {self.title} ({self.priority}{due_date_str})"