from datetime import datetime, time, timedelta
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ROOT_FOLDERPATH : Path = Path(__file__).resolve().parent.parent
    FONT_FILEPATH: Path = ROOT_FOLDERPATH / "data" / "fonts" / "CormorantGaramond-VariableFont_wght.ttf"
    ITALIC_FONT_FILEPATH: Path = ROOT_FOLDERPATH / "data" / "fonts" / "CormorantGaramond-Italic-VariableFont_wght.ttf"
    QUOTE_MAX_WIDTH_RATIO: float = 0.8 # Max screen width proportion ([0;1]) within which the written quote sits
    QUOTE_MAX_HEIGHT_RATIO: float = 0.6 # Max screen height proportion ([0;1]) within which the written quote sits

    # Full-refresh-related settings
    TZ: ZoneInfo = ZoneInfo("Europe/Zurich")
    DEFAULT_LAST_FULL_REFRESH_DT: datetime = datetime(year=1900, month=1, day=1, hour=2, minute=0).replace(tzinfo=TZ)
    LAST_FULL_REFRESH_DT_FILEPATH: Path = ROOT_FOLDERPATH / ".last_full_refresh_dt"
    # Time (HH:MM:SS) after which a full-refresh is triggered, if none have been done today (dd.mm.yyyy)
    FULL_REFRESH_TRIGGER_TIME: time = time(hour=2, minute=0) 
    # Max timedelta after which a full-refresh is triggered
    FULL_REFRESH_MAX_TIMEDELTA: timedelta = timedelta(hours=24)
    
    # Missing-quote-related settings
    MISSING_QUOTE: str = "Welp.\n It seems no quote exists for <b><HHMM></b>."
    MISSING_AUTHOR: str = "Someone"
    MISSING_TITLE: str = "Some book"

    @property
    def LAST_FULL_REFRESH_DT(self) -> datetime:
        """Return the datetime of the last full refresh, 
        defaulting to DEFAULT_LAST_FULL_REFRESH_DT if none was ever done.
        """

        last_full_refresh_dt = self.DEFAULT_LAST_FULL_REFRESH_DT
        if self.LAST_FULL_REFRESH_DT_FILEPATH.is_file():
            last_full_refresh_dt_str = self.LAST_FULL_REFRESH_DT_FILEPATH.read_text()
            last_full_refresh_dt = datetime.fromisoformat(last_full_refresh_dt_str.strip('\n')).replace(tzinfo=self.TZ)

        return last_full_refresh_dt
    
@lru_cache
def get_settings() -> Settings:
    return Settings()