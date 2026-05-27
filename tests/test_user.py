import pytest
from unittest.mock import MagicMock
from datetime import date, timedelta

from src.user import User
from src.common import Contact, PhoneNumber
from src.exceptions import FacilityUnavailableError
from src.facility import FacilityReview


class TestUser:

    @pytest.fixture
    def contact(self):
        return Contact(email="test@mail.com", phone=PhoneNumber(48, "123456789"))

    @pytest.fixture
    def mock_manager(self):

        return MagicMock()

    @pytest.fixture
    def mock_facility(self):

        return MagicMock()

    @pytest.mark.parametrize(
        "first_name, last_name, username",
        [
            ("Jan", "Kowalski", "jankowalski"),
            ("Anna", "Nowak", "annanowak"),
            ("X", "Y", "xy_user"),
            ("Jan-Krzysztof", "Kowalski-Nowak", "j_k_nowak"),
            ("BardzoDlugieImie", "BardzoDlugieNazwisko", "dlugi_nick_12345"),
            ("O'Connor", "Smith", "irish_name"),
            ("Zażółć", "Gęślą", "polskie_znaki"),
            (" John ", " Doe ", "spacje"),
            ("Maria", "Skłodowska-Curie", "m_s_c_1867"),
            ("Kamil", "Ślimak", "kslimak_99"),
        ],
    )
    def test_user_initialization(self, contact, first_name, last_name, username):
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            contact=contact,
        )

        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.username == username
        assert user.contact is contact
        assert isinstance(user.id, str)
        assert len(user.id) > 0

    @pytest.mark.parametrize(
        "days_start, days_end",
        [
            (1, 4),
            (10, 11),
            (30, 44),
            (2, 5),
            (50, 75),
            (1, 30),
            (7, 14),
            (100, 105),
        ],
    )
    def test_make_reservation_success(
        self, contact, mock_facility, mock_manager, days_start, days_end
    ):
        user = User(first_name="Jan", last_name="K", username="jan", contact=contact)
        start = date.today() + timedelta(days=days_start)
        end = date.today() + timedelta(days=days_end)

        reservation = user.make_reservation(mock_facility, start, end, mock_manager)

        assert reservation is not None
        assert reservation.user is user
        mock_manager.create_reservation.assert_called_once_with(reservation)

    @pytest.mark.parametrize(
        "error_message", ["Termin zajęty!", "Obiekt zamknięty", "Brak pokoi"]
    )
    def test_make_reservation_manager_raises_error(
        self, contact, mock_facility, mock_manager, error_message
    ):
        user = User(first_name="Jan", last_name="K", username="jan", contact=contact)

        mock_manager.create_reservation.side_effect = FacilityUnavailableError(
            error_message
        )

        start = date.today() + timedelta(days=1)
        end = date.today() + timedelta(days=4)

        result = user.make_reservation(mock_facility, start, end, mock_manager)

        assert result is None

    @pytest.mark.parametrize(
        "rating, description, should_succeed",
        [
            (5, "Super pobyt!", True),
            (1, "Tragedia", True),
            (3, None, True),
            (4, "Dobrze, ale ", True),
            (2, "Mogło być lepiej", True),
            (0, "Zbyt mało", False),
            (6, "Zbyt dużo", False),
            (-1, "Ujemna", False),
            (-100, "Bardzo ujemna", False),
            (1000, "Bardzo duża", False),
            ("5", "Zły typ (str)", False),
            (4.5, "Zły typ (float)", False),
            (3.14, "Pi", False),
            (None, "Brak oceny", False),
            ([5], "Lista", False),
        ],
    )
    def test_user_add_review(
        self, contact, mock_facility, rating, description, should_succeed
    ):
        user = User(first_name="Jan", last_name="K", username="jan", contact=contact)
        result = user.add_review(mock_facility, rating, description)

        if should_succeed:
            assert result is not None
            assert isinstance(result, FacilityReview)
            assert result.rating == rating
            assert result.description == description
            assert result.username == user.username
        else:
            assert result is None
