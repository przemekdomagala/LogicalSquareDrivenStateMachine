from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
import gui_common as c

# Global variable to store the selected language
# selected_language = None

class LanguageSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(LanguageSelectionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        label = Label(
            text="Choose language for code generation:",
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
        )
        layout.add_widget(label)

        self.selected_language = ""

        self.dropdown = DropDown()

        for lang in ["Python", "Java"]:
            btn = Button(
                text=lang, size_hint_y=None, height=50, background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.language_button = Button(
            text="Choose here...",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
        )
        self.language_button.bind(on_release=self.dropdown.open)

        self.dropdown.bind(on_select=self.update_button_text)

        layout.add_widget(self.language_button)

        next_button = Button(
            text="Next",
            size_hint=(1, 0.2),
            background_color=(0.4, 0.8, 0.2, 1),
            color=(1, 1, 1, 1),
        )
        next_button.bind(on_release=self.go_to_next)
        layout.add_widget(next_button)

        self.add_widget(layout)

    def update_button_text(self, instance, selected_lang):
        self.language_button.text = selected_lang
        # global selected_language  # Update the global variable
        selected_language = selected_lang

    def go_to_next(self, instance):
        if self.language_button.text != "Choose here...":
            # global selected_language  # Update the global variable
            # selected_language = self.language_button.text
            c.chosen_language = self.language_button.text
            self.selected_language = self.language_button.text
            self.manager.current = "square_screen"
        else:
            error_popup = Popup(
                title="Error",
                content=Label(text="Please select a language!"),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()

    # def get_selected_language(self):
        # print("Wybrany jezyk: "+selected_language)
        # return self.selected_language