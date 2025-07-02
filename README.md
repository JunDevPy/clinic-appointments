
# Тестовое задание «Clinic Appointments»

Микросервис для записи пациентов к врачам на FastAPI с PostgreSQL.

## Быстрый старт

```bash
git clone <repository-url>
cd clinic-appointments
cp .env.example .env
docker-compose up -d --build
curl http://localhost:8000/health
```

## API Endpoints
- GET /health - проверка здоровья сервиса
- POST /appointments - создать запись
- GET /appointments/{id} - получить запись по ID

## Make и Разработка
```makefile
make lint    # проверка стиля кода
make test    # запуск тестов
make up      # запуск сервисов
make down    # остановка сервисов
```

## Пример использования

```
# Создать запись
curl -X POST "http://localhost:8000/appointments" \
     -H "Content-Type: application/json" \
     -d '{
       "patient_name": "Иван Иванов",
       "doctor_id": 1,
       "start_time": "2025-07-10T10:00:00"
     }'

# Получить запись
curl "http://localhost:8000/appointments/1"

```