from .task_dialog_parent import TaskDialogBase
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate

class EditTaskDialog(TaskDialogBase):
    def __init__(self, task_id, controller, parent=None):
        super().__init__("Редактировать задачу", parent)
        self.task_id = task_id
        self.controller = controller

        self.ok_button.setText("Сохранить")
        self.ok_button.clicked.connect(self.save_changes)

        # Загружаем данные
        self.load_task_data()

    def load_task_data(self):
        task = self.controller.get_task(self.task_id)
        if not task:
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные задачи.")
            self.reject()
            return

        self.title_input.setText(task["title"])
        self.desc_input.setPlainText(task["description"])
        self.date_input.setDate(QDate.fromString(task["due_date"], "yyyy-MM-dd"))
        self.priority_input.setCurrentText(task["priority"])
        self.status_input.setCurrentText(task["status"])

    def save_changes(self):
        task_data = {
            "title": self.title_input.text(),
            "description": self.desc_input.toPlainText(),
            "due_date": self.date_input.date().toString("yyyy-MM-dd"),
            "priority": self.priority_input.currentText(),
            "status": self.status_input.currentText()
        }

        success = self.controller.update_task(self.task_id, task_data)
        if success:
            self.accept()
