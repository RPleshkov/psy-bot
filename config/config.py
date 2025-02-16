from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class PostgresConfig:
    db_url: str


@dataclass
class Config:
    bot: TgBot
    nats: NatsConfig
    postgres: PostgresConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        bot=TgBot(token=env("BOT_TOKEN")),
        nats=NatsConfig(servers=env.list("NATS_SERVERS")),
        postgres=PostgresConfig(db_url=env("DB_URL")),
    )
