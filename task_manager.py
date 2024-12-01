import json
import os
from datetime import datetime
from typing import Dict
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')


class Task:
    def __init__(self, title: str, description: str, category: str, due_date: str, priority: str):

        def remove_special_characters(input_string: str) -> str:
            # Удаляем все символы, кроме букв и цифр
            return re.sub(r'[^a-zA-Z0-9а-яА-Я]', '', input_string)

        # Удаление специальных символов
        title = remove_special_characters(title)
        description = remove_special_characters(description)
        category = remove_special_characters(category)

        # Проверка обязательных полей
        if not title.strip():
            raise ValueError("Поле 'title' обязательно для заполнения.")
        if not description.strip():
            raise ValueError("Поле 'description' обязательно для заполнения.")
        if not category.strip():
            raise ValueError("Поле 'category' обязательно для заполнения.")
        if not priority.strip():
            raise ValueError("Поле 'priority' обязательно для заполнения.")

        # Повторный ввод срока выполнения до правильного формата
        while not due_date.strip():
            print("Поле 'due_date' обязательно для заполнения.")
            due_date = input("Введите срок выполнения (в формате YYYY-MM-DD): ")

        while True:
            try:
                # Преобразуем дату в нужный формат
                self.due_date = datetime.strptime(due_date, "%Y-%m-%d")

                # Проверка, что дата не старше текущей
                if self.due_date < datetime.now():
                    print("Ошибка: Дата выполнения не может быть старше текущей даты.")
                    due_date = input("Введите срок выполнения (в формате YYYY-MM-DD): ")
                else:
                    break  # Выход из цикла, если дата введена корректно
            except ValueError:
                print("Ошибка: Поле 'due_date' должно быть в формате YYYY-MM-DD.")
                due_date = input("Введите срок выполнения (в формате YYYY-MM-DD): ")

        # Проверка приоритета
        while priority.strip().lower() not in ['низкий', 'средний', 'высокий']:
            print("Ошибка: Приоритет должен быть одним из следующих: 'низкий', 'средний', 'высокий'.")
            priority = input("Введите приоритет (низкий, средний, высокий): ")

        self.id = None
        self.title = title.capitalize()
        self.description = description.capitalize()
        self.category = category.capitalize()
        self.due_date = due_date
        self.priority = priority.capitalize()
        self.status = "Не выполнена"

    def mark_done(self):
        self.status = "Выполнена"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        required_keys = ["id", "title", "description", "category", "due_date", "priority", "status"]
        if not all(key in data for key in required_keys):
            raise ValueError(f"Некоторые обязательные ключи отсутствуют: {set(required_keys) - set(data.keys())}")

        for key in ["title", "description", "category", "priority", "due_date"]:
            if key in data and not data[key].strip():
                data[key] = "Не указано"  # Заменяем пустое значение на строку по умолчанию

        # Проверка формата даты
        try:
            datetime.strptime(data["due_date"], "%Y-%m-%d")
        except ValueError:
            raise ValueError("Поле 'due_date' должно быть в формате YYYY-MM-DD.")

        task = cls(data["title"], data["description"], data["category"], data["due_date"], data["priority"])
        task.id = data["id"]
        task.status = data["status"]
        return task


