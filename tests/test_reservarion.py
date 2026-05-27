import pytest
from datetime import date, timedelta, datetime
from unittest.mock import MagicMock
from src.reservation import Reservation
from src.exceptions import InvalidReservationDateError


class TestReservation:
    @pytest.fixture
    def mock_user(self):
        return MagicMock()

    @pytest.fixture
    def mock_facility(self):
        return MagicMock()

    def test_reservation_valid_dates(self, mock_user, mock_facility):
        start_date = date.today() + timedelta(days=2)
        end_date = date.today() + timedelta(days=5)

        res = Reservation(mock_user, mock_facility, start_date, end_date)

        assert res.start_date.hour == 14
        assert res.end_date.hour == 11
        assert res.start_date < res.end_date

    def test_reservation_end_before_start(self, mock_user, mock_facility):
        start_date = date.today() + timedelta(days=5)
        end_date = date.today() + timedelta(days=2)

        with pytest.raises(
            InvalidReservationDateError,
            match="Start date must be sooner than end date.",
        ):
            Reservation(mock_user, mock_facility, start_date, end_date)

    def test_reservation_in_past(self, mock_user, mock_facility):
        start_date = date.today() - timedelta(days=5)
        end_date = date.today() + timedelta(days=2)

        with pytest.raises(
            InvalidReservationDateError, match="Cannot make reservation in past"
        ):
            Reservation(mock_user, mock_facility, start_date, end_date)
