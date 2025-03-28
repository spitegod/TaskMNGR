from frontend.models.task_model import TaskModel
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
import requests


class TaskController:
    def __init__(self, ui):
        self.ui = ui  # UI (главное окно)
        self.load_tasks()

    def load_tasks(self):
        """Загружает задачи из API и добавляет их в таблицу"""
        tasks = TaskModel.get_tasks()
        self.ui.table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            self.ui.table.setItem(row, 0, self.create_item(task["id"]))
            self.ui.table.setItem(row, 1, self.create_item(task["title"]))
            self.ui.table.setItem(row, 2, self.create_item(task["description"]))
            self.ui.table.setItem(row, 3, self.create_item(task["due_date"]))
            self.ui.table.setItem(row, 4, self.create_item(task["priority"]))

    def add_task(self, task_data):
        response = requests.post("http://127.0.0.1:5000/tasks", json=task_data)
        if response.status_code == 201:
            self.load_tasks()  # Перезагружаем список задач

    def delete_task(self, task_id):
        response = requests.delete(f"http://127.0.0.1:5000/tasks/{task_id}")

        if response.status_code == 200:
            QMessageBox.information(self.ui, "Успешно", "Задача удалена.")
            self.load_tasks()  # Обновляем список задач
        else:
            QMessageBox.critical(self.ui, "Ошибка", "Не удалось удалить задачу.")

    @staticmethod
    def create_item(text):
        """Создает элемент таблицы"""
        return QTableWidgetItem(str(text))
