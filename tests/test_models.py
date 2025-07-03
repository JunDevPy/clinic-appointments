"""
Юнит-тесты для моделей
"""

import pytest
from datetime import datetime, UTC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models import Base, Appointment

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_models.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def test_appointment_creation():
    """Тест создания модели Appointment"""
    db = TestingSessionLocal()

    appointment = Appointment(
        patient_name="Тест Пациент", doctor_id=1, start_time=datetime.now(UTC)
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    assert appointment.id is not None
    assert appointment.patient_name == "Тест Пациент"
    assert appointment.doctor_id == 1
    assert appointment.created_at is not None

    db.close()


def test_appointment_unique_constraint():
    """Тест уникального ограничения doctor_id + start_time"""
    db = TestingSessionLocal()

    start_time = datetime(2025, 7, 10, 14, 0, 0)

    # Первая запись
    appointment1 = Appointment(
        patient_name="Пациент 1", doctor_id=5, start_time=start_time
    )
    db.add(appointment1)
    db.commit()

    # Вторая запись с тем же врачом и временем
    appointment2 = Appointment(
        patient_name="Пациент 2", doctor_id=5, start_time=start_time
    )
    db.add(appointment2)

    with pytest.raises(Exception):  # IntegrityError
        db.commit()

    db.close()
