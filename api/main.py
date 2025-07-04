"""
Главный модуль FastAPI приложения
"""

from datetime import datetime

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from api.config import settings
from api.crud import create_appointment, get_appointment
from api.database import engine, get_db
from api.models import Base
from api.schemas import AppointmentCreate, AppointmentResponse, HealthResponse

# # Создание таблиц закоментил в связи с ошибками в тестах перенес в события
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinic Appointments API",
    description="Микросервис для записи пациентов к врачам",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Проверка здоровья сервиса"""
    return HealthResponse(
        status="healthy",  # noqa: E501
        message="Service is running",  # noqa: E501
        timestamp=datetime.now(),  # noqa: E501
    )  # noqa: E501


@app.post("/appointments", response_model=AppointmentResponse, status_code=201)
async def create_appointment_endpoint(
    appointment: AppointmentCreate, db: Session = Depends(get_db)
):
    """Создать новую запись на прием"""
    return create_appointment(db=db, appointment=appointment)


@app.get("/appointments/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment_endpoint(
    appointment_id: int, db: Session = Depends(get_db)  # noqa: E501
):  # noqa: E501
    """Получить запись по ID"""
    return get_appointment(db=db, appointment_id=appointment_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
