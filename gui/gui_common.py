from kivy.uix.label import Label
from kivy.uix.popup import Popup

def error_popup(text):
    return Popup(
        title="Error",
        content=Label(text=text),
        size_hint=(0.6, 0.4),
    )