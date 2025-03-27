from flask import Flask, request, jsonify
import mysql.connector
import json
from datetime import date  # Импортируем date

app = Flask(__name__)

# Подключение к БД
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="task_manager"
)
cursor = db.cursor()

# Получение всех задач
@app.route('/tasks')
def get_tasks():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    
    # Преобразуем дату в строку
    for task in tasks:
        if isinstance(task['due_date'], date):
            task['due_date'] = task['due_date'].strftime('%Y-%m-%d')
    
    # Сериализуем задачи в JSON с параметром ensure_ascii=False
    response = json.dumps(tasks, ensure_ascii=False)
    
    # Возвращаем результат
    return response, 200

@app.route('/')
def home():
    return "Hello world!"


if __name__ == '__main__':
    app.run(debug=True)
