from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from backend.code_generator import CodeGenerator
import gui_common as c

class GenerateCodeScreen(Screen):
    def __init__(self, state_machine, transitions, **kwargs):
        super(GenerateCodeScreen, self).__init__(**kwargs)

        self.state_machine = state_machine
        self.transitions = transitions

        self.lang_ = c.chosen_language

        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        label = Label(
            text="Generate your code here!",
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
            halign="center",
            valign="middle"
        )
        layout.add_widget(label)

        button_layout = BoxLayout(orientation="horizontal", size_hint=(1, 0.2), spacing=20)
        back_button = Button(text="Back", size_hint=(0.5, 1))
        back_button.bind(on_release=self.go_back)
        button_layout.add_widget(back_button)

        generate_button = Button(text="Generate", size_hint=(0.5, 1))
        generate_button.bind(on_release=self.generate_code)
        button_layout.add_widget(generate_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = "tree_screen"  

    def generate_code(self, instance):
        code_generator = CodeGenerator(self.state_machine, self.transitions)
        
        # Use the selected_language variable
        code_generator.generate_code(language=self.lang_)
        
        popup = Popup(
            title="Code Generated",
            content=Label(text=f"Your code has been generated in {self.lang_}!"),
            size_hint=(0.6, 0.4),
        )
        popup.open()

    def get_states_and_transitions(self, states, transitions):
        self.states = states
        self.transitions = transitions
