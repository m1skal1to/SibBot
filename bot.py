import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import load_config
from handlers.echo import register_echo

logger = logging.getLogger(__name__)


def register_handlers(dp):
    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info('Bot started')

    config = load_config()
    storage = MemoryStorage()
    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)
    webhook_url = config.bot.token + config.bot.app_url

    register_handlers(dp)

    async def on_startup():
        await bot.set_webhook(webhook_url, drop_pending_updates=True)

    async def on_shutdown():
        await bot.delete_webhook()

    try:
        await start_webhook(
            dispatcher=dp,
            webhook_path=config.bot.token + config.bot.app_url,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=config.bot.app_url,
            port=config.bot.port
        )
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped')
