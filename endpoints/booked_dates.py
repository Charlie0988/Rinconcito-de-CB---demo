from silence.decorators import endpoint

@endpoint(
    route="/booked-dates",
    method="GET",
    sql="SELECT start_date, end_date FROM booked_dates",
    description="Fechas reservadas según Booking.com"
)
def get_booked_dates():
    pass