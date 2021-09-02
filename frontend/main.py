import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainWidget(Widget):
    helo_score_team1 = StringProperty("")
    helo_score_team2 = StringProperty("")
    
    def _get_scores(self, name1, name2):
        # get HeLO scores here
        pass

    def set_scores_label(self, name1, name2):
        # get scores here
        # s1, s2 = self._get_scores(name1, name2)
        self.helo_score_team1 = "521" # s1
        self.helo_score_team2 = "125" # s2

    def calc_and_send(self, name1, name2, auth):
        # get scores here
        pass


class HeLOApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    app = HeLOApp()
    app.run()
