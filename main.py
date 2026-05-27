from datetime import date, timedelta

from src.common import PhoneNumber, Contact
from src.facility import Facility, FacilityType, FacilityAddress, FacilityContact
from src.user import User
from src.manager import ReservationManager

def main():
    manager = ReservationManager()
    manager.load_from_json("data_reservations.json")
    address = FacilityAddress(city="Warszawa", street="Marszałkowska", street_number="1", post_code="00-001")
    fac_contact = FacilityContact(email="rezerwacje@grandhotel.pl", website="https://www.grandhotel.pl")
    
    hotel = Facility(
        name="Grand Hotel", 
        facility_type=FacilityType.HOTEL, 
        address=address, 
        contact=fac_contact
    )
    user_phone = PhoneNumber(area_code=48, number="123456789")
    user_contact = Contact(email="jan.kowalski@example.com", phone=user_phone)
    
    user = User(
        first_name="Jan", 
        last_name="Kowalski", 
        username="jankowalski", 
        contact=user_contact
    )
    start_date = date.today() + timedelta(days=15)
    end_date = date.today() + timedelta(days=20)
    reservation1 = user.make_reservation(hotel, start_date, end_date, manager)
    reservation2 = user.make_reservation(hotel, start_date, end_date, manager)
    
    if not reservation2:
        pass

    review = user.add_review(hotel, rating=5, description="Spoko hotel")
    if review:
        hotel.add_review(review)

    manager.save_to_json("data_reservations.json")


if __name__ == "__main__":
    main()