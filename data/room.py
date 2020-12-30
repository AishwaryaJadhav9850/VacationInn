import datetime
import mongoengine as me
from data.booking import Booking

class Room(me.Document):
    registered_date=me.DateTimeField(default=datetime.datetime.now)
    location=me.StringField(required=True)
    name=me.StringField(required=True)
    price=me.FloatField(required=True)
    no_of_rooms=me.IntField(required=True)
    is_AC=me.BooleanField(default=False,required=True)
    no_of_guests=me.IntField(required=True)

    bookings=me.EmbeddedDocumentListField(Booking)

    meta = {
        'db_alias': 'core',
        'collection': 'room'
    }