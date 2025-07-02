from pydantic import BaseModel, Field
from datetime import datetime


class AppointmentCreate(BaseModel):
    """ Схема для создания новой записи """
    patient_name: str = Field(..., min_length=1, max_length=255)
    doctor_id: int = Field(..., gt=0)
    start_time: datetime


class AppointmentResponse(BaseModel):
    """ Схема для отображения записи, включая ID и дату создания """
    id: int
    patient_name: str
    doctor_id: int
    start_time: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    """ Схема для ответа о состоянии сервиса """
    status: str
    message: str
    timestamp: datetime
