from enum import Enum, auto
from typing import List, Optional
from dataclasses import dataclass
from datetime import date, datetime
import uuid

from src.common import PhoneNumber, Contact
from src.exceptions import IncorectRatingError
from src.config import app_logger as logger


class FacilityType(Enum):
    HOTEL = auto()
    MOTEL = auto()
    AIRBNB = auto()
    HOSTEL = auto()


@dataclass
class FacilityContact(Contact):
    website: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()

        if self.website is not None:
            if not self.website.startswith(("http://", "https://")):
                raise ValueError("Website URL mast beggin like: http:// or https://.")


@dataclass
class FacilityReview:
    username: str
    rating: int
    description: Optional[str] = None

    def __post_init__(self):
        self.id = str(uuid.uuid4())
        if not isinstance(self.rating, int):
            raise IncorectRatingError("Rating must be an integer")
        if self.rating < 1 or self.rating > 5:
            raise IncorectRatingError("The rating must be in range: [1, 5]")


@dataclass
class FacilityAddress:
    city: str
    street: str
    street_number: str
    post_code: str


class Facility:
    def __init__(
        self,
        name: str,
        facility_type: FacilityType,
        address: FacilityAddress,
        contact: FacilityContact,
        reviews: Optional[List[FacilityReview]] = None,
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.facility_type = facility_type
        self.address = address
        self.contact = contact
        self.reviews = reviews if reviews is not None else []
        logger.info(f"Facility '{self.name}' initiated successfully.")

    def add_review(self, review: FacilityReview) -> None:
        self.reviews.append(review)
        logger.info(f"Successfully added review. ID={review.id}")
