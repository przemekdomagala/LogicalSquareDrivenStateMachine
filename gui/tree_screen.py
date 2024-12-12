from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from generate_code_screen import GenerateCodeScreen
from state_chosen_screen import StateChosenScreen
from kivy.uix.spinner import Spinner
from backend.code_generator import CodeGenerator

class TreeScreen(Screen):
    def __init__(self, tree_data, **kwargs):
        super(TreeScreen, self).__init__(**kwargs)

        self.tree_data = tree_data  
        self.selected_leaves = []  
        self.expanded_states = []  

        layout = FloatLayout()

        background = Widget()
        with background.canvas:
            Color(0.1, 0.1, 0.2, 1)
            Rectangle(size=self.size, pos=self.pos)
        layout.add_widget(background)

        self.drawing_area = Widget()
        layout.add_widget(self.drawing_area)
        self.bind(size=self.draw_tree, pos=self.draw_tree)  

        button_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(1, 0.1),
            pos_hint={"x": 0, "y": 0},
            spacing=20,
            padding=[20, 10],
        )

        back_button = Button(
            text="Back",
            size_hint=(0.3, 1),
            background_color=(0.8, 0.1, 0.1, 1),
            color=(1, 1, 1, 1),
        )
        back_button.bind(on_release=self.go_back)
        button_layout.add_widget(back_button)

        self.expand_button = Button(
            text="Expand",
            size_hint=(0.3, 1),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        self.expand_button.bind(on_release=self.open_expand_popup)
        button_layout.add_widget(self.expand_button)

        next_button = Button(
            text="Next",
            size_hint=(0.3, 1),
            background_color=(0.1, 0.8, 0.1, 1),
            color=(1, 1, 1, 1),
        )
        next_button.bind(on_release=self.go_next)
        button_layout.add_widget(next_button)

        generate_code_button = Button(
            text="Generate Code",
            size_hint=(0.3, 1),
            background_color=(0.8, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
        )
        generate_code_button.bind(on_release=self.go_to_generate_code)
        button_layout.add_widget(generate_code_button)



        layout.add_widget(button_layout)
        self.add_widget(layout)

    def go_to_generate_code(self, instance):
        """Navigate to the GenerateCodeScreen."""
        if "generate_code" not in self.manager.screen_names:
            self.manager.add_widget(GenerateCodeScreen(name="generate_code"))
        self.manager.current = "generate_code"
        code_generator = CodeGenerator()
        code_generator.generate_code(self.tree_data)

    #region drawtree
    def draw_tree(self, *args):
        """Draw the tree structure with root and its descendants."""
        self.drawing_area.canvas.clear()
        with self.drawing_area.canvas:
            screen_width, screen_height = self.size
            root_x = screen_width / 2
            root_y = screen_height * 0.9

            Color(1, 1, 1, 1)  
            self.draw_circle(root_x, root_y, 50, "root") 

            def draw_children(parent_x, parent_y, children, level=1):
                if not children:
                    return
                
                num_children = len(children)
                child_spacing = screen_width / (num_children + 1)
                child_y = parent_y - screen_height * 0.2  

                for i, (child_name, grand_children) in enumerate(children.items()):
                    child_x = (i + 1) * child_spacing
                    color = (0.2, 0.8, 0.2, 1) if child_name in self.selected_leaves else (0.2, 0.6, 0.8, 1)
                    self.draw_circle(child_x, child_y, 50, child_name, color)

                    Line(points=[parent_x, parent_y - 50, child_x, child_y + 50], width=2)

                    draw_children(child_x, child_y, grand_children, level + 1)

            draw_children(root_x, root_y, self.tree_data["root"])

    def draw_circle(self, x, y, radius, text, color=(0.2, 0.6, 0.8, 1)):
        """Draw a circle with text at (x, y)."""
        Color(*color)
        Line(circle=(x, y, radius), width=3)

        Color(1, 1, 1, 1) 
        if(type(text) != str):
            text = text.name
        label = Label(
            text=text,
            font_size=radius // 2,  
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(radius * 2, radius * 2),
            pos=(x - radius, y - radius),
            halign="center",
            valign="middle",
        )
        label.text_size = label.size  
        label.texture_update()

        self.drawing_area.canvas.add(Rectangle(texture=label.texture, size=label.size, pos=label.pos))

    def confirm_expand_selection(self, popup, selected_state):
        """Update selected leaves based on dropdown selection."""
        if selected_state not in self.expanded_states and selected_state != "Select a state": 
            self.selected_leaves = [selected_state]
            self.expanded_states.append(selected_state)  
        else:
            popup.dismiss()
            return

        popup.dismiss()
        self.draw_tree()


    def go_back(self, instance):
        self.manager.current = "square_screen"

    def go_next(self, instance):
        """Navigate to the next screen after selecting a state."""
        if not self.selected_leaves:
            popup = Popup(
                title="Error",
                content=Label(text="Please select a state to expand."),
                size_hint=(0.6, 0.4),
            )
            popup.open()
            return

        selected_state = self.selected_leaves[0] 
        state_screen = StateChosenScreen(state_name=selected_state, name="state_chosen")
        self.selected_leaves = []

        if "state_chosen" in self.manager.screen_names:
            self.manager.remove_widget(self.manager.get_screen("state_chosen"))
        self.manager.add_widget(state_screen)

        self.manager.current = "state_chosen"
    def open_expand_popup(self, instance):
        """Open a popup to select one state for expansion using a dropdown."""
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=20, size_hint=(1, None))
        popup_layout.bind(minimum_height=popup_layout.setter('height'))

        def collect_unexpanded_leaves(tree, expanded):
            """Recursively find unexpanded leaves."""
            leaves = []
            for key, children in tree.items():
                if not children and key not in expanded:  
                    leaves.append(key)
                elif children:  
                    leaves.extend(collect_unexpanded_leaves(children, expanded))
            return leaves

        available_leaves = collect_unexpanded_leaves(self.tree_data["root"], self.expanded_states)

        if not available_leaves:
            error_popup = Popup(
                title="No Leaves Available",
                content=Label(text="All leaves have been expanded or have no children!"),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
            return

        for i in range(len(available_leaves)):
            if type(available_leaves[i]) == str:
                continue
            available_leaves[i] = available_leaves[i].name

        spinner = Spinner(
            text="Select state",
            values=available_leaves,
            size_hint=(1, None),
            height=40,
        )

        selected_label = Label(
            text="No state selected",
            size_hint=(1, None),
            height=40,
            color=(1, 1, 1, 1),
        )

        def on_spinner_select(spinner, value):
            """Update the label when a selection is made."""
            selected_label.text = f"Selected: {value}"

        spinner.bind(text=on_spinner_select)

        popup_layout.add_widget(Label(text="Choose state to expand:", size_hint=(1, None), height=40, color=(1, 1, 1, 1)))
        popup_layout.add_widget(spinner)
        popup_layout.add_widget(selected_label)

        button_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=20)
        confirm_button = Button(text="Confirm", size_hint_x=0.5)
        cancel_button = Button(text="Cancel", size_hint_x=0.5)

        confirm_button.bind(on_release=lambda x: self.confirm_expand_selection(popup, spinner.text))
        cancel_button.bind(on_release=lambda x: popup.dismiss())

        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)

        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(popup_layout)
        main_layout.add_widget(button_layout)

        popup = Popup(title="Expand Leaves", content=main_layout, size_hint=(0.8, 0.6), auto_dismiss=False)
        popup.open()