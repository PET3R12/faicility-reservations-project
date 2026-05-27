from __future__ import annotations

from datetime import time, date, datetime
import json
import uuid

from src.exceptions import InvalidReservationDateError, TooLongReservationError
from src.facility import Facility
from src.config import app_logger as logger


class Reservation:
    def __init__(
        self,
        user: User,
        facility: Facility,
        start_date: date,
        end_date: date,
    ):
        check_in_hour = time(14, 0)
        check_out_hour = time(11, 0)
        self.id = str(uuid.uuid4())
        self.user = user
        self.start_date = datetime.combine(start_date, check_in_hour)
        self.end_date = datetime.combine(end_date, check_out_hour)
        self.facility = facility

        if self.start_date >= self.end_date:
            raise InvalidReservationDateError(
                "Start date must be sooner than end date."
            )

        if self.start_date < datetime.now():
            raise InvalidReservationDateError("Cannot make reservation in past")
        if (self.end_date - self.start_date).days > 30:
            raise TooLongReservationError("Max duration of reservation is 30 days")

    @classmethod
    def to_json(self) -> json:
        data = {
            "id": self.id,
            "user": self.user,
            "facility": self.facility,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        return json.dump(data, ensure_ascii=False)
