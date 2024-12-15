import json
import os
from datetime import datetime
from typing import List
from dataclasses import dataclass

# Модели
@dataclass
class Task:
    title: str
    description: str
    category: str
    due_date: str
    priority: str
    status: str = "Не выполнена"  # Статус по умолчанию

    def __post_init__(self):
        # Проверка правильности формата даты
        try:
            self.due_date = datetime.strptime(self.due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Поле 'due_date' должно быть в формате YYYY-MM-DD.")
        # Проверка, что дата не в прошлом
        if self.due_date < datetime.now():
            raise ValueError("Дата выполнения не может быть старше текущей даты.")
        # Проверка приоритета
        if self.priority not in ["низкий", "средний", "высокий"]:
            raise ValueError("Приоритет должен быть одним из: низкий, средний, высокий.")
        # Проверка на пустые поля
        if not self.title or not self.description or not self.category:
            raise ValueError("Название, описание и категория не могут быть пустыми.")

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "status": self.status,
        }

# Менеджер задач
class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.filename) or os.stat(self.filename).st_size == 0:
            return []
        with open(self.filename, "r", encoding="utf-8") as file:
            task_dicts = json.load(file)
            return [Task(**task) for task in task_dicts]

    def save_tasks(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, task_id: int):
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self.save_tasks()

# Интерфейс для взаимодействия с пользователем
class TaskManagerCLI:
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager

    def display_tasks(self):
        if not self.task_manager.tasks:
            print("Нет задач для отображения.")
        else:
            for task in self.task_manager.tasks:
                print(f"ID: {task.id}, Наименование: {task.title}, Статус: {task.status}, "
                      f"Дата: {task.due_date.strftime('%Y-%m-%d')}, "
                      f"Приоритет: {task.priority}, Категория: {task.category}, "
                      f"Описание: {task.description}")

    def add_task(self):
        try:
            title = input("Введите название задачи: ").strip()
            description = input("Введите описание задачи: ").strip()
            category = input("Введите категорию задачи: ").strip()
            due_date = input("Введите срок выполнения (YYYY-MM-DD): ").strip()
            priority = input("Введите приоритет задачи (низкий/средний/высокий): ").strip()

            if not title or not description or not category:
                print("Ошибка: Название, описание и категория не могут быть пустыми.")
                return

            task = Task(title=title, description=description, category=category,
                        due_date=due_date, priority=priority)
            self.task_manager.add_task(task)
            print("Задача успешно добавлена!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def delete_task(self):
        task_id = input("Введите ID задачи для удаления: ").strip()
        try:
            task_id = int(task_id)
            self.task_manager.delete_task(task_id)
            print("Задача успешно удалена!")
        except ValueError:
            print("Ошибка: ID должен быть числом.")

# Главная функция
def main():
    task_manager = TaskManager()
    cli = TaskManagerCLI(task_manager)

    while True:
        print("\nМенеджер задач")
        print("1. Просмотр всех задач")
        print("2. Добавить задачу")
        print("3. Удалить задачу")
        print("4. Выход")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            cli.display_tasks()
        elif choice == "2":
            cli.add_task()
        elif choice == "3":
            cli.delete_task()
        elif choice == "4":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
