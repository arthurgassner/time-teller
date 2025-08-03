from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ROOT_FOLDERPATH : Path = Path(__file__).resolve().parent.parent
    LAST_FULL_REFRESH_DT_FILEPATH = ROOT_FOLDERPATH / ".last_full_refresh_dt"
    FONT_FILEPATH = ROOT_FOLDERPATH / "data" / "fonts" / "CormorantGaramond-VariableFont_wght.ttf"
    ITALIC_FONT_FILEPATH = ROOT_FOLDERPATH / "data" / "fonts" / "CormorantGaramond-Italic-VariableFont_wght.ttf"
    TZ: ZoneInfo = ZoneInfo("Europe/Zurich")


@lru_cache
def get_settings() -> Settings:
    return Settings()