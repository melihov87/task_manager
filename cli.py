# cli.py
from models import Task
from services import TaskService
from typing import List

class TaskManagerCLI:
    def __init__(self, service: TaskService):
        self.service = service

    def display_tasks(self, tasks: List[Task]) -> None:
        if not tasks:
            print("Нет задач для отображения.")
            return
        for task in tasks:
            print(
                f"ID: {task.id}, Наименование: {task.title}, Статус: {task.status}, "
                f"Дата: {task.due_date.strftime('%Y-%m-%d')}, Приоритет: {task.priority}, "
                f"Категория: {task.category}, Описание: {task.description}"
            )

    def add_task(self) -> None:
        try:
            self.service.add_task()
        except ValueError as e:
            print(f"Ошибка: {e}")

    def delete_task(self) -> None:
        try:
            task_id = int(input("Введите ID задачи для удаления: ").strip())
            self.service.delete_task(task_id)
            print("Задача успешно удалена!")
        except ValueError:
            print("Ошибка: ID должен быть числом.")

    def change_status(self) -> None:
        try:
            task_id = int(input("Введите ID задачи для смены статуса: ").strip())
            self.service.change_status(task_id)
        except ValueError:
            print("Ошибка: ID должен быть числом.")

    def edit_task(self) -> None:
        try:
            task_id = int(input("Введите ID задачи для редактирования: ").strip())
            self.service.edit_task(task_id)
        except ValueError:
            print("Ошибка: ID должен быть числом.")

    def run(self) -> None:
        while True:
            print("\nМенеджер задач")
            print("1. Просмотр всех задач")
            print("2. Добавить задачу")
            print("3. Удалить задачу")
            print("4. Сменить статус задачи на 'Выполнено'")
            print("5. Редактировать задачу")
            print("6. Выход")

            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self.display_tasks(self.service.tasks)
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.delete_task()
            elif choice == "4":
                self.change_status()
            elif choice == "5":
                self.edit_task()
            elif choice == "6":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
