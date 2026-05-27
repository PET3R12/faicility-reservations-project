from dataclasses import dataclass
from typing import Optional


@dataclass
class PhoneNumber:
    area_code: int
    number: str

    def __post_init__(self):
        if self.area_code <= 0:
            raise ValueError("Area code must be positive")
        if not self.number.isdigit():
            raise ValueError("Phone number can contain numbers only.")


@dataclass
class Contact:

    email: str
    phone: Optional[PhoneNumber] = None

    def __post_init__(self):
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Incorrect e-mail format")
