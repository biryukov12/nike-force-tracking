import logging
import aiohttp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.utils.executor import start_webhook
from aiogram.utils.markdown import hbold
from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Token
BOT_TOKEN = getenv('BOT_TOKEN')

# Heroku app name
HEROKU_APP_NAME = getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(getenv('PORT'))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
scheduler = AsyncIOScheduler()

# UUIDs for parse
men = '0f64ecc7-d624-4e91-b171-b83a03dd8550,'
unisex = '568f7ffc-ee7f-49ed-98eb-0b94708d6e88,'
shoes = '16633190-45e5-4810-a068-232ac7aea82c,'
air_force_1 = '8529ff38-7de8-4f69-973c-9fdbfb102ed2,'
low_top = 'abb0cf06-d7c2-41b7-97ba-c6d5ef5f43ed,'
mid_top = '2797eaa0-4166-486e-96d1-95ad2495b58d,'
high_top = '97a10d31-545b-46d9-ad76-8b4801dd7766,'
footwear_size = '5c357820-4cff-37a6-b815-984753484f06,'  # 7.5 US
cold_weather = 'b3552af0-55fc-4196-99d2-6fc8b834b9f6'

url_with_filter = 'https://api.nike.com/cic/browse/v1?queryid=filteredProductsWithContext' \
                  '&uuids=' + men + shoes + air_force_1 + low_top + mid_top + high_top + footwear_size + \
                  '&language=ru' \
                  '&country=RU' \
                  '&channel=NIKE'

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/95.0.4638.54 Safari/537.36"
}


async def get_force(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url_with_filter, headers=headers) as response:
            all_data = await response.json()
            products = all_data['data']['filteredProductsWithContext']['products']
    if products is None:
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
        await get_force(message)
    except Exception as e:
        await message.answer(str(e))
        print(e)


@dp.message_handler(Text(equals='Schedule: every 1 hour'))
async def schedule_start(message: types.Message):
    try:
        await message.answer('Schedule parsing: every 1 hour')
        logging.warning('Starting schedule parsing every 1 hour...')
        scheduler.add_job(get_force, trigger='interval', hours=1, args=(message,), id='1_hour')
    except Exception as e:
        await message.answer(str(e))
        print(e)


@dp.message_handler(Text(equals='Cancel task'))
async def schedule_clear(message: types.Message):
    logging.warning('Removing schedule parsing every 1 hour...')
    scheduler.remove_all_jobs()
    await message.answer('Schedule parsing removed')


async def on_startup(dp):
    await bot.delete_webhook()
    scheduler.start()
    logging.warning('Starting connection...')
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Shutting down...')
    scheduler.remove_all_jobs()
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
