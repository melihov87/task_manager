# main.py
from repositories import JSONTaskRepository
from services import TaskService
from cli import TaskManagerCLI

def main():
    repository = JSONTaskRepository("tasks.json")
    service = TaskService(repository)
    cli = TaskManagerCLI(service)

    cli.run()

if __name__ == "__main__":
    main()
