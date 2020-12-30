import Infrastructure.state as State
import Services.services as serv
from dateutil.parser import parse
import datetime

def main():
    print("\n***************** WELCOME HOST *****************")
    try:
        show_menu()
        while True:

            argument = get_action()
            if argument=='m':
                return
            switcher = {
                'c': create_account,
                'a': login,
                'l': list_your_rooms,
                'r': register_room,
                'u': update_availability,
                'v': view_booking,
                'e': bye
            }
            func = switcher.get(argument, lambda: "Invalid Input")
            func()
    except KeyboardInterrupt:
        print("Program Exit due to Exception")

def get_action():
    text = '> '
    if State.active_account:
        text = f'{State.active_account.name}> '

    action = input(text)
    return action.strip().lower()

def show_menu():
    print()
    print("What action would toy like to perform:")
    print("[C] - Create account")
    print('[A] - Login to your account')
    print("[L] - List your rooms")
    print("[R] - Register your room")
    print("[U] - Update room availability")
    print("[V] - View bookings")
    print("[M] - Change mode (Guest or Host)")
    print('[E] - [E]xit App')

def create_account():
    print("\n***************** REGISTER *****************")
    name=input("Enter your name: ")
    email=input("Enter your email id: ").strip().lower()
    old_account=serv.find_account_by_email(email)

    if old_account:
        print(f"\nERROR : Account with emial {email} already exists with ID {old_account.id}!\n")
        return

    State.active_account=serv.create_account(name,email)
    print(f"\nSUCCESS : New Account created with ID {State.active_account.id}\n")

def login():
    print("\n***************** LOGIN *****************")
    name = input("Enter your name: ")
    email = input("Enter your email id: ").strip().lower()
    acnt = serv.find_account_by_email(email)
    if not acnt:
        print("\nAccount doesnt exits, kindly create a new account!")
        return
    State.active_account=acnt
    print(f"\nSUCCESS : Welcome {State.active_account.name}")

def list_your_rooms():
    print("***************** LIST OF ROOMS *****************")
    if not State.active_account:
        print("You must login first !")
        return
    room= serv.find_room_provided_by_user(State.active_account)
    print(f"There are {len(room)} room provided by the Owner {State.active_account.name} ")
    for i,r in enumerate(room):
        print(f" {i+1}. Location: {r.location} \t Name:{r.name}")
        for b in r.bookings:
            print("\t * Booking {} {} days, booked? {}".format(b.check_in_date,
                                                          (b.check_out_date-b.check_in_date).days,
                                                          "Yes" if b.booked_date is not None else 'No'))



def register_room():
    print("\n***************** REGISTER YOUR ROOM *****************")
    if not State.active_account:
        print("You must login first !")
        return
    location = input("Enter the location of the room: ")
    name = input("Enter the name of the Room/Hotel/Villa: ")
    price = float(input("Enter the price per night of the room: "))
    no_of_rooms = int(input("Enter the number of the room in the Hotel/Villa: "))
    is_AC = input("Does the room have Air Conditioning [Y,N]: ").strip().lower().startswith('y')
    no_of_guests=int(input("Enter the number of the guests that can accomodate in the room: "))

    room=serv.register_room(State.active_account,location,name,price,no_of_rooms,is_AC,no_of_guests)

    State.active_account.reload()

    print(f"\nSUCCESS : New room has been added with ID {room.id}\n")

def update_availability():
    print("\n***************** UPDATE ROOM AVAILABILITY *****************")
    if not State.active_account:
        print("You must login first !")
        return
    list_your_rooms()
    try:
        no=int(input("Enter the room no. that you want to make available"))
    except ValueError:
        print("Room no. entered is Incorrect !!")
    l=serv.find_room_provided_by_user(State.active_account)
    room=l[no-1]
    print(f"\nYou have select {room.name} to make available")
    start_date=parse(input("Enter the start date of room availability [yyyy-mm-dd]: "))
    days=int(input("Enter no. of days of room availability:"))
    end_date=start_date+datetime.timedelta(days=days)
    room=serv.add_available_dates(start_date,end_date,room)
    State.active_account.reload()
    print(f"\nSUCCESS : Room {room.name} has been made availble {days} days")
    list_your_rooms()

def view_booking():
    print("\n***************** VIEW BOOKINGS *****************")
    if not State.active_account:
        print("You must login first !")
        return
    serv.get_booking_for_user(State.active_account)

def bye():
    exit()