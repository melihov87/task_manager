import os
import json
from models import Task
from typing import List


class TaskRepository:
    def load_tasks(self) -> List[Task]:
        raise NotImplementedError

    def save_tasks(self, tasks: List[Task]) -> None:
        raise NotImplementedError


class JSONTaskRepository(TaskRepository):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.file_path) or os.stat(self.file_path).st_size == 0:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                raw_tasks = json.load(file)
                return [Task.from_dict(task) for task in raw_tasks if isinstance(task, dict)]
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Ошибка при загрузке задач: {e}")
            return []

    def save_tasks(self, tasks: List[Task]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in tasks], file, ensure_ascii=False, indent=4)
