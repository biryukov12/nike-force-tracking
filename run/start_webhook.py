import logging

from aiogram import Dispatcher
from aiogram.utils.executor import start_webhook

from bot.bot import bot, dp, scheduler

from config import webhook_config


log = logging.getLogger(__name__)


async def on_startup(dp: Dispatcher):
    await bot.delete_webhook()
    scheduler.start()
    log.warning('Starting connection...')
    await bot.set_webhook(webhook_config.WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dp: Dispatcher):
    log.warning('Shutting down...')
    scheduler.remove_all_jobs()
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    log.warning('Bye!')


if __name__ == '__main__':
    log.warning("Bot started webhook..")
    start_webhook(
        dispatcher=dp,
        webhook_path=webhook_config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=webhook_config.WEBAPP_HOST,
        port=webhook_config.WEBAPP_PORT,
    )
