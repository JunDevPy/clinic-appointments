"""
CRUD операции для работы с базой данных
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.exceptions import AppointmentConflictError, AppointmentNotFoundError
from api.models import Appointment
from api.schemas import AppointmentCreate


def create_appointment(
    db: Session, appointment: AppointmentCreate  # noqa: E501  # noqa: E501
) -> Appointment:  # noqa: E501
    """Создать новую запись на прием"""
    db_appointment = Appointment(
        patient_name=appointment.patient_name,
        doctor_id=appointment.doctor_id,
        start_time=appointment.start_time,
    )

    try:
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except IntegrityError:
        db.rollback()
        raise AppointmentConflictError(
            f"Врач с ID {appointment.doctor_id} "
            f"уже занят в {appointment.start_time}"
        )


def get_appointment(db: Session, appointment_id: int) -> Appointment:
    """Получить запись по ID"""
    appointment = (
        db.query(Appointment).filter(Appointment.id == appointment_id).first()
    )  # noqa: E501

    if not appointment:
        raise AppointmentNotFoundError(
            f"Запись с ID {appointment_id} не найдена"
        )  # noqa: E501

    return appointment


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    """Получить список записей с пагинацией"""
    return db.query(Appointment).offset(skip).limit(limit).all()
