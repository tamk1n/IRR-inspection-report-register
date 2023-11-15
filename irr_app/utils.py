from enum import Enum

class IRType(Enum):
    negative = 'Negative'
    positive = 'Positive'

class IRStatus(Enum):
    open = 'Open'
    close = 'Close'
    overdue = 'Overdue'