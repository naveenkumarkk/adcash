# app/domain/enums.py
from enum import Enum

class PayoutType(str, Enum):
    CPA = "CPA"
    FIXED = "FIXED"
    CPA_FIXED = "CPA_FIXED"
    CUSTOM= "CUSTOM"
