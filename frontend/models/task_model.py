import requests

API_URL = "http://127.0.0.1:5000/tasks"  # URL бэкенда

class TaskModel:
    @staticmethod
    def get_tasks():
        """Получение списка задач с API"""
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при получении задач: {e}")
            return []
