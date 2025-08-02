from dataclasses import dataclass


@dataclass
class Quote:
    quote: str 
    author: str
    title: str 
    hhmm: str # Time in the hh:mm format