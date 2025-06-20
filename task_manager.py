from task import Task

class TaskManager:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, title, description="", due_date=None, priority="normal"):
        task = Task(title, description, due_date, priority)
        self.tasks.append(task)
        return task
    
    def get_all_tasks(self):
        return self.tasks
    
    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self):
        return [task for task in self.tasks if task.completed]
    
    def find_task_by_title(self, title):
        for task in self.tasks:
            if task.title.lower() == title.lower():
                return task
        return None
    
    def delete_task(self, title):
        task = self.find_task_by_title(title)
        if task:
            self.tasks.remove(task)
            return True
        return False