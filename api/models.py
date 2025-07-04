# Модели данных (Appointment)
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint

from .database import Base


class Appointment(Base):
    """Модель данных для записи на прием"""

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, index=True, nullable=False)
    doctor_id = Column(Integer, index=True, nullable=False)
    start_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        UniqueConstraint("doctor_id", "start_time", name="_doctor_time_uc"),
    )
