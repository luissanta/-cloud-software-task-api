from enum import Enum
from sqlalchemy import desc, asc


class OrderEnum(Enum):
    desc = desc
    asc = asc
