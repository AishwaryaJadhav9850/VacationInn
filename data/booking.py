import mongoengine as me
import datetime

class Booking(me.EmbeddedDocument):
    guest_owner_id=me.ObjectIdField()
    guest_guest_id=me.ObjectIdField()

    booked_date=me.DateTimeField()
    check_in_date=me.DateTimeField(required=True)
    check_out_date=me.DateTimeField(required=True)

    review=me.StringField()
    rating=me.FloatField(default=0)