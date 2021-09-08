import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
import json
from functools import partial
from database.db import DB
from src.calcs import calc_new_score, calc_coop_scores
from kivy.uix.screenmanager import ScreenManager, Screen

# dependencies: kivy, pymongo

class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SuperUserWindow(Widget):
    
    def on_back_button(self):
        self.ids.back_home_button.source = "fig/home2_pressed.png"

    def switch_to_main(self, page_name):
        self.ids.back_home_button.source = "fig/home2.png"
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
    comp_factor = 1
    #confirm = False

    def _alert_popup(self, error):
        layout = BoxLayout(orientation="vertical")
        popup_label = Label(text=str(error), font_name="fonts/Eurostile.ttf",
                                halign="center", valign="middle")
        #popup_label.text_size = popup_label.size
        close_button = Button(text="Close", font_name="fonts/Eurostile.ttf",
                                halign="center", valign="middle",
                                size_hint=(0.4, 0.3),
                                pos_hint={"center_x": 0.5})
        close_button.text_size = close_button.size

        layout.add_widget(popup_label)
        layout.add_widget(close_button)

        popup = Popup(title="Alert Message", content=layout,
                        size_hint=(0.4, 0.4))
        popup.open()

        close_button.bind(on_press=popup.dismiss)

    # def confirm_popup(self, name1, name2, game_score, number_of_players):
    #     # set confirm to False
    #     self._set_confirm(False)
    #     layout = BoxLayout(orientation="vertical")
    #     popup_label1 = Label(text="Please confirm that this information is correct.",
    #                             font_name="fonts/Eurostile.ttf",
    #                             halign="center",
    #                             valign="middle")
    #     popup_label2 = Label(text=f"Your team: {name1}\n Opponent: {name2}\n"+
    #                             f"Played with {number_of_players} players\n"+
    #                             f"Score: {game_score}",
    #                             font_name="fonts/Eurostile.ttf",
    #                             halign="center",
    #                             valign="middle")
    #     confirm_button = Button(text="Confirm", font_name="fonts/Eurostile.ttf",
    #                             halign="center", valign="middle",
    #                             size_hint=(0.4, 0.4),
    #                             pos_hint={"center_x": 0.5})
    #     close_button = Button(text="No! It's not!", font_name="fonts/Eurostile.ttf",
    #                             halign="center", valign="middle",
    #                             size_hint=(0.4, 0.4),
    #                             pos_hint={"center_x": 0.5})
    #     #close_button.text_size = close_button.size

    #     layout.add_widget(popup_label1)
    #     layout.add_widget(popup_label2)
    #     layout2 = BoxLayout(orientation="horizontal")
    #     layout2.add_widget(confirm_button)
    #     layout2.add_widget(close_button)
    #     layout.add_widget(layout2)

    #     popup = Popup(title="Confirm", content=layout,
    #                     size_hint=(0.4, 0.4))
    #     popup.open()

    #     close_button.bind(on_press=popup.dismiss)
    #     confirm_button.bind(on_release=popup.dismiss)
    #     confirm_button.bind(on_press=self._set_confirm)
    
    # def _set_confirm(self, state=True):
    #     self.confirm = state

    def _get_scores(self, name1, name2):
        error = None
        # make sure name1 is not empty
        if name1 != "":
            s1, error = app.db.get_score(name1)
        else:
            s1 = None

        if error is not None:
            # display error to user
            self._alert_popup(error)

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

    def set_comp_factor(self, widget):
        if widget.text == "friendly match (off season)":
            self.comp_factor = 0.5
        elif widget.text == "friendly match (on season)":
            self.comp_factor = 0.8
        elif widget.text == "competitive match":
            self.comp_factor = 1
        elif widget.text == "competitive match (extra sweaty)":
            self.comp_factor = 1.2

    def calc_and_send(self, name1, name2, auth, game_score, checksum, n, coop):
        # check if names have been entered
        if name1 == "" or name2 == "":
            self._alert_popup("Please enter the names of the teams.")
            return
        if coop:
            self._calc_and_send_coop(name1, name2, auth, game_score, checksum, n)
            return
        # confirm information, if not confirmed return and don't send information to db
        # self._confirm_popup(name1, name2, game_score, n)
        # if not self.confirm: return
        # get scores by names
        s1, s2 = self._get_scores(name1, name2)
        # get number of games from data base
        number1, error = app.db.get_number_of_games(name1)
        if error is None:
            number2, error = app.db.get_number_of_games(name2)
        if error is None:
            # make calcs with scores and game score
            new_score1, new_score2, error = calc_new_score(s1, s2, game_score,
                                                    a1= 40 if number1 < 30 else 20,
                                                    a2= 40 if number2 < 30 else 20,
                                                    c=self.comp_factor,
                                                    number_of_players=n)
        if error is None:
            # update db with auth and new score
            # overwrite error variable in case there is one
            error = app.db.update(name1, name2, auth, new_score1, new_score2, int(checksum))
        if error is None:
            # display new scores
            self.set_scores_label(name1, name2)
        # route error through this else statement
        else:
            # raise error, because something failed
            # display error to user
            self._alert_popup(error)

    def _calc_and_send_coop(self, names1, names2, auth, game_score, checksums, n):
        # split list of names by ","
        names1, names2 = names1.split(","), names2.split(",")
        # remove whitespaces
        names1, names2 = list(map(lambda x: x.strip(), names1)), list(map(lambda x: x.strip(), names2))
        # get score for every team
        h1s = [self._get_scores(name, "")[0] for name in names1]
        h2s = [self._get_scores(name, "")[0] for name in names2]
        print(h1s, h2s)
        # calc the cooperations new scores
        h1s_new, h2s_new, error = calc_coop_scores(h1s, h2s, game_score,
                                                    c=self.comp_factor,
                                                    total_number_of_players=n)
        print(f"old scores: {h1s} and {h2s}, new scores: {h1s_new} and {h2s_new}")
        # split checksums and remove whitespaces
        checksums = checksums.split(",")
        checksums = list(map(lambda x: x.strip(), checksums))
        # check auth code of first team
        auth_checked= app.db.check_auth(names1[0], auth)
        # check checksum of the opponents
        checksums_checked = app.db.check_coop_checksums(names2, checksums)
        print("checked: ", auth_checked, checksums_checked)
        # update db
        if error is None and auth_checked and checksums_checked:
            zipped = list(zip(names1, h1s_new)) + list(zip(names2, h2s_new))
            for name, h_new in zipped:
                print("names lists: ", names1, names2)
                error = app.db.update_single(name, h_new,
                                            opponents=names2 if name in names1 else names1)
                if error is not None:
                    break
        if error is None:
            # display new scores
            self.set_scores_label(names1[0], names2[0])
        else:
            # raise error, because something failed
            # display error to user
            self._alert_popup(error)

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
    # username = "Public"
    # password = "6h2WPva5g"
    auth = ""
    # in case user changed the username in the config file
    with open("config.json", "r") as config:
        config_data = json.load(config)
        username = config_data["mongodb"]["username"]
        password = config_data["mongodb"]["password"]
        _cluster = config_data["mongodb"]["cluster"]
        _db = config_data["mongodb"]["db"]
        _collection = config_data["mongodb"]["collection"]
    db = DB(username, password, _cluster, _db, _collection)

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
        self.db = DB(username, password, self._cluster, self._db, self._collection)


if __name__ == "__main__":
    app = HeLOApp()
    app.run()
