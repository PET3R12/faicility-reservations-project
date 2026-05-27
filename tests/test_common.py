import pytest
from src.common import PhoneNumber, Contact


class TestPhoneNumber:
    @pytest.mark.parametrize(
        "area_code, number",
        [
            (48, "123456789"),
            (1, "9876543210"),
            (44, "111222333"),
            (49, "111222"),
            (33, "999999999"),
            (420, "123123123"),
            (999, "000000000000"),
            (7, "12345"),
            (358, "0401234567"),
            (81, "9012345678"),
            (380, "501234567"),
            (93, "701234567"),
        ],
    )
    def test_phone_number_valid(self, area_code, number):
        phone = PhoneNumber(area_code, number)
        assert phone.area_code == area_code
        assert phone.number == number
        assert isinstance(phone, PhoneNumber)

    @pytest.mark.parametrize(
        "area_code, number, expected_error_msg",
        [
            (0, "123456789", "Area code must be positive"),
            (-48, "123456789", "Area code must be positive"),
            (-1, "123456789", "Area code must be positive"),
            (-999, "000", "Area code must be positive"),
            (48, "12345a678", "Phone number can contain numbers only."),
            (48, "number", "Phone number can contain numbers only."),
            (48, "12 34 56", "Phone number can contain numbers only."),
            (48, "123-456", "Phone number can contain numbers only."),
            (48, "+48123456", "Phone number can contain numbers only."),
            (48, "", "Phone number can contain numbers only."),
        ],
    )
    def test_phone_number_invalid(self, area_code, number, expected_error_msg):
        with pytest.raises(ValueError) as exc_info:
            PhoneNumber(area_code, number)
        assert str(exc_info.value) == expected_error_msg


class TestContact:
    @pytest.mark.parametrize(
        "email", ["test@example.com", "user.name@domain.co.uk", "admin@localhost.net"]
    )
    def test_contact_valid_email_only(self, email):
        contact = Contact(email=email)
        assert contact.email == email
        assert contact.phone is None

    @pytest.mark.parametrize(
        "email", ["testexample.com", "test@examplecom", "userexample", ""]
    )
    def test_contact_invalid_email(self, email):
        with pytest.raises(ValueError, match="Incorrect e-mail format"):
            Contact(email=email)

    def test_contact_with_phone(self):
        phone = PhoneNumber(48, "111222333")
        contact = Contact(email="test@domain.com", phone=phone)
        assert contact.phone is not None
        assert contact.phone.number == "111222333"
        assert contact.email in "Moje emaile: test@domain.com"
