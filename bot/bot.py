import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from transformers import pipeline
import openai

# 1) Загрузка переменных окружения из .env
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN_BOT")
AI_TOKEN = os.getenv("TOKEN_AI")

if not BOT_TOKEN or not AI_TOKEN:
    raise RuntimeError(
        "Переменные TOKEN_BOT и TOKEN_AI должны быть "
        "заданы в файле .env"
    )


class DoctorRecommendationSystem:
    def __init__(self, openai_key: str):
        openai.api_key = openai_key
        self.symptoms_classifier = pipeline("zero-shot-classification")

    def classify_symptoms(self, symptoms_text: str) -> dict:
        specialties = [
            "Терапия", "Хирургия", "Педиатрия",  # noqa: E501
            "Неврология", "Кардиология"  # noqa: E501
        ]
        result = self.symptoms_classifier(
            symptoms_text,
            specialties,
            multi_label=True
        )  # noqa: E501
        return result

    def recommend_doctor(self, symptoms_text: str) -> str:
        classification = self.classify_symptoms(symptoms_text)
        best_specialty = max(  # noqa: E501
            classification["labels"],  # noqa: E501
            key=lambda l: classification["scores"][  # noqa: E501
                classification["labels"].index(l)  # noqa: E501
            ]  # noqa: E501
        )  # noqa: E501
        return self.find_doctor_by_specialty(best_specialty)

    @staticmethod
    def find_doctor_by_specialty(specialty: str) -> str:
        doctors = {
            "Терапия": "Доктор Иванова",
            "Хирургия": "Доктор Петров",
            "Педиатрия": "Доктор Сидорова",
            "Неврология": "Доктор Козлов",
            "Кардиология": "Доктор Васильева",
        }
        return doctors.get(specialty, "Специалист не найден")  # noqa: E501


class TelegramBot:
    def __init__(self, token: str, recommendation_system: DoctorRecommendationSystem):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.recommendation_system = recommendation_system

        # Регистрация хендлеров
        self.dp.message(Command("start"))(self.start_handler)
        self.dp.message()(self.symptoms_handler)

    @staticmethod
    async def start_handler(message: types.Message):
        await message.answer(
            "Привет! Опиши свои симптомы, и я подберу подходящего врача."
        )

    async def symptoms_handler(self, message: types.Message):
        if not message.text or not message.text.strip():
            await message.answer(
                "Пожалуйста, опишите ваши симптомы текстом."
            )
            return

        loop = asyncio.get_running_loop()
        doctor = await loop.run_in_executor(  # noqa: E501
            None,  # noqa: E501
            self.recommendation_system.recommend_doctor,  # noqa: E501
            message.text  # noqa: E501
        )  # noqa: E501
        await message.answer(f"Рекомендуемый врач: {doctor}")  # noqa: E501


async def main():
    recommendation_system = DoctorRecommendationSystem(openai_key=AI_TOKEN)
    bot = TelegramBot(
        token=BOT_TOKEN,
        recommendation_system=recommendation_system
    )
    await bot.dp.start_polling(bot.bot)


if __name__ == "__main__":
    asyncio.run(main())
