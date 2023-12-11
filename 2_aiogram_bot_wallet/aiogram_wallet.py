import json

from aiogram import Bot, Dispatcher, types, executor
from config import TOKEN, JSON_FILE


bot = Bot(TOKEN)
dp = Dispatcher(bot)

#создать кошелек пользователя по команде -cw
@dp.message_handler(commands=["-cw"])
async def create_wallet(message: types.Message):
    id_user = message.from_user.id
    user_ballance = 0
    res_user = {f"{id_user}": user_ballance}

    # файл БД для чтения
    with open(JSON_FILE, encoding="utf-8") as input_file:
        try:
            data = json.load(input_file)
        except:
            data = res_user
        else:
            data.update(res_user)

    # файл БД для записи
    with open(JSON_FILE, "w", encoding="utf-8") as wallet:
        json.dump(data, wallet, indent=4, ensure_ascii=False)

    await bot.send_message(chat_id=id_user, text=f"Кошелек {id_user} успешно создан")
    await message.delete()

# показать балланс кошелька пользователя по команде -sb
@dp.message_handler(commands=["-sb"])
async def show_wallet(message: types.Message):
    id_user = message.from_user.id

    # файл БД для чтения
    with open(JSON_FILE, encoding="utf-8") as input_file:
        data = json.load(input_file)
        user_ballance = data.get(f"{id_user}")
    await bot.send_message(chat_id=id_user, text=f"Ваш баланс = {user_ballance}")
    await message.delete()

# добавить 50 денег на баланс кошелька пользователя по команде -add_50
@dp.message_handler(commands=["-add_50"])
async def add_money(message: types.Message):
    id_user = message.from_user.id
    add_ballance = 50

    # файл БД для чтения
    with open(JSON_FILE, encoding="utf-8") as input_file:
        data = json.load(input_file)
        user_ballance = data.get(f"{id_user}")
        data[f"{id_user}"] = user_ballance + add_ballance
        user_ballance = data[f"{id_user}"]

    # файл БД для записи
    with open(JSON_FILE, "w", encoding="utf-8") as wallet:
        json.dump(data, wallet, indent=4, ensure_ascii=False)

    await bot.send_message(
        chat_id=id_user, text=f"Ваш баланс пополнен на {add_ballance}"
    )
    await bot.send_message(chat_id=id_user, text=f"Ваш баланс = {user_ballance}")
    await message.delete()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
