class Task:
    def __init__(self, title, description, assignee):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.completed = False

    def mark_completed(self):
        self.completed = True

# Sample data (replace with a database in a real-world application)
tasks = []