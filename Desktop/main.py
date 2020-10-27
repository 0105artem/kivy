#! python3
# "How Do You Feel?" app is an application made with kivy library wich asks
# to user "How do you feel?" and then returns a quote to cheer him up. It can
# also be installed on Android if you download the apk file from the apk folder.

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob, random
from datetime import datetime
from pathlib import Path


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "sign_up_screen"

    def login(self, uname, pword):
        print(uname, pword)
        with open("users.json") as file:
            users = json.load(file)
        
        if (uname in users) and (users[uname]['password'] == pword):
            self.manager.transition.direction = 'left'
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"

class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        users[uname] = {"username": uname, "password": pword, 
            "created": datetime.now().strftime("%Y-%m-%d %H-%M-%S")}
        
        with open("users.json", "w") as file:
            json.dump(users, file)

        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen_success"
    
    def back_to_login(self):
        self.manager.transition.direction = "left"
        self.manager.current = "login_screen"


class SignUpScreenSuccess(Screen):
    def login_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


    def get_quote(self, uinput):
        uinput = uinput.lower()

        files_lst = glob.glob("quotes/*txt")
        files_lst = [Path(filepath).stem for filepath in files_lst]

        if uinput == '':
            self.ids.quote.text = "Put some feeling."
        elif uinput in files_lst:
            with open(f"quotes/{uinput}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling."


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()