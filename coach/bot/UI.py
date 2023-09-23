from asgiref.sync import sync_to_async
import logging
import os
import ast
from contextlib import suppress
import requests
import aiogram.utils.markdown as md
# import aiogram.methods
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ParseMode
from aiogram.types import (
    Audio,
    Document,
    PhotoSize,
    Video,
    Voice
)
from aiogram.types import ChatActions
from aiogram.types.message import ContentType, ContentTypes
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageCantBeEdited,
                                      MessageToDeleteNotFound,
                                      MessageToEditNotFound)
from aiogram.types.input_file import InputFile
from dotenv import load_dotenv

import os
# import django


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminsite.settings')

# django.setup()

from . import markup as nav
from . import db, google_db
from .markup import YearsCallback, MonthCallback, ThemesCallback
from .functions import delete_message, send_material, send_progress, file_info
from .bot_initializer import bot, storage, dp

# from .admin_bot import Form


# from coaching.database import server



# from adminpanel import views as server

load_dotenv()
TOKEN = os.getenv("TOKEN")
PAYMENTS_TOKEN = os.getenv("PAYMENTS_TOKEN")
ADMINS_str = os.getenv("ADMINS")
ADMINS = ast.literal_eval(ADMINS_str)
PRICE_FIRST = types.LabeledPrice(label="Подписка на 1 месяц", amount=20000*100)
PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=10000*100)


# bot = Bot(TOKEN, parse_mode="HTML")
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)
# logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
#                     level=logging.INFO)


class Form(StatesGroup):
    name = State()

# ______________________________________________________________________Commands
@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    plus = await sync_to_async(db.is_plus)(message.chat.id)
    await sync_to_async(db.new_user_plus)(message.chat.first_name, message.chat.id, False)
    await bot.send_message(message.from_user.id,
                           '''Добро пожаловать, {0.first_name}! Здравствуйте! Я бот компании Incide of Coaching. 
                Рад приветствовать вас и предложить подписку на наши материалы. 
                Наша компания  предлагаеет высококачественные статьи, видео и аудиоматериалы по темам развития личности, психологии отношений, самосовершенствования и многому другому. 
                Подписавшись на нашу рассылку, вы получите доступ к нашим эксклюзивным материалам в течение месяца. 
                Кроме того, у нас есть дегустационное меню, которое вы можете посмотреть, чтобы ознакомиться с нашими возможностями. Желаете подписаться на наши материалы?
                           '''.format(message.from_user))


    plus = await sync_to_async(db.is_plus)(message.chat.id)
    if plus:
        await bot.send_message(message.from_user.id, f"Здравствуйте, {plus}! Рад Вас видеть! Что я могу для Вас сделать?", reply_markup=nav.UserMainMenu)
    else:
        await bot.send_message(message.from_user.id, "Что я могу для Вас сделать?", reply_markup=nav.UserMainMenu)


@dp.message_handler(commands=['menu'])
async def command_start(message: types.Message):
    plus = await sync_to_async(db.is_plus)(message.chat.id)
    if plus:
        await bot.send_message(message.from_user.id, f'{plus}, что я могу для Вас сделать?', reply_markup=nav.UserMainMenu)
    else:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, что я могу для Вас сделать?', reply_markup=nav.UserMainMenu)


@dp.message_handler(commands=['admin'])
async def command_info(message: types.Message):
    if message.chat.id in ADMINS:
        await bot.send_message(message.from_user.id, 'Панель управления администратора.', reply_markup=nav.AdminMenu)
    else:
        await bot.send_message(message.chat.id, 'У вас нет доступа.')

# ______________________________________________________________________Cancel


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='Отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    await state.get_state()
    await state.finish()
    await bot.send_message(message.chat.id, 'Операция прервана', reply_markup=nav.UserMainMenu)


