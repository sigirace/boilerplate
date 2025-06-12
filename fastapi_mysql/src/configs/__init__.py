from functools import lru_cache
from configs.mysql_setting import MysqlSetting
from configs.jwt_setting import JWTSetting
from configs.mongo_setting import MongoSetting


class Settings:

    def __init__(self):
        self.mysql = MysqlSetting()
        self.jwt = JWTSetting()
        self.mongo = MongoSetting()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
