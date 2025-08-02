from datetime import datetime
from zoneinfo import ZoneInfo

from utils.randomly_select_quote import randomly_select_quote

def test_randomly_select_quote():
    """Ensure randomly selecting a quote/title/author works as expected."""

    # Given
    dt = datetime.now(tz=ZoneInfo("Europe/Zurich"))

    # When
    quote, title, author = randomly_select_quote(dt=dt)    

    # Then
    # TODO complete
    
