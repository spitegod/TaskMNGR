from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QTextEdit, QDateEdit
from PyQt6.QtCore import QDate

class TaskDialogBase(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
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
        self.date_label = QLabel("Дата:")
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)  # Добавляем выпадающий календарь
        self.date_input.setDate(QDate.currentDate())  # Устанавливаем текущую дату

        # Отключаем возможность редактирования вручную, но календарь доступен
        self.date_input.setKeyboardTracking(False)  # Отключаем отслеживание ввода с клавиатуры

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
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Отмена")
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        # Подключаем кнопку отмены
        self.cancel_button.clicked.connect(self.reject)