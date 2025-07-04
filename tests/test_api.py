"""
Интеграционные тесты API
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import Base, get_db
from api.main import app

# Создаем временную базу для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,  # noqa: E501
    autoflush=False,  # noqa: E501
    bind=engine,  # noqa: E501
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_health_check():
    """Тест health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_create_appointment():
    """Тест создания записи"""
    appointment_data = {
        "patient_name": "Иван Иванов",
        "doctor_id": 1,
        "start_time": "2025-07-10T10:00:00",
    }
    response = client.post("/appointments", json=appointment_data)
    assert response.status_code == 201
    data = response.json()
    assert data["patient_name"] == "Иван Иванов"
    assert data["doctor_id"] == 1
    assert "id" in data


def test_get_appointment():
    """Тест получения записи"""

    # Сначала создаем запись
    appointment_data = {
        "patient_name": "Петр Петров",
        "doctor_id": 2,
        "start_time": "2025-07-10T11:00:00",
    }
    create_response = client.post("/appointments", json=appointment_data)
    appointment_id = create_response.json()["id"]

    # Теперь получаем её
    response = client.get(f"/appointments/{appointment_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_name"] == "Петр Петров"
    assert data["id"] == appointment_id


def test_appointment_conflict():
    """Тест конфликта при создании записи (один врач в одно время)"""

    appointment_data = {
        "patient_name": "Анна Иванова",
        "doctor_id": 3,
        "start_time": "2025-07-10T12:00:00",
    }

    # Первая запись должна пройти
    response1 = client.post("/appointments", json=appointment_data)
    assert response1.status_code == 201

    # Вторая запись с тем же врачом и временем должна вернуть ошибку
    appointment_data["patient_name"] = "Борис Борисов"
    response2 = client.post("/appointments", json=appointment_data)
    assert response2.status_code == 409


def test_get_nonexistent_appointment():
    """Тест получения несуществующей записи"""

    response = client.get("/appointments/999999")
    assert response.status_code == 404
