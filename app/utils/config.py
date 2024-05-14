from dataclasses import dataclass

@dataclass
class Config:
    BOT_TOKEN: str
    POSTGRESQL: str
    POSTGRESQL_FOR_ALEMBIC: str
    CHAT_ID: str

# 6924525672:AAHjaj5OXNTTLRk1QsHroBwDhgeLft5iKsw
def load_config() -> Config:
    return Config(BOT_TOKEN='6924525672:AAHjaj5OXNTTLRk1QsHroBwDhgeLft5iKsw',
                  POSTGRESQL='postgresql+asyncpg://postgres:356211kKmM@213.171.8.131:5432/bot',
                  POSTGRESQL_FOR_ALEMBIC='postgresql+asyncpg://postgres:356211kKmM@213.171.8.131:5432/bot',
                  CHAT_ID='@aassswwwwwwq')

settings = load_config()
