from datetime import datetime
from zoneinfo import ZoneInfo

from utils.randomly_select_quote_title_author import randomly_select_quote_title_author

def test_randomly_select_quote_title_author():
    """Ensure randomly selecting a quote/title/author works as expected."""

    # Given
    dt = datetime.now(tz=ZoneInfo("Europe/Zurich"))

    # When
    quote, title, author = randomly_select_quote_title_author(dt=dt)    

    # Then
    # TODO complete
    
