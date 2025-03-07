from enum import Enum,unique

@unique
class ActiveStocks(Enum):
    ALPHABET = "GOOG"
    TSLA = "TSLA"
    MSFT = "MSFT"
    AMZN = "AMZN"
    NVIDIA = "NVDA"