import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from algoritm_runner import alg_main


API_TOKEN = os.getenv("TELEGRAM_TOKEN")


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message(Command("start"))
async def welcome(message: types.Message):
    """Отправляет приветственное сообщение"""

    await message.answer(f'Здравствуй, {message.from_user.full_name}!')


@dp.message()
async def agregate_salary(message: types.Message):
    """Отправляет ответ после поступления входных данных"""

    answer_message = alg_main(message.text)
    await message.answer(answer_message)



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())