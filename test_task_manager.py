import pytest
from task_manager import TaskManager


@pytest.fixture
def task_manager():
    return TaskManager(file_path="test_tasks.json")


def test_add_task(task_manager):
    task_manager.add_task("Test Task", "Test Description", "Работа", "2024-12-01", "Высокий")
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == "Test Task"
    assert task_manager.tasks[0].description == "Test Description"


def test_mark_task_done(task_manager):
    task_manager.add_task("Test Task", "Test Description", "Работа", "2024-12-01", "Высокий")
    task_id = task_manager.tasks[0].id
    task_manager.mark_task_done(task_id)
    assert task_manager.tasks[0].status == "Выполнена"


def test_search_tasks(task_manager):
    task_manager.add_task("Test Task", "Test Description", "Работа", "2024-12-01", "Высокий")
    task_manager.add_task("Another Task", "Test Description", "Личное", "2024-12-01", "Средний")
    tasks = task_manager.search_tasks("Test")
    assert len(tasks) == 2


def test_delete_task(task_manager):
    task_manager.add_task("Test Task", "Test Description", "Работа", "2024-12-01", "Высокий")
    task_id = task_manager.tasks[0].id
    task_manager.delete_task(task_id)
    assert len(task_manager.tasks) == 0
