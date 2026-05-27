import json
import os
from datetime import datetime
from typing import List

from src.facility import Facility
from src.reservation import Reservation
from src.exceptions import FacilityUnavailableError
from src.config import app_logger as logger


class ReservationManager:
    def __init__(self):
        self.reservations: List[Reservation] = []

    def is_facility_available(
        self, facility: Facility, start_date: datetime, end_date: datetime
    ) -> bool:

        for res in self.reservations:
            if res.facility.id == facility.id:
                if start_date < res.end_date and end_date > res.start_date:
                    return False
        return True

    def create_reservation(self, reservation: Reservation) -> Reservation | None:
        if not self.is_facility_available(
            reservation.facility, reservation.start_date, reservation.end_date
        ):
            logger.warning(
                f"Facility {reservation.facility.name} is already booked at in given time frame."
            )
            raise FacilityUnavailableError("Given time frame is already booked.")

        self.reservations.append(reservation)
        logger.info(f"Reservation {reservation.id} added successfully.")
        return reservation

    def save_to_json(self, filepath: str = "reservations.json"):
        data_to_save = []
        for res in self.reservations:
            data_to_save.append(
                {
                    "id": res.id,
                    "user_id": res.user.id,
                    "facility_id": res.facility.id,
                    "start_date": res.start_date.isoformat(),
                    "end_date": res.end_date.isoformat(),
                }
            )

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        logger.info(f"Saved {len(self.reservations)} reservations to '{filepath}'.")

    def load_from_json(self, filepath: str = "reservations.json"):
        if not os.path.exists(filepath):
            logger.warning(f"File {filepath} does not exist.")
            return []

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.info(f"Loaded {len(data)} past reservations from JSON.")
        return data
