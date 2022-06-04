import logging

from aiogram import executor

from bot import dp

log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.warning("Bot started polling...")
    executor.start_polling(dp, skip_updates=True)
