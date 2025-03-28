from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget
import sys
from frontend.controllers.task_controller import TaskController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 600, 400)

        self.init_ui()
        self.controller = TaskController(self)  # Подключаем контроллер

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Таблица задач
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Дата", "Приоритет"])
        layout.addWidget(self.table)

        # Кнопки
        self.add_button = QPushButton("Добавить задачу")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")

        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.open_add_task_dialog)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)

        central_widget.setLayout(layout)

    def open_add_task_dialog(self):
        from frontend.ui.add_task_dialog import AddTaskDialog
        dialog = AddTaskDialog(self)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
