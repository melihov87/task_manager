import unittest
from unittest.mock import mock_open, patch
from datetime import datetime, timedelta
from task_manager import Task, TaskManager


class TestTask(unittest.TestCase):
    def test_task_initialization_valid(self):
        task = Task("Моя работа", "Описание моей работы", "Работа", "2024-12-31", "Средний")
        self.assertEqual(task.title, "Моя работа")
        self.assertEqual(task.description, "Описание моей работы")
        self.assertEqual(task.due_date.strftime("%Y-%m-%d"), "2024-12-31")
        self.assertEqual(task.priority, "Средний")
        self.assertEqual(task.status, "Не выполнена")

    def test_task_initialization_invalid_date(self):
        with self.assertRaises(ValueError) as context:
            Task("Моя работа", "Описание моей работы", "Работа", "нет-даты", "Средний")
        self.assertEqual(
            str(context.exception), "Поле 'due_date' должно быть в формате YYYY-MM-DD."
        )

    def test_task_initialization_past_date(self):
        past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        with self.assertRaises(ValueError) as context:
            Task("Моя работа", "Описание моей работы", "Работа", past_date, "Средний")
        self.assertEqual(
            str(context.exception), "Дата выполнения не может быть старше текущей даты."
        )


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager()

    @patch("task_manager.open", new_callable=mock_open)
    def test_save_tasks(self, mock_file):
        task = Task("Моя работа", "Описание моей работы", "Работа", "2024-12-31", "Средний")
        self.task_manager.add_task(task)
        self.task_manager.save_tasks()

        # Получаем все вызовы метода write
        write_calls = mock_file().write.call_args_list
        # Собираем написанные данные
        written_data = "".join(call.args[0] for call in write_calls)

        # Проверяем итоговое содержимое файла
        self.assertIn('"title": "Моя работа"', written_data)
        self.assertIn('"due_date": "2024-12-31T00:00:00"', written_data)
