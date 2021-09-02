import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainWidget(Widget):
    pass


class HeLOApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    app = HeLOApp()
    app.run()
