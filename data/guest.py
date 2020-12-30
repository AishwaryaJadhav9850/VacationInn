import datetime
import mongoengine as me
class Guest(me.Document):
    registered_date=me.DateTimeField(default=datetime.datetime.now)
    name=me.StringField(required=True)
    age=me.IntField(required=True)
    no_of_guests=me.IntField(required=True)
    is_family=me.BooleanField(required=True,default=False)

    meta={
        'db_alias':'core',
        'collection':'guest'
    }
