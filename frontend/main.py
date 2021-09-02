import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from database.db import DB


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainWidget(Widget):
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
        # make calcs with scores and game score
        new_score1 = 777
        # update db with auth and new score
        res = self.db.update(name1, auth, new_score1)
        if res:
            # display new scores
            self.set_scores_label(name1, name2)
        else:
            # raise error, because update failed
            print("Auth failed")

    def __del__(self):
        # close connection to data base
        self.db.client.close()


class HeLOApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    app = HeLOApp()
    app.run()
