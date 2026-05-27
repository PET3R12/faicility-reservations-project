import pytest
from src.facility import (
    FacilityContact,
    FacilityReview,
    FacilityAddress,
    Facility,
    FacilityType,
)
from src.exceptions import IncorectRatingError


class TestFacilityContact:
    @pytest.mark.parametrize(
        "website",
        [
            "http://example.com",
            "https://secure-domain.pl",
            None,
            "https://www.hotel.com.pl",
            "http://sub.domain.org/path",
            "https://hotel-warszawa.pl",
            "http://192.168.1.1",
        ],
    )
    def test_facility_contact_valid_website(self, website):
        contact = FacilityContact(email="hotel@hotel.com", website=website)
        assert contact.website == website

    @pytest.mark.parametrize(
        "website",
        [
            "www.example.com",
            "ftp://files.com",
            "example.com",
            "htt://literowka.pl",
            "https//brak-dwukropka.com",
            "://sam-ukosnik.pl",
            "ws://websocket.com",
        ],
    )
    def test_facility_contact_invalid_website(self, website):
        with pytest.raises(
            ValueError, match=r"Website URL mast beggin like: http:// or https://\."
        ):
            FacilityContact(email="hotel@hotel.com", website=website)


class TestFacilityReview:
    @pytest.mark.parametrize("rating", [1, 2, 3, 4, 5])
    def test_review_valid_rating(self, rating):
        review = FacilityReview(username="user1", rating=rating, description="Ok")
        assert review.rating == rating
        assert len(review.id) > 0

    @pytest.mark.parametrize("rating", [0, 6, -1, 100])
    def test_review_invalid_rating_bounds(self, rating):
        with pytest.raises(
            IncorectRatingError, match=r"The rating must be in range: \[1, 5\]"
        ):
            FacilityReview(username="user1", rating=rating)

    @pytest.mark.parametrize("rating", [4.5, "5", None])
    def test_review_invalid_rating_type(self, rating):
        with pytest.raises(IncorectRatingError, match="Rating must be an integer"):
            FacilityReview(username="user1", rating=rating)


class TestFacility:
    @pytest.fixture
    def sample_facility(self):
        address = FacilityAddress("Warszawa", "Marszałkowska", "1", "00-001")
        contact = FacilityContact("kontakt@hotel.pl")
        return Facility("Grand Hotel", FacilityType.HOTEL, address, contact)

    def test_facility_initialization(self, sample_facility):
        assert sample_facility.name == "Grand Hotel"
        assert sample_facility.facility_type == FacilityType.HOTEL
        assert isinstance(sample_facility.reviews, list)
        assert len(sample_facility.reviews) == 0

    def test_add_review(self, sample_facility):
        review = FacilityReview("user", 5, "Super!")
        sample_facility.add_review(review)

        assert len(sample_facility.reviews) == 1
        assert sample_facility.reviews[0] is review
        assert sample_facility.reviews[0].rating > 4
