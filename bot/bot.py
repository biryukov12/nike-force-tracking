import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.bot_config import BOT_TOKEN

from dotenv import load_dotenv

from parse.parse import parsing_data

load_dotenv()

log = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
scheduler = AsyncIOScheduler()


async def get_data(message: types.Message):
    products = await parsing_data()
    if parsing_data is None:
        log.warning('No force')
        await bot.send_message(message.chat.id, 'No force')
    else:
        for i in range(len(products)):
            title = products[i]['title']
            current_price = products[i]['price']['currentPrice']
            product_url = 'https://nike.com/ru' + products[i]['url'].strip('{countryLang}')
            answer = f"{hbold(title)}\n" \
                     f"{hbold(current_price)}₽\n" \
                     f"{product_url}"
            await bot.send_message(message.chat.id, answer)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Once', 'Schedule: every 1 hour', 'Cancel task']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Select: once parsing or schedule parsing', reply_markup=keyboard)


@dp.message_handler(Text(equals='Once'))
async def once(message: types.Message):
    try:
        await get_data(message)
    except Exception as e:
        log.error(e)


@dp.message_handler(Text(equals='Schedule: every 1 hour'))
async def schedule_start(message: types.Message):
    try:
        await message.answer('Schedule parsing: every 1 hour')
        log.warning('Starting schedule parsing every 1 hour...')
        scheduler.add_job(get_data, trigger='interval', hours=1, args=(message,), id='1_hour')
    except Exception as e:
        log.error(e)


@dp.message_handler(Text(equals='Cancel task'))
async def schedule_clear(message: types.Message):
    log.warning('Removing schedule parsing every 1 hour...')
    scheduler.remove_all_jobs()
    await message.answer('Schedule parsing removed')
