import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from database.db import DB
from src.calcs import calc_new_score
from kivy.uix.screenmanager import ScreenManager, Screen


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SuperUserWindow(Widget):
    
    def switch_to_main(self, page_name):
        app.screen_manager.current = page_name

    def submit(self, username, password):
        # make sure TextInputs are not empty
        # if username or password is wrong, this error will be catched later
        if username != "" and password != "":
            app.change_db_user(username, password)
            app.main_page.ids["current_user"].text = username

    def get_checksum(self, label, auth):
        checksum = app.db.get_checksum(auth)
        label.text = str(checksum)


class MainWidget(Widget):
    superuser_disabled = BooleanProperty(True)
    helo_score_team1 = StringProperty("")
    helo_score_team2 = StringProperty("")

    def _alert_popup(self, error):
        layout = GridLayout(cols=1)
        popup_label = Label(text=str(error))
        close_button = Button(text="Close")

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title="Alert Message", content=layout)
        popup.open()

        close_button.bind(on_press=popup.dismiss)
    
    
    def _get_scores(self, name1, name2):
        error = None
        # make sure name1 is not empty
        if name1 != "":
            s1, error = app.db.get_score(name1)
        else:
            s1 = None

        # make sure name2 is not empty
        if name2 != "":
            s2, error = app.db.get_score(name2)
        else:
            s2 = None

        if error is not None:
            # display error to user
            self._alert_popup(error)

        return s1, s2

    def set_scores_label(self, name1, name2):
        # get scores here
        s1, s2 = self._get_scores(name1, name2)
        self.helo_score_team1 = str(s1) # s1
        self.helo_score_team2 = str(s2) # s2

    def calc_and_send(self, name1, name2, auth, game_score, checksum):
        # get scores by names
        s1, s2 = self._get_scores(name1, name2)
        # make calcs with scores and game score
        new_score1, new_score2 = calc_new_score(s1, s2, game_score)
        # update db with auth and new score
        error = app.db.update_scores(name1, name2, auth, new_score1, new_score2, int(checksum))
        if error is None:
            # display new scores
            self.set_scores_label(name1, name2)
        else:
            # raise error, because update failed
            print(error)
            # display error to user
            self._alert_popup(error)

    def on_switch_active(self, widget):
        if widget.active:
            self.superuser_disabled = False
            # # check if Superuser
            # self.db = DB(app.username, app.password)
        else:
            self.superuser_disabled = True

    def switch_to_superuser_page(self, page_name, auth):
        check = app.db.check_superuser(auth)
        if check is None:
            app.screen_manager.current = page_name
            app.auth = auth
        elif auth == "":
            self._alert_popup("Please enter an authentication code.")
        else:
            self._alert_popup(check)

    def __del__(self):
        # close connection to data base
        self.db.client.close()


# class HeLOApp(App):
#     def build(self):
#         return MainWidget()

class HeLOApp(App):
    username = "Public"
    password = "6h2WPva5g"
    auth = ""
    db = DB(username, password)

    def build(self):
        self.screen_manager = ScreenManager()

        # main page
        self.main_page = MainWidget()
        screen = Screen(name="Main")
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        # super user login
        self.superuser_page = SuperUserWindow()
        screen = Screen(name="Superuser")
        screen.add_widget(self.superuser_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def change_db_user(self, username, password):
        self.db = DB(username, password)


if __name__ == "__main__":
    app = HeLOApp()
    app.run()
