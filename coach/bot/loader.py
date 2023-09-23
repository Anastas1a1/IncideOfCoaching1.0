import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adminsite.settings')
django.setup()
import logging
from .bot_initializer import dp
from . import bot_admin
from . import UI
from aiogram import executor


logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


bot_admin.setup(dp)
UI.setup(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
