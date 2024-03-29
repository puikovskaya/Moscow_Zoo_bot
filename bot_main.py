import asyncio

import logging
import sys

import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section
)

from quizzz import router, animal, photo_animal

TOKEN = '7123492389:AAEM-amJfW7Rbqe3X9BTeAzvrsTXMqZxmv4'

bot = aiogram.Bot(TOKEN)
dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    kb = [
        [
            types.KeyboardButton(text="Начнём"),
            types.KeyboardButton(text="Описание бота"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Привет! Здесь ты сможешь узнать своё тотемное животное из Московского зоопарка, начнём?",
                         reply_markup=keyboard)


@dp.message(F.text.lower() == "начнём")
async def commands(message: types.Message):
    response = as_list(
        as_marked_section(
            Bold("Жми:"),
            "/quiz- начать викторину тотемного животного\n",
            marker="✅ ",
        ),
    )
    await message.answer(
        **response.as_kwargs()
    )


@dp.message(F.text.lower() == "написать сотруднику по опеке над животным")
async def tell(message: types.Message):
    chat_id = '583478595'  # chatid сотрудника
    sotrudnik = '@dofermin'
    chat_user = message.chat.username
    await bot.send_message(chat_id, f"@{chat_user} прошёл викторину, "
                                    f"его результат: {animal[message.chat.username]}")
    await message.answer(f'Сотрудник {sotrudnik} скоро свяжется с вами. '
                         f'Можете написать ему интересующий вас вопрос.')


@dp.message(F.text.lower() == "поделиться результатами в соцсети")
async def tell(message: types.Message):
    # Условная функция
    chat_id = '583478595'
    await bot.send_photo(chat_id, photo=f'{photo_animal[message.chat.username]}',
                         caption=f'Моё тотемное животное - {animal[message.chat.username]}!\n\n'
                                 f'Жду, когда пройдёшь ты: https://t.me/quiz_for_Moscow_zoo_bot')


@dp.message(F.text.lower() == "описание бота")
async def description(message: types.Message):
    await message.answer("Я помогаю определить ваше тотемное животное")


async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
