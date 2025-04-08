import pytest
from fastapi.testclient import TestClient
from main import app  # Импорт приложения
import main  # Импорт модуля приложения для доступа к его глобальным переменным

# Инициализируем тестовый клиент
client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_app_state():
    # Сбрасываем состояние приложения перед каждым тестом
    main.tasks = []
    main.current_id = 0

def test_create_task():
    response = client.post(
        "/tasks",
        json={"title": "Valid Task", "description": "A valid task description", "status": "pending"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Valid Task"

def test_get_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_get_tasks_with_data():
    # Создаем задачу
    client.post(
        "/tasks",
        json={"title": "Valid Task", "description": "A valid task description", "status": "pending"}
    )
    # Проверяем список задач
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 1