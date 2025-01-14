from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from language_selection_screen import LanguageSelectionScreen
from square_screen import SquareScreen

Window.clearcolor = (0.1, 0.1, 0.2, 1)

class MainApp(App):
    def build(self):
        self.title = "State Machine Generator"
        sm = ScreenManager()
        sm.add_widget(LanguageSelectionScreen(name="language_selection"))
        sm.add_widget(SquareScreen(name="square_screen"))
        return sm

if __name__ == "__main__":
    MainApp().run()
