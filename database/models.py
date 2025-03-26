from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderFSM:
    user_id: int
    user_name: str
    start: str = ""
    type_property: str = ""
    budget: int = 0
    district: str = ""
    specifications: str = ""
    custom_specification: str = ""
    contacts: str = ""
    present: str = ""
    name: str = ""

    created: datetime = datetime.now()  # Время создания заявки
    updated: datetime = datetime.now()  # Последнее обновление заявки
