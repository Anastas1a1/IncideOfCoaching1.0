
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, ChatActions
from asgiref.sync import sync_to_async
import asyncio
import logging
from .bot_initializer import bot, storage, dp
from . import markup as nav
from .functions import file_info
from .functions import delete_message, send_material, send_progress, file_info
from . import db, google_db
from .markup import YearsCallback, MonthCallback, ThemesCallback
import os
from dotenv import load_dotenv
load_dotenv()
import ast

ADMINS_str = os.getenv("ADMINS")
ADMINS = ast.literal_eval(ADMINS_str)

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


@dp.message_handler(state=Form.admin_mes, content_types=['text', 'document', 'audio', 'photo', 'video', 'voice', 'animation', 'sticker'])
async def set_admin_mes(message: types.Message, state: FSMContext):
    if message.text:
        async with state.proxy() as data:
            data['admin_mes'] = message.text
            print( data['admin_mes'])    
            await bot.send_message(message.chat.id, 'Каким пользователям нужно отправить сообщение?\n"{}"'.format(data['admin_mes']), reply_markup=nav.SendMesMenu)
            await Form.last_send.set()
    else:
        file_id, file_name, ext = await file_info(message)
        print(file_id, file_name, ext)
        if file_id:
            async with state.proxy() as data:
                data['admin_file_id'] = file_id
                data['admin_file_name'] = file_name
                data['admin_file_ext'] = ext
                await bot.send_message(message.chat.id, 'Каким пользователям нужно отправить сообщение?', reply_markup=nav.SendMesMenu)
                await send_material(data['admin_file_ext'], message.chat.id, data['admin_file_id'], data['admin_file_name'])
        await Form.last_send.set()


@dp.callback_query_handler(text_contains="btn:SendMesMenu:", state=Form.last_send)
async def admin_menu_send_mes(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    category = call.data.split(':')[2]
    tg_ids = await sync_to_async(db.get_tg_id)(category)
    if tg_ids:
        async with state.proxy() as data:
            data['last_send'] = []
            for id in tg_ids:
                if 'admin_mes' in data:
                    data['last_send'].append(await bot.send_message(int(id), data['admin_mes']))
                elif 'admin_file_id' in data:
                    data['last_send'].append(await send_material(data['admin_file_ext'], int(id), data['admin_file_id'], data['admin_file_name']))
            await bot.send_message(call.message.chat.id, 'Сообщения пользователям отправлены.')
    else:
        await bot.send_message(call.message.chat.id, 'Произошла ошибка. Сообщения не отправлены')
    
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

        file, file_tg = await sync_to_async(db.get_files_by_name)(file_name)
        
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

def setup(dp):
    dp.register_callback_query_handler(admin_menu, text_contains="AdminMenu")
    dp.register_message_handler(set_admin_mes, state=Form.admin_mes)
    dp.register_callback_query_handler(admin_menu_send_mes, text_contains="btn:SendMesMenu:", state=Form.last_send)
    dp.register_message_handler(download_file, state=Form.admin_file_id, content_types=['document', 'audio', 'photo', 'video', 'voice', 'animation', 'sticker'])
    dp.register_callback_query_handler(choice_admin_year, YearsCallback.filter(space='ChoiceAdminYear'), state=Form.admin_year)
    dp.register_message_handler(include_admin_year, state=Form.admin_year)
    dp.register_callback_query_handler(choice_admin_month, MonthCallback.filter(space="ChoiceAdminMonth"), state=Form.admin_year)
    dp.register_message_handler(include_admin_category, state=Form.admin_category)
    dp.register_callback_query_handler(choice_admin_theme, ThemesCallback.filter(space="ChoiceAdminThemes"), state=Form.admin_topic)
    dp.register_message_handler(include_admin_topic, state=Form.admin_topic)
    dp.register_callback_query_handler(add_tg_file_to_db, text_contains="HaveFileMenu", state=Form.admin_agree)
