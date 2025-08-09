from datetime import datetime
from zoneinfo import ZoneInfo

from utils.quote import Quote
from utils.settings import get_settings

def test_randomly_select_quote():
    """Ensure randomly selecting a quote/title/author works as expected."""

    # Given
    dt = datetime.now(tz=ZoneInfo("Europe/Zurich"))

    # When
    quote = Quote.randomly_select_quote(dt=dt)    

    # Then
    assert type(quote) is Quote
    assert quote.hhmm == f"{dt.hour:02}:{dt.minute:02}"

def test__get_missing_quote():
    """Ensure the missing quote fits what is expected by the settings."""

    # Given
    hhmm = "12:34"

    # When
    missing_quote = Quote._get_missing_quote(hhmm=hhmm)

    # Then
    assert type(missing_quote) is Quote
    assert hhmm == missing_quote.hhmm 
    assert hhmm in missing_quote.quote 
    assert missing_quote.author == get_settings().MISSING_AUTHOR
    assert missing_quote.title == get_settings().MISSING_TITLE