@dp.callback_query_handler(text="cancel", state="*")
async def cancel_inline(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    await state.get_state()
    await state.finish()
    await bot.send_message(call.message.chat.id, 'Операция прервана', reply_markup=nav.UserMainMenu)


# # ______________________________________________________________________Admin

# @dp.callback_query_handler(text_contains="AdminMenu")
# async def admin_menu(call: CallbackQuery):
#     await bot.edit_message_reply_markup(
#         chat_id=call.from_user.id,
#         message_id=call.message.message_id,
#         reply_markup=None
#     )
#     if call.data == "btn:AdminMenu:message":
#         await bot.send_message(call.message.chat.id, 'Введите текст сообщения или отправьте файл')
#         await Form.admin_mes.set()

#     elif call.data == "btn:AdminMenu:del_message":
#         try:
#             for mes in last_send:
#                 asyncio.create_task(delete_message(mes, 0))
#                 print('удалено:  ', mes)
#         except:
#             await bot.send_message(call.message.chat.id, 'Сообщения не удалены')
#     elif call.data == "btn:AdminMenu:docs":
#         await call.message.answer('Отправьте в ответ файлы (они должны храниться на гугл диске и иметь то же название для правильной классификации)')
#         await Form.admin_file_id.set()
        
#     elif call.data == 'btn:AdminMenu:sync_db':
#         await sync_to_async(google_db.list_files_recursively)()


# _____________________________________________________________________________________________________UserMainMenu

@dp.callback_query_handler(text_contains="UserMainMenu")
async def users_main_menu(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    user_data = await sync_to_async(db.is_plus)(call.message.chat.id)
    if call.data == 'btn:UserMainMenu:subscription':
        if not user_data:
            await call.message.answer(f'Расширенный план включает в себя...\nСтоимость... Для вас 20')
            await call.message.answer(f'Начать оформление?', reply_markup=nav.SubscriptionMenu1)
        elif user_data:
            async with state.proxy() as data:
                data['name'] = user_data
            await call.message.answer('Расширенный план включает в себя...\nСтоимость... Для вас 10')
            await call.message.answer('''Прдление подписки на 1 мес на имя {}.\nВсе верно или изменить данные?'''.format(user_data), reply_markup=nav.SubscriptionMenu2)

    elif call.data == 'btn:UserMainMenu:access':
        print('test1')
        docs  = await sync_to_async(db.my_info)(call.message.chat.id)
        
        if not docs:
            await call.message.answer('''У вас нет подписки, потому предлагаем вам наше дегустационное меню!\nЕсли хотите больше материалов, оформите нашу подписку''')
            docs  = await sync_to_async(db.degust)(call.message.chat.id)
        print(docs)
            
        if not docs:
            for admin in ADMINS:
                await bot.send_message(admin, f'Ошибка в отправке дегустационного меню пользователю {call.message.id}')
        else:   
            print('Yeeeess')
            for doc in docs:
                await send_material(doc[0], doc[1], doc[2], doc[3])
        
        await state.finish()
        await bot.send_message(call.message.chat.id, 'Меню:', reply_markup=nav.UserMainMenu)

        # if not docs:
        #     await call.message.answer('''У вас нет подписки, потому предлагаем вам наше дегустационное меню!\n
        #                               Если хотите больше материалов, оформите нашу подписку''')

        # elif len(month) < 1:
        #     if len(docs) == 1 and 'Дегустационное меню' in month:
        #         await call.message.answer('У вас нет подписки, потому предлагаем вам наше дегустационное меню!\nЕсли хотите больше материалов, попроуйте нашу подписку')
        #     else:
        #         await call.message.answer('Отправляю доступные вам материалы!')
                # for category in month:
                # await send_materials(call.message.chat.id, '2023/Дегустационное меню')

        # else:
        #     await call.message.answer('Выберете из доступного', reply_markup=nav.month_markup(month))


# _____________________________________________________________________________________________________DocsMonthMenu

# @dp.callback_query_handler(text_contains="ChoiceMonth")
# async def users_main_menu(call: CallbackQuery, state: FSMContext):
#     await bot.edit_message_reply_markup(
#         chat_id=call.from_user.id,
#         message_id=call.message.message_id,
#         reply_markup=None
#     )

#     print(call.data)

#     if 'all' in call.data:
#         month = server.docs_info(call.message.chat.id)
    # c_data = call.data[]

        # _________________________________________________________________________________________TODO


@dp.callback_query_handler(text_contains="SubscriptionMenu")
async def users_main_menu(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    if call.data == "btn:SubscriptionMenu:yes":
        await call.message.answer('Отправьте в ответ имя и фамилию')
        await Form.name.set()
        
    elif call.data == "btn:SubscriptionMenu:have_name":
        if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(call.message.chat.id, "Тестовый платеж!!!")

        await bot.send_invoice(call.message.chat.id,
                               title="Подписка на бота",
                               description="Активация подписки на бота на 1 месяц",
                               provider_token=PAYMENTS_TOKEN,
                               currency="rub",
                               is_flexible=False,
                               prices=[PRICE],
                               start_parameter="one-month-subscription",
                               payload="test-invoice-payload")


@dp.message_handler(state=Form.name)
async def include_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

        if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
            await bot.send_message(message.chat.id, "Тестовый платеж!!!")
    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE_FIRST],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


# _____________________________________________________________________________________________________Check_pay

# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message, state=FSMContext):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!")
    async with state.proxy() as data:
        await sync_to_async(db.new_user_plus)(data['name'], message.chat.id, True)

def setup(dp):
    dp.register_callback_query_handler(users_main_menu, text_contains="UserMainMenu")
    dp.register_message_handler(include_name, state=Form.name)
    dp.register_pre_checkout_query_handler(pre_checkout_query)
    dp.register_message_handler(successful_payment, content_types=types.ContentType.SUCCESSFUL_PAYMENT)
