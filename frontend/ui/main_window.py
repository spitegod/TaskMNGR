from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QMessageBox, QAbstractItemView, QMenuBar
import sys
from frontend.controllers.task_controller import TaskController
from PyQt6.QtGui import QAction


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
        
        # Разрешаем выделение только одной строки
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Запрещаем редактирование ячеек
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


        # Кнопки
        self.add_button = QPushButton("Добавить задачу")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")

        layout.addWidget(self.add_button)
        self.add_button.clicked.connect(self.open_add_task_dialog)

        layout.addWidget(self.edit_button)
        self.edit_button.clicked.connect(self.open_edit_dialog)

        layout.addWidget(self.delete_button)
        self.delete_button.clicked.connect(self.delete_task)
        self.menu_bar = QMenuBar(self)
        file_menu = self.menu_bar.addMenu("Файл")
        
        # Создаем действие "Очистить таблицу"
        clear_action = QAction("Очистить таблицу", self)
        clear_action.triggered.connect(self.clear_table)  # Привязываем действие к функции
        file_menu.addAction(clear_action)

        # Добавляем меню в окно
        self.setMenuBar(self.menu_bar)

        central_widget.setLayout(layout)


    def open_add_task_dialog(self):
        from frontend.ui.add_task_dialog import AddTaskDialog
        dialog = AddTaskDialog(self)
        dialog.exec()

    def open_edit_dialog(self):
        from frontend.ui.edit_task_dialog import EditTaskDialog
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для редактирования.")
            return

        # Получаем ID задачи
        task_id = self.table.item(selected_row, 0).text()

        # Открываем диалог редактирования
        dialog = EditTaskDialog(task_id, self.controller)
        if dialog.exec():
            self.controller.load_tasks()  # Обновляем список после редактирования

    def delete_task(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для удаления.")
            return
        
        task_id = self.table.item(selected_row, 0).text()
        
        confirm = QMessageBox.question(self, "Удаление", f"Удалить задачу #{selected_row + 1}?", 
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.controller.delete_task(task_id)

    def clear_table(self):
        """Очистить таблицу и базу данных"""
        reply = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите очистить таблицу?", 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            # 1. Очищаем таблицу на клиенте
            self.controller.clear_table()

            # 2. Отправляем запрос на сервер для очистки базы данных
            response = self.controller.delete_all_tasks()
            
            if response.status_code == 200:
                QMessageBox.information(self, "Очистка", "Таблица и база данных были очищены.")
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось очистить базу данных.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
