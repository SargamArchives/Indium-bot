from dataclasses import dataclass
from typing import List, MutableMapping

@dataclass
class CountryResponse:
    def __init__(self,
                capital: str,
                currencies: List[MutableMapping[str, str]],
                altSpellings: List[str],
                region: str,
                population: int,
                **kwargs):

        self.capital = capital
        self.currencies = currencies
        self.alt_spellings = altSpellings
        self.region = region
        self.population = population
        self.kwargs = kwargs