class TaskManager:
    def __init__(self):
        self.file_path = "tasks.json"
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        except json.JSONDecodeError:
            print("Ошибка: некорректный формат файла tasks.json.")
            return []

    def save_tasks(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title, description, category, due_date, priority):
        try:
            task = Task(title, description, category, due_date, priority)
            task.id = self.generate_id()
            self.tasks.append(task)
            self.save_tasks()
            print("Задача успешно добавлена!")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def generate_id(self) -> int:
        return max([task.id for task in self.tasks], default=0) + 1

    def mark_task_done(self, task_id):
        task = self.find_task_by_id(task_id)
        if task:
            task.mark_done()
            self.save_tasks()
            print(f"Задача с ID {task_id} отмечена как выполненная.")
        else:
            print(f"Задача с ID {task_id} не найдена.")

    def edit_task(self, task_id, title=None, description=None, category=None, due_date=None, priority=None, status=None):
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Задача с ID {task_id} не найдена.")
            return

        try:
            if title:
                task.title = title
            if description:
                task.description = description
            if category:
                task.category = category
            if due_date:
                datetime.strptime(due_date, "%Y-%m-%d")  # Проверка формата
                task.due_date = due_date
            if priority:
                task.priority = priority
            if status:
                task.status = status
            self.save_tasks()
            print(f"Задача с ID {task_id} успешно обновлена.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def delete_task(self, task_id):
        try:
            task_id = int(task_id)
            self.tasks = [task for task in self.tasks if task.id != task_id]
            self.save_tasks()
            print(f"Задача с ID {task_id} удалена.")
        except ValueError:
            print("Ошибка: ID должен быть числом.")

    def delete_task_by_category(self, category_name):
        try:
            # Приводим имя категории к нижнему регистру для безопасного сравнения
            category_name = category_name.strip().lower()

            # Находим все задачи, относящиеся к этой категории
            tasks_to_delete = [task for task in self.tasks if task.category.strip().lower() == category_name]

            if tasks_to_delete:
                # Удаляем задачи с этой категорией
                self.tasks = [task for task in self.tasks if task.category.strip().lower() != category_name]
                self.save_tasks()
                print(f"Задачи с категорией '{category_name}' были удалены.")
            else:
                print(f"Ошибка: Задачи с категорией '{category_name}' не найдены.")

        except ValueError:
            print("Ошибка: Введена некорректная категория.")

    def find_task_by_id(self, task_id):
        return next((task for task in self.tasks if task.id == task_id), None)

    def find_tasks_by_category(self, category):
        return [task for task in self.tasks if task.category.lower() == category.lower()]

    def search_tasks(self, keyword, category=None, status=None):
        keyword = keyword.lower().strip()
        tasks = self.tasks
        if category:
            tasks = [task for task in tasks if task.category.lower() == category.lower()]
        if status:
            tasks = [task for task in tasks if task.status.lower() == status.lower()]
        tasks = [task for task in tasks if keyword in task.title.lower() or keyword in task.description.lower()]
        return tasks

    def display_tasks(self, tasks):
        if not tasks:
            print("Нет задач для отображения.")
            return

        for task in tasks:
            print(
                f"ID: {task.id}, Title: {task.title}, Status: {task.status}, "
                f"Due Date: {task.due_date}, Priority: {task.priority}, "
                f"Category: {task.category}, Description: {task.description}"
            )


# Вспомогательная функция для ввода данных с проверкой на пустоту
def clean_input(prompt, optional=False):
    """
    Функция для ввода данных с проверкой на пустоту.
    Если поле обязательное, оно не может быть пустым.
    """
    while True:
        user_input = input(prompt).strip()
        if not optional and not user_input:
            print("Это поле обязательно для заполнения!")
        else:
            return user_input


def main():
    task_manager = TaskManager()

    while True:
        print("\nМенеджер задач")
        print("1. Просмотр всех задач")
        print("2. Просмотр задач по категории")
        print("3. Добавить задачу")
        print("4. Редактировать задачу")
        print("5. Отметить задачу как выполненную")
        print("6. Удалить задачу по ID")
        print("7. Удалить задачу по КАТЕГОРИИ")
        print("8. Поиск задач")
        print("9. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            task_manager.display_tasks(task_manager.tasks)
        elif choice == "2":
            category = input("Введите категорию: ")
            tasks = task_manager.find_tasks_by_category(category)
            task_manager.display_tasks(tasks)
        elif choice == "3":
            title = clean_input("Введите название задачи: ")
            description = clean_input("Введите описание задачи: ")
            category = clean_input("Введите категорию: ")
            due_date = clean_input("Введите срок выполнения (в формате YYYY-MM-DD): ")
            priority = clean_input("Введите приоритет (низкий, средний, высокий): ")
            task_manager.add_task(title, description, category, due_date, priority)
        elif choice == "4":
            task_id = int(input("Введите ID задачи для редактирования: "))
            title = input("Введите новое название задачи (оставьте пустым для сохранения старого): ")
            description = input("Введите новое описание задачи (оставьте пустым для сохранения старого): ")
            category = input("Введите новую категорию задачи (оставьте пустым для сохранения старой): ")
            due_date = input("Введите новый срок выполнения задачи (в формате YYYY-MM-DD, оставьте пустым для сохранения старого): ")
            priority = input("Введите новый приоритет задачи (оставьте пустым для сохранения старого): ")
            status = input("Введите новый статус задачи (оставьте пустым для сохранения старого): ")

            task_manager.edit_task(
                task_id, title or None, description or None, category or None, due_date or None,
                priority or None, status or None
            )
        elif choice == "5":
            task_id = int(input("Введите ID задачи, которую хотите отметить как выполненную: "))
            task_manager.mark_task_done(task_id)
        elif choice == "6":
            task_id = int(input("Введите ID задачи для удаления: "))
            task_manager.delete_task(task_id)
        elif choice == "7":
            category = input("Введите КАТЕГОРИЮ задачи для удаления: ").strip()
            task_manager.delete_task_by_category(category)
        elif choice == "8":
            keyword = input("Введите ключевое слово для поиска: ")
            category = input("Введите категорию для поиска (оставьте пустым для всех): ")
            status = input("Введите статус для поиска (оставьте пустым для всех): ")
            tasks = task_manager.search_tasks(keyword, category, status)
            task_manager.display_tasks(tasks)
        elif choice == "9":
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите число от 1 до 8.")


if __name__ == "__main__":
    main()
