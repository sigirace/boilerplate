from urllib.parse import quote_plus
from configs.setting import BaseAppSettings


class MysqlSetting(BaseAppSettings):
    mysql_host: str
    mysql_port: int
    mysql_id: str
    mysql_pw: str
    mysql_db: str

    def async_url(self) -> str:
        return (
            f"mysql+asyncmy://{self.mysql_id}:{quote_plus(self.mysql_pw)}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
            f"?charset=utf8mb4"
        )

    def sync_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_id}:{quote_plus(self.mysql_pw)}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
            f"?charset=utf8mb4"
        )
