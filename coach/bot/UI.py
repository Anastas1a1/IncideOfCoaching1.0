from asgiref.sync import sync_to_async
import asyncio
import logging
import os
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
from tqdm import tqdm
from aiogram.types import ChatActions
from aiogram.types.message import ContentType, ContentTypes
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageCantBeEdited,
                                      MessageToDeleteNotFound,
                                      MessageToEditNotFound)
from aiogram.types.input_file import InputFile
from dotenv import load_dotenv

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminsite.settings')

django.setup()

from . import markup as nav
from . import db, google_db
from .markup import YearsCallback, MonthCallback, ThemesCallback

# from coaching.database import server



# from adminpanel import views as server

load_dotenv()
TOKEN = os.getenv("TOKEN")
PAYMENTS_TOKEN = os.getenv("PAYMENTS_TOKEN")

PRICE_FIRST = types.LabeledPrice(label="Подписка на 1 месяц", amount=20000*100)
PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=10000*100)

ADMINS = [1065409295, 63746635]
bot = Bot(TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


class Form(StatesGroup):
    admin_file_id = State()
    admin_file_name = State()
    admin_file_ext = State()
    admin_year = State()
    admin_category = State()
    admin_topic = State()
    admin_agree = State()

    name = State()

    admin_mes = State()
    last_send = State()


last_send = []
# ______________________________________________________________________Delete_mes


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


async def send_progress(progress_message, progress: int):
    empty_blocks = 10 - progress
    filled_emoji = '🟩' * progress
    empty_emoji = '▫️' * empty_blocks
    progress_bar = f'{filled_emoji}{empty_emoji}'
    await progress_message.edit_text(progress_bar)
# ______________________________________________________________________send_materials


async def send_material(ext, user_id, file_id, file_name):
    match ext:
        case 'document':
            mes = await bot.send_document(
                user_id, file_id,
                caption=f"{file_name}",
                disable_notification=True,
                protect_content=True
            )
        case 'audio':
            mes = await bot.send_audio(
                user_id, file_id,
                caption=f"{file_name}",
                disable_notification=True,
                protect_content=True
            )
        case 'photo':
            mes = await bot.send_photo(
                user_id, file_id,
                disable_notification=True,
                protect_content=True
            )
        case 'video':
            mes = await bot.send_video(
                user_id, file_id,
                caption=f"{file_name}",
                disable_notification=True,
                protect_content=True
            )
        case 'voice':
            mes = await bot.send_document(
                user_id, file_id,
                disable_notification=True,
                protect_content=True
            )
        case 'animation':
            mes = await bot.send_animation(
                user_id, file_id,
                disable_notification=True,
                protect_content=True
            )
        case 'video_note':
            mes = await bot.send_video(
                user_id, file_id,
                disable_notification=True,
                protect_content=True
            )
    return mes


async def file_info(message):
    print('yes')
    file_id = None
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        ext = 'document'

    elif message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.file_name
        ext = 'audio'

    elif message.photo:
        file_id = message.photo[-1].file_id
        file_name = '-'
        ext = 'photo'

    elif message.video:
        file_id = message.video.file_id
        file_name = message.video.file_name
        ext = 'video'

    elif message.voice:
        file_id = message.voice.file_id
        file_name = '-'
        ext = 'voice'

    elif message.animation:
        file_id = message.animation.file_id
        file_name = '-'
        ext = 'animation'

    elif message.video_note:
        file_id = message.video_note.file_id
        file_name = '-'
        ext = 'video_note'
    elif message.sticker:
        file_id = message.sticker.file_id
        file_name = '-'
        ext = 'sticker'
    if file_id:

        return file_id, file_name, ext

# async def send_materials(user_id: int, category: list):
#     headers_1 = []

#     year, month = category.split('/')
#     if month not in headers_1:
#         await bot.send_message(user_id, '___<b>'+month+'</b>___', parse_mode='HTML')
#         headers_1.append(month)

#     docs = server.get_themes(year, month)

#     if not docs:
#         await bot.send_message(user_id, 'Произошла ошибка')
#     else:
#         headers_2 = []
#         for doc in docs:
#             print(doc)
#             path = 'docs/'+ year +'/' + month + '/'
#             if os.path.exists(path) == False:
#                 path = 'docs/'+ year +'/' + month + ' /'

#             if doc[0] == '-':
#                 path += doc[1]
#             else:
#                 path += doc[0]+ '/'+ doc[1]
#                 if doc[0] not in headers_2:
#                     await bot.send_message(user_id,'<b>'+doc[0]+'</b>', parse_mode='HTML')
#                     headers_2.append(doc[0])
#             print(path)

#             if os.path.exists(path):
#                 with open(path, 'rb') as file:
#                     filename = os.path.basename(path)
#                     _, file_extension = os.path.splitext(filename)
#                     if file_extension in ['.jpg', '.jpeg', '.png']:
#                         photo = InputFile(path)
#                         await bot.send_photo(
#                             user_id, file,
#                             caption = f"{filename}\n\nОтправлено через Telegram-бота",
#                             disable_notification = True,
#                             protect_content = True
#                         )
#                     elif file_extension in ['.ppt', '.pptx', '.pdf', '.doc', '.docx']:
#                         await bot.send_document(
#                             user_id, file,
#                             caption = f"{filename}\n\nОтправлено через Telegram-бота",
#                             disable_notification = True,
#                             protect_content = True
#                         )

#                     elif file_extension == '.mp4':
#                         await bot.send_video(
#                             user_id, file,
#                             caption = f"{filename}\n\nОтправлено через Telegram-бота",
#                             disable_notification = True,
#                             protect_content = True
#                         )
#                     elif file_extension == ['.mp3', '.m4a']:
#                         await bot.send_audio(
#                             user_id, file,
#                             caption = f"{filename}\n\nОтправлено через Telegram-бота",
#                             disable_notification = True,
#                             protect_content = True
#                         )

#                     else:
#                         await bot.send_message(user_id,f"Формат файла {filename} не поддерживается")
#             else:
#                 await bot.send_message(user_id,f"Файл {os.path.basename(path)} не найден")


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

    # await bot.send_message(message.from_user.id, 'Некоторое описание\nНачнем?', reply_markup = nav.UserMainMenu)

    plus = await sync_to_async(db.is_plus)(message.chat.id)
    if plus:
        await bot.send_message(message.from_user.id, f"Здравствуйте, {plus}! Рад Вас видеть! Что я могу для Вас сделать?", reply_markup=nav.UserPlusMainMenu)
    else:
        await bot.send_message(message.from_user.id, "Что я могу для Вас сделать?", reply_markup=nav.UserMainMenu)


@dp.message_handler(commands=['menu'])
async def command_start(message: types.Message):
    plus = await sync_to_async(db.is_plus)(message.chat.id)
    if plus:
        await bot.send_message(message.from_user.id, "{plus}, что я могу для Вас сделать?", reply_markup=nav.UserPlusMainMenu)
    else:
        await bot.send_message(message.from_user.id, "{0.first_name}, что я могу для Вас сделать?", reply_markup=nav.UserMainMenu)


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


# ______________________________________________________________________Admin

@dp.callback_query_handler(text_contains="AdminMenu")
async def admin_menu(call: CallbackQuery):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    if call.data == "btn:AdminMenu:message":
        await bot.send_message(call.message.chat.id, 'Введите текст сообщения или отправьте файл')
        await Form.admin_mes.set()

    elif call.data == "btn:AdminMenu:del_message":
        try:
            for mes in last_send:
                asyncio.create_task(delete_message(mes, 0))
                print('удалено:  ', mes)
        except:
            await bot.send_message(call.message.chat.id, 'Сообщения не удалены')
    elif call.data == "btn:AdminMenu:docs":
        await call.message.answer('Отправьте в ответ файлы (они должны храниться на гугл диске и иметь то же название для правильной классификации)')
        await Form.admin_file_id.set()
        
    elif call.data == 'btn:AdminMenu:sync_db':
        await sync_to_async(google_db.list_files_recursively)()

# ______________________________________________________________________AdminSendMes


@dp.message_handler(state=Form.admin_mes)
async def set_admin_mes(message: types.Message, state: FSMContext):
    if message.text:
        async with state.proxy() as data:
            data['admin_mes'] = message.text
    else:
        file_id, file_name, ext = await file_info(message)
        if file_id:
            async with state.proxy() as data:
                data['admin_file_id'] = file_id
                data['admin_file_name'] = file_name
                data['admin_file_ext'] = ext
        await bot.send_message(message.chat.id, 'Каким пользователям нужно отправить сообщение?\n"{}"'.format(data['admin_mes']), reply_markup=nav.SendMesMenu)
        await Form.last_send.set()


@dp.callback_query_handler(text_contains="btn:SendMesMenu:", state=Form.last_send)
async def admin_menu_send_mes(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    category = call.data.split(':')[2]
    tg_ids = sync_to_async(db.get_tg_id)(category)
    if tg_ids:
        async with state.proxy() as data:
            data['last_send'] = []
            for id in tg_ids:
                if data['admin_mes']:
                    data['last_send'].append(await bot.send_message(int(id), data['admin_mes']))
                elif data['admin_file_id']:
                    data['last_send'].append(await send_material(data['admin_file_ext'], int(id), data['admin_file_id'], data['admin_file_name']))

        await bot.send_message(call.message.chat.id, 'Сообщения пользователям отправлены.')
    else:
        await bot.send_message(call.message.chat.id, 'произошла ошибка. Сообщения не отправлены')
    await state.finish()


# _____________________________________________________________________________________________________TO DO

@dp.message_handler(state=Form.admin_file_id, content_types=['document', 'audio', 'photo', 'video', 'voice', 'animation', 'sticker'])
async def download_file(message: types.Message, state: FSMContext):
    progress_message = await bot.send_message(message.chat.id, '▫️'*10)
    await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_DOCUMENT)
    await send_progress(progress_message, 1)

    file_id, file_name, ext = await file_info(message)

    await send_progress(progress_message, 4)
    if file_id:
        async with state.proxy() as data:
            data['admin_file_id'] = file_id
            data['admin_file_name'] = file_name
            data['admin_file_ext'] = ext

        file, file_tg = await sync_to_async(db.get_file_by_name)(file_name)
        
        await send_progress(progress_message, 7)
        
        if file:
            async with state.proxy() as data:
                data['admin_year'] = file.year
                data['admin_category'] = file.category
                data['admin_topic'] = file.topic
                preview = [data['admin_year'], data['admin_category'],
                        data['admin_topic'], data['admin_file_name']]
                await send_progress(progress_message, 10)
                while '-' in preview:
                    preview.remove('-')
            await delete_message(progress_message, 1)        
            
            if file_tg:
                await delete_message(progress_message, 1)
                await bot.send_message(message.chat.id, 'В базе найден файл:\n{" --> ".join(preview)}') 
                await send_material(file_tg.ext, message.chat.id, file_tg.tg_id, file_name)
                await bot.send_message(message.chat.id, 'Выберете действие', reply_markup=nav.HaveTgFileMenu) #______________________________TODO
                await Form.admin_agree.set()
                
            else:
                await message.reply(f'Файл будет добавлен в базу как {" --> ".join(preview)}\nВсё верно или изменить путь?', reply_markup=nav.HaveFileMenu)
                await Form.admin_agree.set()
        else:
            await send_progress(progress_message, 8)
            years = await sync_to_async(db.get_unique_years)()
            await send_progress(progress_message, 10)
            await delete_message(progress_message, 1)
            await bot.send_message(message.chat.id, 'Для добавления этого файла уточните несколько моментов о нём.\nВыберете год', reply_markup=nav.years_markup(years, True))
            await Form.admin_year.set()
    else:
        await delete_message(progress_message, 1)
        await bot.send_message(message.chat.id, "Извините, я не могу обработать этот тип файла")


# _____________________________________________________________________________________________________AdminYear


@dp.callback_query_handler(YearsCallback.filter(space='ChoiceAdminYear'), state=Form.admin_year)
async def choice_admin_year(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    logging.info(f"call = {callback_data}")
    print('1')

    year = callback_data.get("year")
    if year == "Другой":
        await bot.send_message(call.message.chat.id, 'Введите год')
        await Form.admin_year.set()
    else:
        async with state.proxy() as data:
            data['admin_year'] = year
        month = await sync_to_async(db.get_unique_category)(year)
        await bot.send_message(call.message.chat.id, 'Выберете месяц подписки, либо категорию, куда следует добавить файл', reply_markup=nav.month_markup(month, year, True))


@dp.message_handler(state=Form.admin_year)
async def include_admin_year(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['admin_year'] = message.text
    await bot.send_message(message.chat.id, 'Введите месяц подписки, либо категорию, куда следует добавить файл')
    await Form.admin_category.set()


# _____________________________________________________________________________________________________AdminCategory

@dp.callback_query_handler(MonthCallback.filter(space="ChoiceAdminMonth"), state=Form.admin_year)
async def choice_admin_month(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    logging.info(f"call = {callback_data}")
    year = callback_data.get("year")
    month = callback_data.get("month")
    if month == "Другой":
        await bot.send_message(call.message.chat.id, 'Введите месяц подписки, либо категорию, куда следует добавить файл')
        await Form.admin_category.set()
    else:
        async with state.proxy() as data:
            data['admin_category'] = month
        themes = await sync_to_async(db.get_unique_topic)(year, month)
        await bot.send_message(call.message.chat.id, 'Выберете тему', reply_markup=nav.themes_markup(themes))
        await Form.admin_topic.set()


@dp.message_handler(state=Form.admin_category)
async def include_admin_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['admin_category'] = message.text

    await bot.send_message(message.chat.id, 'Введите заголовок/тему файла')
    await Form.admin_topic.set()


# _____________________________________________________________________________________________________AdminTopic

@dp.callback_query_handler(ThemesCallback.filter(space="ChoiceAdminThemes"), state=Form.admin_topic)
async def choice_admin_theme(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    logging.info(f"call = {callback_data}")
    topic = callback_data.get("topic")
    async with state.proxy() as data:
        data['admin_topic']=topic
    print(topic)

    if topic == "Другая":
        await bot.send_message(call.message.chat.id, 'Введите заголовок/тему файла')
        await Form.admin_topic.set()
    else:
        async with state.proxy() as data:
            file = [data['admin_file_ext'], data['admin_year'], data['admin_category'],
                    topic, data['admin_file_name'], data['admin_file_id']]
            await send_material(data['admin_file_ext'], call.message.chat.id, data['admin_file_id'], data['admin_file_name'])

            await bot.send_message(call.message.chat.id, f'Файл будет добавлен в базу как {", ".join(file)}\nВсё верно или изменить путь?', reply_markup=nav.HaveFileMenu)
            await Form.admin_agree.set()
            # await bot.send_message(call.message.chat.id,'Вы предоставили файл\n{}\n{}\n{}\n{}\n\nВсё верно?'.format(data['admin_year'], data['admin_category'], data['admin_topic']))

            # ______________________________________________Подтверждение


@dp.message_handler(state=Form.admin_topic)
async def include_admin_topic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['admin_topic'] = message.text
        file = [data['admin_file_ext'], data['admin_year'], data['admin_category'],
                data['admin_topic'], data['admin_file_name'], data['admin_file_id']]
        await send_material(data['admin_file_ext'], message.chat.id, data['admin_file_id'], data['admin_file_name'])

        await bot.send_message(message.chat.id, f'Файл будет добавлен в базу как {"-->".join(file)}\nВсё верно или изменить путь?', reply_markup=nav.HaveFileMenu)

        # ______________________________________________Подтверждение


@dp.callback_query_handler(text_contains="HaveFileMenu", state=Form.admin_agree)
async def add_tg_file_to_db(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    if call.data == "btn:HaveFileMenu:OK":
        async with state.proxy() as data:
            # try:
            add_file = await sync_to_async(db.add_file_tg)(data['admin_year'], 
                                                            data['admin_category'], 
                                                            data['admin_topic'],
                                                            data['admin_file_name'], 
                                                            data['admin_file_id'], 
                                                            data['admin_file_ext'])
            if add_file :
                await bot.send_message(call.message.chat.id, 'Материал успешно добавлен!')
            else:
                await bot.send_message(call.message.chat.id, 'Произошла ошибка, попробуйте ещё раз')
            await state.finish()

    if call.data == "btn:HaveFileMenu:Change":
        years = await sync_to_async(db.get_unique_years)()
        await bot.send_message(call.message.chat.id, 'Введите год подписки, в который будет добавлен файл', reply_markup=nav.years_markup(years, True))
        await Form.admin_year.set()


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
            await call.message.answer(f'Расширенный план включает в себя...\nСтоимсоть... Для вас 20')
            await call.message.answer(f'Начать оформление?', reply_markup=nav.SubscriptionMenu1)
        elif user_data:
            async with state.proxy() as data:
                data['name'] = user_data
            await call.message.answer('Расширенный план включает в себя...\nСтоимсоть... Для вас 10')
            await call.message.answer('''Прдление подписки на 1 мес на имя {}.\nВсе верно или изменить данные?'''.format(user_data), reply_markup=nav.SubscriptionMenu2)

    elif call.data == 'btn:UserMainMenu:access':
        docs  = await sync_to_async(db.my_info)(call.message.chat.id)
        
        if not docs:
            await call.message.answer('''У вас нет подписки, потому предлагаем вам наше дегустационное меню!\n
                                      Если хотите больше материалов, оформите нашу подписку''')
            docs  = await sync_to_async(db.degust)(call.message.chat.id)
            
        if not docs:
            for admin in ADMINS:
                await bot.send_message(admin, f'Ошибка в отправке дегустационного меню пользователю {call.message.id}')
        else:   
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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
