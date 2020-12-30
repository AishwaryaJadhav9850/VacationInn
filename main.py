import main_guest
import main_host
import data.mongo_setup as ms

def bye():
    exit()

if __name__ == '__main__':
    ms.global_init()
    try:
        while True:
            print("[B] - Do you want to [B]ook a Room")
            print('[O] - Do you want to [O]ffer a Room')
            print('[E] - [E]xit')
            argument = input().strip().lower()
            switcher = {
                'b': main_guest.main,
                'o': main_host.main,
                'e': bye
            }
            func = switcher.get(argument, lambda: "Invalid Input")
            func()
    except KeyboardInterrupt:
        print("Program Exit due to Exception")



