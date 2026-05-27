import pytest
import os
import json
from datetime import date, timedelta, datetime
from unittest.mock import MagicMock, patch
from src.manager import ReservationManager
from src.reservation import Reservation
from src.exceptions import FacilityUnavailableError


class TestReservationManager:
    @pytest.fixture
    def manager(self):
        return ReservationManager()

    @pytest.fixture
    def mock_reservation(self):
        res = MagicMock()
        res.facility.id = "fac_123"
        res.start_date = datetime.now() + timedelta(days=1)
        res.end_date = datetime.now() + timedelta(days=5)
        return res

    def test_create_reservation_success(self, manager, mock_reservation):
        result = manager.create_reservation(mock_reservation)

        assert result is mock_reservation
        assert len(manager.reservations) == 1
        assert mock_reservation in manager.reservations

    def test_create_reservation_conflict(self, manager, mock_reservation):
        manager.create_reservation(mock_reservation)
        with pytest.raises(
            FacilityUnavailableError, match="Given time frame is already booked."
        ):
            manager.create_reservation(mock_reservation)

    @patch("builtins.open", new_callable=MagicMock)
    def test_save_to_json(self, mock_open, manager, mock_reservation):
        mock_reservation.id = "res_123"
        mock_reservation.user.id = "user_123"
        mock_reservation.facility.id = "fac_123"

        manager.create_reservation(mock_reservation)
        manager.save_to_json("dummy_path.json")

        mock_open.assert_called_once_with("dummy_path.json", "w", encoding="utf-8")

    def test_load_from_json_file_not_exists(self, manager):
        with patch("os.path.exists", return_value=False):
            result = manager.load_from_json("fake_path.json")
            assert result == []
