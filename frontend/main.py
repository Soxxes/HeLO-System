import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from database.db import DB
from src.calcs import calc_new_score
from kivy.uix.screenmanager import ScreenManager, Screen


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SuperUserLogIn(Widget):
    
    def switch_to_main(self, page_name):
        app.screen_manager.current = page_name


class MainWidget(Widget):
    superuser_disabled = BooleanProperty(True)
    helo_score_team1 = StringProperty("")
    helo_score_team2 = StringProperty("")
    db = DB("Marc", "jK5%oWq")
    
    def _get_scores(self, name1, name2):
        # make sure name1 is not empty
        if name1 != "":
            s1 = self.db.get_score(name1)
        else:
            s1 = None

        # make sure name2 is not empty
        if name2 != "":
            s2 = self.db.get_score(name2)
        else:
            s2 = None

        return s1, s2

    def set_scores_label(self, name1, name2):
        # get scores here
        s1, s2 = self._get_scores(name1, name2)
        self.helo_score_team1 = str(s1) # s1
        self.helo_score_team2 = str(s2) # s2

    def calc_and_send(self, name1, name2, auth, game_score):
        # get scores by names
        s1, s2 = self._get_scores(name1, name2)
        # make calcs with scores and game score
        new_score1, new_score2 = calc_new_score(s1, s2, game_score)
        # update db with auth and new score
        res = self.db.update_scores(name1, name2, auth, new_score1, new_score2)
        if res:
            # display new scores
            self.set_scores_label(name1, name2)
        else:
            # raise error, because update failed
            print("Auth failed")

    def on_switch_active(self, widget):
        if widget.active:
            self.superuser_disabled = False
        else:
            self.superuser_disabled = True

    def switch_to_superuser_page(self, page_name):
        app.screen_manager.current = page_name

    def __del__(self):
        # close connection to data base
        self.db.client.close()


# class HeLOApp(App):
#     def build(self):
#         return MainWidget()

class HeLOApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # main page
        self.main_page = MainWidget()
        screen = Screen(name="Main")
        screen.add_widget(self.main_page)
        self.screen_manager.add_widget(screen)

        # super user login
        self.superuser_page = SuperUserLogIn()
        screen = Screen(name="Superuser")
        screen.add_widget(self.superuser_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    app = HeLOApp()
    app.run()
