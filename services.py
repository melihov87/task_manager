from datetime import datetime
from typing import List, Optional
from models import Task
from repositories import TaskRepository

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository
        self.tasks = self.repository.load_tasks()

    def add_task(self) -> None:
        try:
            task = Task(
                id=max([t.id for t in self.tasks], default=0) + 1,
                title=self.sanitize_input(input("Введите название задачи: ").strip()).lower().capitalize(),
                description=input("Введите описание задачи: ").strip().lower().capitalize(),
                category=input("Введите категорию задачи: ").strip().lower().capitalize(),
                due_date=datetime.strptime(input("Введите срок выполнения (YYYY-MM-DD): ").strip(), "%Y-%m-%d"),
                priority=self.validate_priority(input("Введите приоритет задачи (низкий/средний/высокий): ")
                                                .strip()).lower().capitalize(),
                status="В работе"  # Указан статус по умолчанию
            )
            self.tasks.append(task)
            self.repository.save_tasks(self.tasks)
            print("Задача успешно добавлена!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def edit_task(self, task_id: int) -> None:
        task = self.find_task_by_id(task_id)
        if task:
            task.title = self.sanitize_input(input("Введите новое название задачи: ").strip()).lower().capitalize()
            task.description = input("Введите новое описание задачи: ").strip().lower().capitalize()
            task.category = input("Введите новую категорию задачи: ").strip().lower().capitalize()
            task.due_date = datetime.strptime(input("Введите новый срок выполнения (YYYY-MM-DD): ").strip(), "%Y-%m-%d")
            task.priority = self.validate_priority(input("Введите новый приоритет задачи (низкий/средний/высокий): ").strip()).lower().capitalize()
            self.repository.save_tasks(self.tasks)
            print("Задача успешно отредактирована!")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def validate_priority(self, priority: str) -> str:
        if priority not in ["низкий", "средний", "высокий"]:
            raise ValueError("Приоритет должен быть одним из: низкий, средний, высокий")
        return priority

    def sanitize_input(self, text: str) -> str:
        try:
            return text.encode("utf-8", "replace").decode("utf-8")
        except UnicodeEncodeError:
            return text.replace("\udcd0", "?")  # Заменить некорректный символ на "?"

    def find_task_by_id(self, task_id: int) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def delete_task(self, task_id: int) -> None:
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.repository.save_tasks(self.tasks)

    def display_tasks(self) -> None:
        if not self.tasks:
            print("Нет задач для отображения.")
            return
        for task in self.tasks:
            print(
                f"ID: {task.id}, Наименование: {task.title}, Статус: {task.status}, "
                f"Дата: {task.due_date.strftime('%Y-%m-%d')}, Приоритет: {task.priority}, "
                f"Категория: {task.category}, Описание: {task.description}"
            )
