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

# Добавление задачи
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()  # Получаем данные из тела запроса
    
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    priority = data.get('priority', 'Средний')  # По умолчанию "Средний"
    status = data.get('status', 'Новая')  # По умолчанию "Новая"
    
    if not title:
        return jsonify({"error": "Title is required"}), 400
    
    # Вставка новой задачи в базу данных
    cursor.execute("""
        INSERT INTO tasks (title, description, due_date, priority, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, description, due_date, priority, status))
    
    db.commit()
    
    # Возвращаем успешный ответ
    return jsonify({"message": "Task added successfully"}), 201

# Получение конкретной задачи
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Преобразуем дату в строку
    if isinstance(task['due_date'], date):
        task['due_date'] = task['due_date'].strftime('%Y-%m-%d')

    response = json.dumps(task, ensure_ascii=False)
    
    # Возвращаем результат
    return response, 200

# Обновление задачи
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    
    if not task:
        return jsonify({"error": "Task not found"}), 404

    title = data.get('title', task['title'])
    description = data.get('description', task['description'])
    due_date = data.get('due_date', task['due_date'])
    priority = data.get('priority', task['priority'])
    status = data.get('status', task['status'])

    cursor.execute("""
        UPDATE tasks 
        SET title = %s, description = %s, due_date = %s, priority = %s, status = %s
        WHERE id = %s
    """, (title, description, due_date, priority, status, task_id))

    db.commit()

    return jsonify({"message": "Task updated successfully"}), 200


@app.route('/')
def home():
    return "Hello world!"


if __name__ == '__main__':
    app.run(debug=True)
