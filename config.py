from environs import Env
from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str
    bot_admin: str
    use_redis: bool


@dataclass
class DbConfig:
    user: str
    password: str
    host: str
    name: str


@dataclass
class Config:
    bot: BotConfig
    db: DbConfig


def load_config():
    env = Env()
    env.read_env('.env')

    return Config(
        bot= BotConfig(
            token=env.str('BOT_TOKEN'),
            bot_admin=env.int('BOT_ADMIN'),
            use_redis=env.bool('REDIS')
        ),
        db=DbConfig(
            user=env.str('DB_USER'),
            password=env.str('DB_PASS'),
            host=env.str('DB_HOST'),
            name=env.str('DB_NAME')
        )
    )
