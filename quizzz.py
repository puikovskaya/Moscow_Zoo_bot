import aiohttp
import asyncio
import requests
import json
from bs4 import BeautifulSoup

from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.formatting import (
   Bold, as_list, as_marked_section
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, types, F

from info import dict_of_animals


router = Router()
animal = {}
photo_animal = {}

class number_of_question(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    answer_1 = State()
    answer_2 = State()
    answer_3 = State()

@router.message(Command("quiz"))
async def quiz(message: Message, state: FSMContext): # command: CommandObject,
    kb = [
        [
            types.KeyboardButton(text="Да!"),
            types.KeyboardButton(text="Нет!"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    await message.answer('Вы иногда пьёте молоко?',
                         reply_markup=keyboard
                         )
    await state.set_state(number_of_question.question_1.state)

@router.message(number_of_question.question_1)
async def q_1(message: types.Message, state: FSMContext):
    kb = [
        [
            types.KeyboardButton(text="Да!"),
            types.KeyboardButton(text="Редко. Шашлыки да!"),
            types.KeyboardButton(text="Нет!"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    if message.text == 'Да!':
        await state.set_data({'Milk': True})
        await message.answer('Любите кушать мясо?', reply_markup=keyboard)
        await state.set_state(number_of_question.question_2.state)
    elif message.text == 'Нет!':
        await state.set_data({'Milk': False})
        await message.answer('Любите кушать мясо?', reply_markup=keyboard)
        await state.set_state(number_of_question.question_2.state)
    else:
        await message.answer('Используйте кнопку для ответов.')



@router.message(number_of_question.question_2)
async def q_2(message: types.Message, state: FSMContext):
    mystate = await state.get_data()
    if message.text == 'Да!':
        mystate['Meat'] = True
        await state.set_data(mystate)
        if mystate['Milk']:
            kb = [
                [
                    types.KeyboardButton(text="Кошек!"),
                    types.KeyboardButton(text="Собак!"),
                    types.KeyboardButton(text="Всех животных!"),
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
            await message.answer('Вы больше любите кошек или собак?', reply_markup=keyboard)
        else:
            kb = [
                [
                    types.KeyboardButton(text="Зеленый"),
                    types.KeyboardButton(text="Черный"),
                    types.KeyboardButton(text="Белый"),
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
            await message.answer('Выберите цвет, который больше вам подходит', reply_markup=keyboard)
        await state.set_state(number_of_question.question_3.state)

    elif message.text == 'Нет!':
        mystate['Meat'] = False
        await state.set_data(mystate)
        if mystate['Milk']:
            kb = [
                [
                    types.KeyboardButton(text="Да! Люблю воду"),
                    types.KeyboardButton(text="Нет! Зря не намокну"),
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
            await message.answer('Вы любитель принимать ванну или находиться в воде?',
                                 reply_markup=keyboard)
        else:
            kb = [
                [
                    types.KeyboardButton(text="Да! Я в отношениях."),
                    types.KeyboardButton(text="Нет! Я один."),
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
            await message.answer('У вас есть любимый человек?',
                                 reply_markup=keyboard)
        await state.set_state(number_of_question.question_3.state)

    elif message.text == "Редко. Шашлыки да!":
        mystate['Meat'] = 'Редко'
        await state.set_data(mystate)
        if mystate['Milk']:
            kb = [
                [
                    types.KeyboardButton(text="Да! Иногда сплю очень долго"),
                    types.KeyboardButton(text="Нет! Не сплю по долгу"),
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
            await state.set_data(mystate)
            await state.set_data({'Meat': "Редко"})
            await message.answer('Иногда вы можте проспать очень много времени?', reply_markup=keyboard)
        else:
            kb = [
                [
                    types.KeyboardButton(text="Я в броне"),
                    types.KeyboardButton(text="Умело избегаю"),
                ],
            ]
            keyboard = types.ReplyKeyboardMarkup(
                keyboard=kb,
                resize_keyboard=True,
            )
            await state.set_data(mystate)
            await state.set_data({'Meat': "Редко"})
            await message.answer('Удары судьбы вы стойко выдерживаете или умело избегаете?',
                                 reply_markup=keyboard)
        await state.set_state(number_of_question.question_3.state)
    else:
        await message.answer('Используйте кнопку для ответов.')


@router.message(number_of_question.question_3)
async def q_3(message: types.Message, state: FSMContext):
    mystate = await state.get_data()

    kb = [
        [
            types.KeyboardButton(text="И кто же это?"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )

    if message.text == "Кошек!":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'Cats_lover'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Собак!":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'Dogs_lover'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Всех животных!":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'Animals_lover'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Зеленый":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'Green_lover'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Черный":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'Black_lover'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Белый":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'White_lover'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Да! Люблю воду":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'Water_lover'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Нет! Зря не намокну":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'not_Water_lover'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Да! Я в отношениях.":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'familial'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Нет! Я один.":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'not_familial'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Да! Иногда сплю очень долго":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'love_sleep'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Нет! Не сплю по долгу":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'not_love_sleep'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Я в броне":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = 'have_armor'
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)

    elif message.text == "Умело избегаю":
        await message.answer('Кажется я знаю ваше тотемное животное..', reply_markup=keyboard)
        mystate['Parametr'] = "have_stealth"
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_1.state)
    else:
        await message.answer('Используйте кнопку для ответов.')

@router.message(number_of_question.answer_1)
async def a_1(message: types.Message, state: FSMContext):
    global animal, photo_animal
    mystate = await state.get_data()
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Расскажи о нём"))
    builder.add(types.KeyboardButton(text="Написать отзыв"))
    builder.add(types.KeyboardButton(text="Поделиться результатами в соцсети", ))
    builder.add(types.KeyboardButton(text="Написать сотруднику по опеке над животным", ))
    builder.add(types.KeyboardButton(text="Попробовать ещё раз", ))
    builder.adjust(2,1,1,1)

    if message.text == "И кто же это?":
        str_anim = dict_of_animals[mystate['Parametr']][0]
        animal[message.chat.username] = dict_of_animals[mystate['Parametr']][0]
        str_http_anim = dict_of_animals[mystate['Parametr']][2]
        photo_animal[message.chat.username] = dict_of_animals[mystate['Parametr']][2]
        kb = [
            [
                types.InlineKeyboardButton(text="Поддержать животное",
                                           url='https://moscowzoo.ru/my-zoo/become-a-guardian/')
            ]
        ]
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=kb
        )
        await message.answer('Думаю, что ваше тотемное животное это..',
                             reply_markup=builder.as_markup(resize_keyboard=True))
        await message.answer_photo(photo=f'{str_http_anim}',
                                   caption=f'{str_anim}!\n\n'
                             f'Вы можете поддержать животное взяв его под опеку '
                             f'в нашем зоопарке, кликай по кнопке, чтобы узнать подробности.\n\n'
                             f'Будем благодарны, если напишите отзыв о нашей викторине!',
                             reply_markup=keyboard)
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_2.state)
    else:
        await message.answer('Используйте кнопку для ответов.')


@router.message(number_of_question.answer_2)
async def a_2(message: types.Message, state: FSMContext):
    mystate = await state.get_data()
    if message.text == "Написать отзыв":
        kb = [[
            types.KeyboardButton(text="1"), types.KeyboardButton(text="2"),
            types.KeyboardButton(text="3"), types.KeyboardButton(text="4"),
            types.KeyboardButton(text="5")
               ]]
        builder = ReplyKeyboardBuilder(kb)
        builder.adjust(2, 2, 1)
        await message.answer('Напишите отзыв следующим сообщением '
                             'или просто поставьте оценку от 1 до 5',
                             reply_markup=builder.as_markup(resize_markup = True))
        await state.set_data(mystate)
        await state.set_state(number_of_question.answer_3.state)
    elif message.text == "Расскажи о нём":
        http = dict_of_animals[mystate['Parametr']][1]
        response = requests.get(
            f'{http}', verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        Text_of_animal = soup.find('div', class_='dp-content-inner')
        bot_list_of_msg = []
        if dict_of_animals[mystate['Parametr']][0] == "Обыкновенный шакал" or dict_of_animals[mystate['Parametr']][0] == "Японский макак":
            bot_list_of_msg.append(Text_of_animal.text)
            bot_msg = ''.join(bot_list_of_msg)
            bot_msg = bot_msg.replace('\n\n\n','\n')
            bot_msg = bot_msg.replace('\n\n\n', '\n\n')
        else:
            lines_with_p = Text_of_animal.find_all('p')
            for p in lines_with_p:
                bot_list_of_msg.append(p.text)
            bot_msg = ''.join(bot_list_of_msg)
        if len(bot_msg) > 4096:
            # если сообщение длиннее допустимого для отправки
            bot_msgs = [bot_msg[i:i + 4096] for i in range(0, len(bot_msg), 4096)]
            for part_msg in bot_msgs:
                await message.answer(part_msg)
        else:
            await message.answer(f'{bot_msg}')
    elif message.text == "Попробовать ещё раз":
        await quiz(message, state)
    else:
        await message.answer('Используйте кнопку для ответов.')



@router.message(number_of_question.answer_3)
async def a_3(message: types.Message, state: FSMContext):
    mystate = await state.get_data()
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Расскажи о нём"))
    builder.add(types.KeyboardButton(text="Написать отзыв"))
    builder.add(types.KeyboardButton(text="Поделиться результатами в соцсети"))
    builder.add(types.KeyboardButton(text="Написать сотруднику по опеке над животным"))
    builder.add(types.KeyboardButton(text="Попробовать ещё раз"))
    builder.adjust(2, 1, 1, 1)
    with open('Отзывы.txt', 'a') as file:
        file.write(f'{message.chat.username}: {message.text}; ')
    await message.answer('Спасибо за ваш отзыв!',
                         reply_markup=builder.as_markup(resize_keyboard=True))
    await state.set_data(mystate)
    await state.set_state(number_of_question.answer_2.state)

@router.message()
async def commands2(message: types.Message):
    response = as_list(
        as_marked_section(
            Bold("Жми:"),
            "/quiz- начать викторину тотемного животного\n"
            "/start - обновить диалог",
            marker="✅ ",
        ),
    )
    await message.answer(
        **response.as_kwargs()
    )