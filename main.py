import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fluentogram import TranslatorHub
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config.config import load_config, Config
from middleware.i18n import TranslatorRunnerMiddleware
from middleware.session import DbSessionMiddleware
from middleware.track_all_users import TrackAllUsersMiddleware
from storage.nats_storage import NatsStorage
from utils.i18n import create_translator_hub
from utils.nats_connect import connect_to_nats

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():

    logger.info("Start Bot")

    config: Config = load_config()

    engine = create_async_engine(url=config.postgres.db_url)

    nc, js = await connect_to_nats(servers=config.nats.servers)

    storage: NatsStorage = await NatsStorage(nc=nc, js=js).create_storage()

    bot = Bot(config.bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    translator_hub: TranslatorHub = create_translator_hub()

    Sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    # Подключаем роутеры

    # Подключаем мидлвари
    dp.update.outer_middleware(DbSessionMiddleware(Sessionmaker))
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.message.outer_middleware(TrackAllUsersMiddleware())

    try:
        await dp.start_polling(bot, _translator_hub=translator_hub)
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info("Connection to NATS closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stop Bot")
