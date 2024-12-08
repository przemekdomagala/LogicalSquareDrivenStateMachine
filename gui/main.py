from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from language_selection_screen import LanguageSelectionScreen
from square_screen import SquareScreen

Window.clearcolor = (0.1, 0.1, 0.2, 1)

#TODO: Extract states from GUI
#TODO: Code generation of state machine, with states but without transitions for the time being

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LanguageSelectionScreen(name="language_selection"))
        sm.add_widget(SquareScreen(name="square_screen"))
        return sm

if __name__ == "__main__":
    MainApp().run()
