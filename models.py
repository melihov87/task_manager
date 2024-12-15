from datetime import datetime


class Task:
    def __init__(self, id, title, description, category, due_date, priority, status):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date.strftime("%Y-%m-%d"),  # Преобразуем дату в строку
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=datetime.strptime(data["due_date"], "%Y-%m-%d"),
            priority=data["priority"],
            status=data["status"]
        )
