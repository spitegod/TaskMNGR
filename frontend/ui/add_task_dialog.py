from .task_dialog_parent import TaskDialogBase

class AddTaskDialog(TaskDialogBase):
    def __init__(self, parent=None):
        super().__init__("Добавить задачу", parent)

        self.ok_button.setText("Добавить")
        self.ok_button.clicked.connect(self.add_task)

    def add_task(self):
        task_data = {
            "title": self.title_input.text(),
            "description": self.desc_input.toPlainText(),
            "due_date": self.date_input.date().toString("yyyy-MM-dd"),
            "priority": self.priority_input.currentText(),
            "status": self.status_input.currentText()
        }
        self.parent().controller.add_task(task_data)
        self.accept()
