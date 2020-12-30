from data.owner import Owner
from data.room import Room
from data.booking import Booking
from data.guest import Guest

import datetime
import parser
import mongoengine

def find_account_by_email(email:str)-> Owner:
    owner = Owner.objects().filter(email=email).first()
    return owner

def create_account(name:str,email:str)->Owner:
    owner=Owner()
    owner.name=name
    owner.email=email
    owner.save()
    return owner

def add_guest(active_account:Owner,name:str,age:int,no_of_guests:int,is_family:bool) -> Guest:
    guest=Guest()
    guest.name=name
    guest.age=age
    guest.no_of_guests=no_of_guests
    guest.is_family=is_family
    guest.save()

    acnt=find_account_by_email(active_account.email)
    acnt.guest_ids.append(guest.id)
    acnt.save()
    return guest

def register_room(active_account:Owner, location:str,name:str,price:float,
                  no_of_rooms:int,is_AC:bool,no_of_guests:int)-> Room:
    room=Room()
    room.location = location
    room.name = name
    room.price = price
    room.no_of_rooms = no_of_rooms
    room.is_AC = is_AC
    room.no_of_guests=no_of_guests
    room.save()
    acnt=find_account_by_email(active_account.email)
    acnt.room_ids.append(room.id)
    acnt.save()
    return room


def find_room_provided_by_user(account: Owner) -> list[Room]:
    query=Room.objects(id__in=account.room_ids)
    return list(query)


def find_guest_provided_by_user(active_account:Owner) -> list[Guest]:
    query=Guest.objects(id__in=active_account.guest_ids)
    return list(query)

def add_available_dates(start_date:datetime,end_date:datetime,room:Room) -> Room:
    booking=Booking()
    booking.check_in_date =start_date
    booking.check_out_date = end_date
    room=Room.objects(id=room.id).first()
    room.bookings.append(booking)
    room.save()
    return room

def get_available_rooms(checkin:datetime,checkout:datetime,gst:Guest,location:str) -> list[Room]:
    query = Room.objects() \
        .filter(location__gte=location) \
        .filter(bookings__check_in_date__lte=checkin) \
        .filter(bookings__check_out_date__gte=checkout)
    rooms = query.order_by('price', '-no_of_guests')
    final_room=[]
    for r in rooms:
        for b in r.bookings:
            if b.check_in_date <= checkin and b.check_out_date >= checkout and b.guest_guest_id is None:
                final_room.append(r)
    return final_room

def book_room(acnt:Owner,rm:Room,gst:Guest,checkin:datetime,checkout:datetime):
    booking: Optional[Booking] = None

    for b in rm.bookings:
        if b.check_in_date <= checkin and b.check_out_date >= checkout and b.guest_guest_id is None:
            booking=b
            break
    booking.guest_guest_id=acnt.id
    booking.guest_guest_id=gst.id
    booking.check_in_date=checkin
    booking.check_out_date=checkout
    booking.booked_date=datetime.datetime.now()
    rm.save()
    return


def get_booking_for_user(active_account:Owner):
    acnt=find_account_by_email(active_account.email)
    print("Below are all the GUEST IDS: - ")
    booked_rooms=[]

    for r in Room.objects:
        for b in r.bookings:
            for a in acnt.guest_ids:
                if b.guest_guest_id==a:
                    guest_1=Guest.objects().filter(id=a).first()
                    print(f"\t * Guest {guest_1.name} has been booked at {r.location} from {b.check_in_date} to {b.check_out_date} for {(b.check_out_date-b.check_in_date)}. ")
    return

