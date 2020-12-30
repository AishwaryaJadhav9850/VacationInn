import mongoengine as me
import datetime

class Owner(me.Document):
    registered_date=me.DateTimeField(default=datetime.datetime.now)
    name = me.StringField(required=True)
    email=me.StringField(required=True)

    guest_ids=me.ListField()
    room_ids=me.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'owner'
    }