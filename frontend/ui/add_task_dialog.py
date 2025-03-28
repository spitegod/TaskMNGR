from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QTextEdit, QDateEdit
from PyQt6.QtCore import QDate

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить задачу")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Поле для названия
        self.title_label = QLabel("Название:")
        self.title_input = QLineEdit()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.title_input)

        # Поле для описания
        self.desc_label = QLabel("Описание:")
        self.desc_input = QTextEdit()
        self.layout.addWidget(self.desc_label)
        self.layout.addWidget(self.desc_input)

        # Поле для даты
        # self.date_label = QLabel("Дата (YYYY-MM-DD):")
        # self.date_input = QLineEdit()
        # self.layout.addWidget(self.date_label)
        # self.layout.addWidget(self.date_input)

        self.date_label = QLabel("Дата:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)  # Добавляем выпадающий календарь
        self.date_input.setDate(QDate.currentDate())  # Устанавливаем текущую дату
        self.layout.addWidget(self.date_label)
        self.layout.addWidget(self.date_input)

        # Поле для приоритета
        self.priority_label = QLabel("Приоритет:")
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Низкий", "Средний", "Высокий"])
        self.layout.addWidget(self.priority_label)
        self.layout.addWidget(self.priority_input)

        # Поле для статуса
        self.status_label = QLabel("Статус:")
        self.status_input = QComboBox()
        self.status_input.addItems(["Новая", "В процессе", "Завершена"])
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.status_input)

        # Кнопки
        self.add_button = QPushButton("Добавить")
        self.cancel_button = QPushButton("Отмена")
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.cancel_button)

        # Подключаем сигналы
        self.add_button.clicked.connect(self.add_task)
        self.cancel_button.clicked.connect(self.reject)

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
