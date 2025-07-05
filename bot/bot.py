import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from transformers import pipeline
import openai


class DoctorRecommendationSystem:
    def __init__(self, openai_key):
        openai.api_key = openai_key
        self.symptoms_classifier = pipeline("zero-shot-classification")

    def classify_symptoms(self, symptoms_text):
        specialties = [
            "Терапия", "Хирургия", "Педиатрия",
            "Неврология", "Кардиология"
        ]
        result = self.symptoms_classifier(
            symptoms_text,
            specialties,
            multi_label=True
        )
        return result

    def recommend_doctor(self, symptoms_text):
        classification = self.classify_symptoms(symptoms_text)
        # Находим специальность с максимальным скором
        best_specialty = max(
            classification['labels'],
            key=lambda label: classification['scores'][classification['labels'].index(label)]
        )
        return self.find_doctor_by_specialty(best_specialty)

    @staticmethod
    def find_doctor_by_specialty(specialty):
        doctors = {
            "Терапия": "Доктор Иванова",
            "Хирургия": "Доктор Петров",
            "Педиатрия": "Доктор Сидорова",
            "Неврология": "Доктор Козлов",
            "Кардиология": "Доктор Васильева"
        }
        return doctors.get(specialty, "Специалист не найден")


class TelegramBot:
    def __init__(self, token, recommendation_system):
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.recommendation_system = recommendation_system

        self.dp.message(Command("start"))(self.start_handler)
        self.dp.message()(self.symptoms_handler)

    @staticmethod
    async def start_handler(message: types.Message):
        await message.answer("Привет! Опиши свои симптомы, и я подберу подходящего врача.")

    async def symptoms_handler(self, message: types.Message):
        if not message.text.strip():
            await message.answer("Пожалуйста, опишите ваши симптомы текстом.")
            return

        # Работаем с рекомендательной системой через ThreadPool
        loop = asyncio.get_running_loop()
        doctor = await loop.run_in_executor(
            None,
            self.recommendation_system.recommend_doctor,
            message.text
        )
        await message.answer(f"Рекомендуемый врач: {doctor}")


async def main():
    recommendation_system = DoctorRecommendationSystem(openai_key="YOUR_OPENAI_KEY")
    bot = TelegramBot(
        token="YOUR_BOT_TOKEN",
        recommendation_system=recommendation_system
    )
    await bot.dp.start_polling(bot.bot)


if __name__ == "__main__":
    asyncio.run(main())
