class Task:
    def __init__(self, title, description="", due_date=None, priority="normal", completed=False):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.completed = completed
    
    def mark_as_completed(self):
        self.completed = True
    
    def update_priority(self, new_priority):
        self.priority = new_priority
    
    def __str__(self):
        status = "✓" if self.completed else "□"
        due_date_str = f", Prazo: {self.due_date}" if self.due_date else ""
        return f"[{status}] {self.title} ({self.priority}{due_date_str})"