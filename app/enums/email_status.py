from enum import Enum, unique

@unique
class EmailStatus(Enum):
    SENT = 'SENT'
    FAILED = 'FAILED'