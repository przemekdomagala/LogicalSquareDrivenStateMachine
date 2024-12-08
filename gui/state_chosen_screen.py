from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from square_widget import SquareWidget

from states_identifier import StatesIdentifier

class StateChosenScreen(Screen):
    def __init__(self, state_name, **kwargs):
        super(StateChosenScreen, self).__init__(**kwargs)
        self.state_name = state_name
        self.inputs = []

        layout = FloatLayout()

        # Instructions
        instructions = Label(
            text=f"State chosen to expand: {self.state_name}\n(Lewy górny róg must be first!)",
            font_size=20,
            color=(1, 1, 1, 1),
            size_hint=(1, 0.1),
            pos_hint={"x": 0, "top": 1},
        )
        layout.add_widget(instructions)

        square_widget = SquareWidget(size_hint=(1, 0.8), pos_hint={"x": 0, "y": 0.1})
        layout.add_widget(square_widget)

        # Input fields layout
        square_layout = FloatLayout(size_hint=(1, 0.8), pos_hint={"x": 0, "y": 0.1})
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
            square_layout.add_widget(input_box)

        layout.add_widget(square_layout)

        # Button layout
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

        save_button = Button(
            text="Save & Update Tree",
            size_hint=(0.4, 1),
            background_color=(0.1, 0.8, 0.1, 1),
            color=(1, 1, 1, 1),
        )
        save_button.bind(on_release=self.save_and_update_tree)
        button_layout.add_widget(save_button)

        layout.add_widget(button_layout)
        self.add_widget(layout)

    def check_top_left(self, instance, value):
        """Enable/disable other inputs based on the top-left corner."""
        if value.strip() == "":
            for i, input_box in enumerate(self.inputs):
                if i != 0:
                    input_box.text = ""
                    input_box.disabled = True
        else:
            for i, input_box in enumerate(self.inputs):
                if i != 0:
                    input_box.disabled = False

    def save_and_update_tree(self, instance):
        """Save the new square's leaves and update the tree on `TreeScreen`."""
        new_leaves = [input_box.text for input_box in self.inputs]
        state_identifier = StatesIdentifier()
        new_leaves = state_identifier._idenfity_states(new_leaves)


        if not new_leaves:
            popup = Popup(
                title="Error",
                content=Label(text="All fields must be filled in!"),
                size_hint=(0.6, 0.4),
            )
            popup.open()
            return
    
        # Get the TreeScreen instance
        tree_screen = self.manager.get_screen("tree_screen")
    
        # Update tree_data to include the new leaves
        current_state = tree_screen.tree_data["root"].get(self.state_name, {})
        for leaf in new_leaves:
            current_state[leaf] = {}  # Add the new leaf with an empty dictionary as its children
    
        tree_screen.tree_data["root"][self.state_name] = current_state  # Update the tree_data
        tree_screen.draw_tree()  # Redraw the tree with updated data
    
        self.manager.current = "tree_screen"


    def go_back(self, instance):
        self.manager.current = "tree_screen"