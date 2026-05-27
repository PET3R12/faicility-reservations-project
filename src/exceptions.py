class InvalidReservationDateError(Exception):
    pass


class FacilityUnavailableError(Exception):
    pass


class PastDateError(Exception):
    pass


class InvalidContactInfoError(Exception):
    pass


class InvalidReviewRatingError(Exception):
    pass


class IncorectRatingError(Exception):
    pass


class TooLongReservationError(Exception):
    pass
