from datetime import datetime
from zoneinfo import ZoneInfo

from utils.quote import Quote

def test_randomly_select_quote():
    """Ensure randomly selecting a quote/title/author works as expected."""

    # Given
    dt = datetime.now(tz=ZoneInfo("Europe/Zurich"))

    # When
    quote = Quote.randomly_select_quote(dt=dt)    

    # Then
    assert type(quote) is Quote
    assert quote.hhmm == f"{dt.hour:02}:{dt.minute:02}"