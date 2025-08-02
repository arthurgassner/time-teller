import csv
from dataclasses import dataclass
from datetime import datetime
import logging
from pathlib import Path
import random


@dataclass
class Quote:
    quote: str 
    author: str
    title: str 
    hhmm: str # Time in the hh:mm format

    @staticmethod
    def randomly_select_quote(dt: datetime) -> "Quote":

        # Figure out the current time
        hhmm = f"{dt.hour:02}:{dt.minute:02}"
        logging.debug(f"Selected time: {hhmm}")
        
        quote_filepath = Path(f"data/quotes/{hhmm}.csv")
        if not quote_filepath.is_file():
            return Quote(quote=f"Welp.\n It seems no quote exists for {hhmm}.", author="Someone", title="Some book", hhmm=hhmm)

        # Load the file containing the relevant quotes
        with quote_filepath.open(newline='') as f:
            reader = csv.reader(f)
            csv_rows = list(reader)

        # Randomly select one row
        selected_row_idx = random.randint(0, len(csv_rows)-1)
        selected_csv_row = ''.join(csv_rows[selected_row_idx])   
        
        _, quote, title, author = selected_csv_row.split('|')
        
        # Fix endlines
        quote = quote.replace('<br/>', '\n')
        
        return Quote(quote=quote, author=author, title=title, hhmm=hhmm)
