import Infrastructure.state as State
import Services.services as serv
from dateutil.parser import parse
import datetime

def main():
    print("\n***************** WELCOME GUEST *****************")
    try:
        show_menu()
        while True:

            argument = get_action()
            if argument=='m':
                return
            switcher = {
                'c': create_account,
                'l': login,
                'a': add_guest,
                'g': view_guest,
                'b': book_room,
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
    print('[L] - Login to your account')
    print("[A] - Add guests")
    print("[G] - View guests")
    print("[B] - Book room")
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

def add_guest():
    print("\n***************** ADD GUEST *****************")
    if not State.active_account:
        print("You must login first !")
        return
    name = input("Enter the name of the guest: ")
    age = int(input("Enter the age of the guest: "))
    no_of_guests = int(input("Enter no. of guest will accompany: "))
    is_family = input("Is it a family? ").strip().lower().startswith('y')

    guest=serv.add_guest(State.active_account,name,age,no_of_guests,is_family)
    State.active_account.reload()
    print(f"\nSUCCESS : New Guest has been added {guest.name}\n")


def view_guest():
    print("\n***************** VIEW GUEST *****************")
    if not State.active_account:
        print("You must login first !")
        return
    guest=serv.find_guest_provided_by_user(State.active_account)

    print(f"There are {len(guest)} guests provided by you {State.active_account.name} ")
    for i,r in enumerate(guest):
        print(f" {i+1}. Name: {r.name} \t Age:{r.age}")

def book_room():
    print("\n***************** BOOK A ROOM *****************")
    if not State.active_account:
        print("You must login first !")
        return

    guest=serv.find_guest_provided_by_user(State.active_account)
    if not guest:
        print("You must add guest !")
        return

    print("\n")
    location=input("Enter the location: ")
    checkin = parse(input("Enter the Check-in date [yyyy-mm-dd]: "))
    checkout=parse(input("Enter the Check-out date [yyyy-mm-dd]: "))
    print(checkin,checkout)
    if checkin>checkout:
        print("Check in date should be earlier to check out date!")
        return

    print(f"There are {len(guest)} guests provided by you {State.active_account.name} ")
    for i, r in enumerate(guest):
        print(f" {i + 1}. Name: {r.name} \t Age:{r.age}")
    gst=guest[int(input("Which guest do you want book room for: "))-1]

    room=serv.get_available_rooms(checkin,checkout,gst,location)
    if len(room)==0:
        print("Sorry, there are no rooms for the secltion criteria you entered!")
        return

    for i, r in enumerate(room):
        print(f" {i + 1}. Location: {r.location} \t Price:{r.price}")

    rm=room[int(input("Which room no. do you want to book?"))-1]
    serv.book_room(State.active_account,rm,gst,checkin,checkout)
    print(f"SUCCESS :  Room {rm} has been booked for {gst.name} in {r.location} at {r.price} ")

def view_booking():
    print("\n***************** VIEW BOOKINGS *****************")
    if not State.active_account:
        print("You must login first !")
        return
    serv.get_booking_for_user(State.active_account)


def bye():
    exit()