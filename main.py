import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.config import load_config, Config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():

    logger.info("Start Bot")

    config: Config = load_config()

    bot = Bot(config.bot.token)
    dp = Dispatcher()

    # Подключаем роутеры

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stop Bot")
