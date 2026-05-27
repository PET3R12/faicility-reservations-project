from __future__ import annotations

from datetime import date, datetime
import uuid
from typing import Optional

from src.manager import ReservationManager
from src.common import PhoneNumber, Contact
from src.facility import Facility, FacilityReview
from src.reservation import Reservation
from src.config import app_logger as logger

from src.exceptions import (
    IncorectRatingError,
    InvalidReservationDateError,
    FacilityUnavailableError,
)


class User:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        username: str,
        contact: Contact,
    ):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.contact = contact
        logger.info(f"User '{self.username}' created successfully.")

    def make_reservation(
        self,
        facility: Facility,
        start_date: date,
        end_date: date,
        manager: "ReservationManager",
    ) -> Reservation | None:
        try:
            reservation = Reservation(
                user=self, facility=facility, start_date=start_date, end_date=end_date
            )
            manager.create_reservation(reservation)
            return reservation
        except (InvalidReservationDateError, FacilityUnavailableError) as e:
            logger.error(f"Unable to create reservation for '{self.username}': {e}")
            return None

    def add_review(
        self, facility: Facility, rating: int, description: Optional[str]
    ) -> FacilityReview | None:
        try:
            review = FacilityReview(
                username=self.username, rating=rating, description=description
            )
            return review
        except IncorectRatingError as e:
            logger.error(f"Unable to add review: {e}")
            return None
