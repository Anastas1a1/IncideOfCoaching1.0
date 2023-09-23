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
from aiogram.types import ChatActions
from aiogram.types.message import ContentType, ContentTypes
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageCantBeEdited,
                                      MessageToDeleteNotFound,
                                      MessageToEditNotFound)
from .bot_initializer import bot
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
    print('yesss2')
    match ext:
        case 'document':
            mes = await bot.send_document(
                user_id, file_id,
                caption=f"{file_name}",
                disable_notification=True
            )
        case 'audio':
            mes = await bot.send_audio(
                user_id, file_id,
                caption=f"{file_name}",
                disable_notification=True
            )
        case 'photo':
            mes = await bot.send_photo(
                user_id, file_id,
                disable_notification=True
            )
        case 'video':
            mes = await bot.send_video(
                user_id, file_id,
                caption=f"{file_name}",
                disable_notification=True
            )
        case 'voice':
            mes = await bot.send_voice(
                user_id, file_id,
                disable_notification=True
            )
        case 'animation':
            mes = await bot.send_animation(
                user_id, file_id,
                disable_notification=True
            )
        case 'video_note':
            mes = await bot.send_video(
                user_id, file_id,
                disable_notification=True
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


    return file_id, file_name, ext