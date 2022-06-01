import os
from instaloader import Instaloader, TwoFactorAuthRequiredException
S = "0"
STATUS = set(int(x) for x in (S).split())
L = Instaloader()



def generate():
    print("Now Enter your Instagram username")
    id = input()
    print("Enter Your Instagram Password")
    pwd = input()
    try:
        L.login(id, pwd)
        L.save_session_to_file(filename=f"./{id}")
        usersavelocal(id)
        STATUS.add(1)
    except TwoFactorAuthRequiredException:
        print(
            "Your account has Two Factor authentication Enabled.\nNow Enter the code recived on your mobile."
        )
        code = input()
        L.two_factor_login(code)
        L.save_session_to_file(filename=f"./{id}")
        usersavelocal(id)
        STATUS.add(1)
    except Exception as e:
        print(e)
        return
    print("Succesfully Logged into Instagram")
def usersavelocal(username):
    file = open("username.txt","w")
    if os.path.isfile("username.txt"):
        with open("username.txt") as f:
            file.write(username)
            file.close()
generate()