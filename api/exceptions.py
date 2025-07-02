"""
Кастомные исключения
"""
from fastapi import HTTPException, status


class AppointmentConflictError(HTTPException):
    """Конфликт при создании записи"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class AppointmentNotFoundError(HTTPException):
    """Запись не найдена"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

