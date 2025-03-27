from flask import Flask, request, jsonify
import mysql.connector

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
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    result = []
    for task in tasks:
        result.append({
            "id": task[0],
            "title": task[1],
            "description": task[2],
            "due_date": str(task[3]),
            "priority": task[4],
            "status": task[5]
        })
    return jsonify(result)

@app.route('/')
def home():
    return "Hello world!"

# Добавление новой задачи
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    sql = "INSERT INTO tasks (title, description, due_date, priority, status) VALUES (%s, %s, %s, %s, %s)"
    values = (data["title"], data["description"], data["due_date"], data["priority"], data["status"])
    cursor.execute(sql, values)
    db.commit()
    return jsonify({"message": "Задача добавлена"}), 201

if __name__ == '__main__':
    app.run(debug=True)
