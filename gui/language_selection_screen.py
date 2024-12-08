from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup

class LanguageSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(LanguageSelectionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        label = Label(
            text="Wybierz język:",
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
        )
        layout.add_widget(label)

        self.dropdown = DropDown()

        for lang in ["Python"]:
            btn = Button(
                text=lang, size_hint_y=None, height=50, background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.language_button = Button(
            text="Wybierz...",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
        )
        self.language_button.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=self.update_button_text)

        layout.add_widget(self.language_button)

        next_button = Button(
            text="Dalej",
            size_hint=(1, 0.2),
            background_color=(0.4, 0.8, 0.2, 1),
            color=(1, 1, 1, 1),
        )
        next_button.bind(on_release=self.go_to_next)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def update_button_text(self, instance, selected_language):
        self.language_button.text = selected_language

    def go_to_next(self, instance):
        if self.language_button.text != "Wybierz...":
            self.manager.current = "square_screen"
        else:
            error_popup = Popup(
                title="Błąd",
                content=Label(text="Proszę wybrać język!"),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
