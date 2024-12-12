from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from square_widget import SquareWidget
from tree_screen import TreeScreen
from states_identifier import StatesIdentifier

class SquareScreen(Screen):
    def __init__(self, **kwargs):
        super(SquareScreen, self).__init__(**kwargs)

        layout = FloatLayout()

        instructions = Label(
            text="Fill square's corners with predicates:\nLeft top corner predicate is initial, must always be filled!",
            font_size=20,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1),
            pos_hint={"x": 0, "top": 1},
        )
        layout.add_widget(instructions)

        square_widget = SquareWidget(size_hint=(1, 0.8), pos_hint={"x": 0, "y": 0.1})
        layout.add_widget(square_widget)

        self.inputs = []
        positions = [
            {"x": 0.1, "top": 0.9}, 
            {"x": 0.8, "top": 0.9}, 
            {"x": 0.1, "top": 0.2}, 
            {"x": 0.8, "top": 0.2}, 
        ]

        for i, pos in enumerate(positions):
            input_box = TextInput(
                size_hint=(0.1, 0.05),
                pos_hint=pos,
                multiline=False,
                background_color=(0.2, 0.2, 0.4, 1),
                foreground_color=(1, 1, 1, 1),
            )
            if i == 0:
                input_box.bind(text=self.check_top_left)
            else:
                input_box.disabled = True

            self.inputs.append(input_box)
            layout.add_widget(input_box)

        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.1),
            pos_hint={"x": 0, "y": 0},
            spacing=20,
            padding=[20, 10],
        )

        back_button = Button(
            text="Back",
            size_hint=(0.4, 1),
            background_color=(0.8, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
        )
        back_button.bind(on_release=self.go_back)
        button_layout.add_widget(back_button)

        next_button = Button(
            text="Next",
            size_hint=(0.4, 1),
            background_color=(0.1, 0.8, 0.1, 1),
            color=(1, 1, 1, 1),
        )
        next_button.bind(on_release=self.go_next)
        button_layout.add_widget(next_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def check_top_left(self, instance, value):
        """Enables/disables other fields based on the top-left corner value."""
        if value.strip() == "":
            for i, input_box in enumerate(self.inputs):
                if i != 0:
                    input_box.text = "" 
                    input_box.disabled = True
        else:
            for i, input_box in enumerate(self.inputs):
                if i != 0:
                    input_box.disabled = False

    def go_back(self, instance):
        self.manager.current = "language_selection"

    def go_next(self, instance):
        if self.inputs[0].text.strip() == "":
            popup = Popup(
                title="Błąd",
                content=Label(text="Left top corner must always be filled!"),
                size_hint=(0.6, 0.4),
            )
            popup.open()
            return

        leaves = [input_box.text.strip() for input_box in self.inputs]

        states_identifier = StatesIdentifier()
        states = states_identifier._idenfity_states(leaves)
        root = {
            "root": {state.name: {} for state in states}  
        }

        if "tree_screen" in self.manager.screen_names:
            self.manager.remove_widget(self.manager.get_screen("tree_screen"))

        tree_screen = TreeScreen(tree_data=root, name="tree_screen")  
        self.manager.add_widget(tree_screen)

        self.manager.current = "tree_screen"