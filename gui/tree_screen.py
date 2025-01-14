from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from state_chosen_screen import StateChosenScreen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from backend.attribute import Attribute
from gui.tree_screen_navigation import go_next, go_back, go_to_generate_code
from backend.prover_input_generator import check_disjointness

import gui_common as c

class TreeScreen(Screen):
    def __init__(self, tree_data, **kwargs):
        super(TreeScreen, self).__init__(**kwargs)

        self.tree_data = tree_data  
        self.selected_leaves = []  
        self.expanded_states = []  
        self.states = []

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
        back_button.bind(on_release=go_back)
        button_layout.add_widget(back_button)

        self.expand_button = Button(
            text="Expand",
            size_hint=(0.3, 1),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        self.expand_button.bind(on_release=self.open_expand_popup)
        button_layout.add_widget(self.expand_button)

        #
        self.rename_button = Button(
        text="Rename",
        size_hint=(0.3, 1),
        background_color=(0.5, 0.3, 0.8, 1),
        color=(1, 1, 1, 1)
        )
        self.rename_button.bind(on_release=self.open_rename_popup)
        button_layout.add_widget(self.rename_button)
        #


        #region attributes_button
        self.add_attribute_button = Button(
            text="Add Attribute",
            size_hint=(0.3, 1),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
        )
        self.add_attribute_button.bind(on_release=self.open_add_attribute_popup)
        button_layout.add_widget(self.add_attribute_button)

        prover_button = Button(
            text="Prover",
            size_hint=(0.3, 1),
            background_color=(0.5, 0.5, 0.5, 1),
            color=(1, 1, 1, 1)
        )
        prover_button.bind(on_release=self.open_prover_popup)
        button_layout.add_widget(prover_button)

        next_button = Button(
            text="Next",
            size_hint=(0.3, 1),
            background_color=(0.1, 0.8, 0.1, 1),
            color=(1, 1, 1, 1),
        )
        next_button.bind(on_release=go_next)
        button_layout.add_widget(next_button)

        generate_code_button = Button(
            text="Generate Code",
            size_hint=(0.3, 1),
            background_color=(0.8, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
        )
        generate_code_button.bind(on_release=go_to_generate_code)
        button_layout.add_widget(generate_code_button)



        layout.add_widget(button_layout)
        self.add_widget(layout)



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
                
                for i, (child, grand_children) in enumerate(children.items()):
                    child_x = (i + 1) * child_spacing
                    color = (0.2, 0.8, 0.2, 1) if child in self.selected_leaves else (0.2, 0.6, 0.8, 1)
                    self.draw_circle(child_x, child_y, 50, child.name, color)

                    Line(points=[parent_x, parent_y - 50, child_x, child_y + 50], width=2)

                    draw_children(child_x, child_y, grand_children, level + 1)

            draw_children(root_x, root_y, self.tree_data["root"])


    
    def extract_states(self):
        pass

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


        selected_state = self.selected_leaves[0] 
        # state_screen = StateChosenScreen(state_name=selected_state.name, name="state_chosen")
        state_screen = StateChosenScreen(state=selected_state, name="state_chosen")
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
            displayed_leaves = {}
            for leaf in available_leaves:
                displayed_leaves[leaf.name] = leaf
            # available_leaves[i] = available_leaves[i].name

        spinner = Spinner(
            text="Select state",
            values=displayed_leaves.keys(),
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

        error_popup = c.error_popup("Please select a state to expand.")

        confirm_button.bind(on_release=lambda x: self.confirm_expand_selection(popup, displayed_leaves[spinner.text]) 
                            if spinner.text != 'Select state' 
                            else error_popup.open())
        
        cancel_button.bind(on_release=lambda x: popup.dismiss())

        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)

        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(popup_layout)
        main_layout.add_widget(button_layout)

        popup = Popup(title="Expand Leaves", content=main_layout, size_hint=(0.8, 0.6), auto_dismiss=False)
        popup.open()

    def open_rename_popup(self, instance):
        """Open a popup to rename a selected state."""
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=20, size_hint=(1, None))
        popup_layout.bind(minimum_height=popup_layout.setter('height'))

        # Collect all states available for renaming
        def collect_all_states(tree):
            """Recursively collect all states."""
            states = []
            for key, children in tree.items():
                states.append(key)
                if children:
                    states.extend(collect_all_states(children))
            return states

        available_states = collect_all_states(self.tree_data["root"])

        helper_dict = {}

        for i in range(len(available_states)):
            if type(available_states[i]) == str:
                continue
            helper_dict[available_states[i].name] = available_states[i]
            available_states[i] = available_states[i].name

        if not available_states:
            error_popup = Popup(
                title="No States Available",
                content=Label(text="No states available for renaming!"),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
            return

        # Spinner to select the state
        spinner = Spinner(
            text="Select state",
            values=helper_dict.keys(),
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

        # Text input for the new name
        rename_input = TextInput(
            hint_text="Enter new name",
            multiline=False,
            size_hint=(1, None),
            height=40,
        )

        # Popup layout
        popup_layout.add_widget(Label(text="Choose state to rename:", size_hint=(1, None), height=40, color=(1, 1, 1, 1)))
        popup_layout.add_widget(spinner)
        popup_layout.add_widget(Label(text="Enter new name:", size_hint=(1, None), height=40, color=(1, 1, 1, 1)))
        popup_layout.add_widget(rename_input)
        popup_layout.add_widget(selected_label)

        # Buttons for Confirm and Cancel
        button_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=20)
        confirm_button = Button(text="Confirm", size_hint_x=0.5)
        cancel_button = Button(text="Cancel", size_hint_x=0.5)

        error_popup = c.error_popup("Please select a state to rename.")

        confirm_button.bind(on_release=lambda x: self.confirm_rename_selection(popup, helper_dict[spinner.text]
                                                                               if spinner.text != 'Select state' 
                                                                                else error_popup.open()
                                                                               , rename_input.text))
        cancel_button.bind(on_release=lambda x: popup.dismiss())

        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)

        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(popup_layout)
        main_layout.add_widget(button_layout)

        popup = Popup(title="Rename State", content=main_layout, size_hint=(0.8, 0.6), auto_dismiss=False)
        popup.open()

    def confirm_rename_selection(self, popup, state_to_rename, new_name):
        """Handle the renaming process."""

        if not state_to_rename:
            return
    
        if not new_name.strip():
            error_popup = Popup(
                title="Invalid Name",
                content=Label(text="New name cannot be empty."),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
            return
    
        # Rename the state in the tree data
        def rename_state(tree, target, new_name):
            """Recursively rename the state in the tree."""
            for key, children in list(tree.items()):
                if key == target:
                    # tree[new_name] = tree.pop(key)  # Rename the key
                    # tree[key].name = new_name
                    target.name = new_name
                    return True
                elif children:
                    if rename_state(children, target, new_name):
                        return True
            return False

        old_name = state_to_rename.name
        if rename_state(self.tree_data["root"], state_to_rename, new_name):
            popup.dismiss()
    
            # **Redraw the tree after renaming**
            self.draw_tree()
    
            success_popup = Popup(
                title="Rename Successful",
                content=Label(text=f"State '{old_name}' has been renamed to '{new_name}'."),
                size_hint=(0.6, 0.4),
            )
            success_popup.open()
        else:
            error_popup = Popup(
                title="Rename Failed",
                content=Label(text="Failed to rename the selected state."),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
    
    def open_add_attribute_popup(self, instance):
        """Open a popup to add an attribute to a selected state."""
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=10, size_hint=(1, None))
        popup_layout.bind(minimum_height=popup_layout.setter('height'))
    
        # Collect all states available for adding attributes
        def collect_all_states(tree):
            """Recursively collect all states."""
            states = []
            for key, children in tree.items():
                states.append(key)
                if children:
                    states.extend(collect_all_states(children))
            return states
    
        available_states = collect_all_states(self.tree_data["root"])
        helper_dict = {}
        for i in range(len(available_states)):
            if type(available_states[i]) == str:
                continue
            helper_dict[available_states[i].name] = available_states[i]
            available_states[i] = available_states[i].name
    
        if not available_states:
            error_popup = Popup(
                title="No States Available",
                content=Label(text="No states available for adding attributes!"),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
            return
    
        # Spinner to select the state
        spinner = Spinner(
            text="Select state",
            values=helper_dict.keys(),
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
    
        # Input for attribute name
        attribute_name_input = TextInput(
            hint_text="Enter attribute name",
            multiline=False,
            size_hint=(1, None),
            height=40,
        )
    
        # Spinner to choose attribute type
        attribute_type_spinner = Spinner(
            text="Select attribute type",
            values=["Value", "Range"],
            size_hint=(1, None),
            height=40,
        )
        
        # Dynamic layout for attribute input
        attribute_input_layout = BoxLayout(orientation="vertical", size_hint=(1, None))
    
        # Inputs for value
        attribute_value_input = TextInput(
            hint_text="Enter attribute value",
            multiline=False,
            size_hint=(1, None),
            height=40,
        )
    
        # Inputs for range
        range_start_input = TextInput(
            hint_text="Enter range start",
            multiline=False,
            size_hint=(1, None),
            height=40,
        )
        range_end_input = TextInput(
            hint_text="Enter range end",
            multiline=False,
            size_hint=(1, None),
            height=40,
        )
        range_bound_spinner = Spinner(
            text="Select range bound type",
            values=["Closed", "Open Start", "Open End", "Open Both"],
            size_hint=(1, None),
            height=40,
        )
    
        # Function to toggle inputs based on selected type
        def update_attribute_inputs(spinner, value):
            attribute_input_layout.clear_widgets()
            if value == "Value":
                attribute_input_layout.add_widget(attribute_value_input)
            elif value == "Range":
                attribute_input_layout.add_widget(range_start_input)
                attribute_input_layout.add_widget(range_end_input)
                attribute_input_layout.add_widget(range_bound_spinner)
    
        attribute_type_spinner.bind(text=update_attribute_inputs)
    
        # Initial setup
        attribute_input_layout.add_widget(attribute_value_input)
    
        # Popup layout
        popup_layout.add_widget(Label(text="Choose state to add attribute:", size_hint=(1, None), height=40, color=(1, 1, 1, 1)))
        popup_layout.add_widget(spinner)
        popup_layout.add_widget(Label(text="Enter attribute name:", size_hint=(1, None), height=40, color=(1, 1, 1, 1)))
        popup_layout.add_widget(attribute_name_input)
        popup_layout.add_widget(Label(text="Select attribute type:", size_hint=(1, None), height=40, color=(1, 1, 1, 1)))
        popup_layout.add_widget(attribute_type_spinner)
        popup_layout.add_widget(attribute_input_layout)
        popup_layout.add_widget(selected_label)
    
        # Buttons for Confirm and Cancel
        button_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=20)
        confirm_button = Button(text="Confirm", size_hint_x=0.5)
        cancel_button = Button(text="Cancel", size_hint_x=0.5)
    
        error_popup = c.error_popup("Please select a state to add an attribute.")
    
        def confirm_action(instance):
            if spinner.text == 'Select state':
                error_popup.open()
                return
            state = helper_dict[spinner.text]
            attribute_name = attribute_name_input.text
            if not attribute_name:
                error_popup.content = Label(text="Please enter an attribute name!")
                error_popup.open()
                return
            if attribute_type_spinner.text == "Value":
                value = attribute_value_input.text
                self.confirm_add_attribute(popup, state, attribute_name, {"kind": "Value", "value": value})
            elif attribute_type_spinner.text == "Range":
                start = range_start_input.text
                end = range_end_input.text
                bound_type = range_bound_spinner.text
                self.confirm_add_attribute(popup, state, attribute_name, {
                    "kind": "Range",
                    "start": start,
                    "end": end,
                    "bound_type": bound_type
                })
    
        confirm_button.bind(on_release=confirm_action)
        cancel_button.bind(on_release=lambda x: popup.dismiss())
    
        button_layout.add_widget(confirm_button)
        button_layout.add_widget(cancel_button)
    
        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(popup_layout)
        main_layout.add_widget(button_layout)
    
        popup = Popup(title="Add Attribute", content=main_layout, size_hint=(0.95, 0.95), auto_dismiss=False)
        popup.open()

    
    def confirm_add_attribute(self, popup, state, attribute_name, attribute_value):
        """Handle the process of adding an attribute to a state."""
        isValue = attribute_value["kind"] == "Value"
        initial_value = attribute_value
        if isValue: 
            attribute_value = attribute_value["value"]
        
        if not state or state == "Select state":
            return
        if not attribute_name.strip():
            error_popup = Popup(
                title="Invalid Attribute Name",
                content=Label(text="Attribute name cannot be empty."),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
            return
        if isValue and not attribute_value.strip():
            error_popup = Popup(
                title="Invalid Attribute Value",
                content=Label(text="Attribute value cannot be empty."),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
            return
        elif isValue and attribute_value.strip():
            try:
            # Check for boolean
                if attribute_value.lower() in ['true', 'false']:
                    attribute_value = bool(attribute_value.lower() == 'true')
                # Check for integer
                if attribute_value.isdigit() or (attribute_value.startswith('-') and attribute_value[1:].isdigit()):
                    attribute_value = int(attribute_value)
                # Check for float
                elif float(attribute_value):  # If this doesn't raise an error, it's a float
                    attribute_value = float(attribute_value)
            except ValueError:
                attribute_value = str(attribute_value)    
        elif not isValue:
            if not attribute_value["start"].strip():
                attribute_value["start"] = float("-inf")
            else:
                try:
                    attribute_value["start"] = float(attribute_value["start"])
                except ValueError:
                    error_popup = c.error_popup("Invalid range start value.")
                    error_popup.open()
                    return
            if not attribute_value["end"].strip():
                attribute_value["end"] = float("inf")
            else:
                try:
                    attribute_value["end"] = float(attribute_value["end"])
                except ValueError:
                    error_popup = c.error_popup("Invalid range end value.")
                    error_popup.open()
                    return

            if attribute_value["start"] > attribute_value["end"]:
                error_popup = c.error_popup("Range start value cannot be greater than range end value.")
                error_popup.open()

        # Add the attribute to the state
        state.add_attribute(Attribute(attribute_name, initial_value))

        popup.dismiss()
        # Redraw the tree after adding the attribute
        self.draw_tree()
        success_popup = Popup(
            title="Attribute Added",
            content=Label(text=f"Attribute '{attribute_name}' has been added to state '{state.name}' with value '{attribute_value}'."),
            size_hint=(0.6, 0.4),
        )
        success_popup.open()

    def open_prover_popup(self, instance):
        """Open a popup for the prover functionality."""
        def has_attributes(tree):
            """Recursively check if any state in the tree has attributes."""
            for key, children in tree.items():
                if key.attributes:
                    return True
                if children and has_attributes(children):
                    return True
            return False

        if not has_attributes(self.tree_data["root"]):
            error_popup = Popup(
                title="No Attributes Found",
                content=Label(text="No states with attributes found in the tree."),
                size_hint=(0.6, 0.4),
            )
            error_popup.open()
            return

        # Popup layout
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=20, size_hint=(1, None))
        popup_layout.bind(minimum_height=popup_layout.setter('height'))

        prover_spinner = Spinner(
            text="Select prover",
            values=["z3", "vampire"],
            size_hint=(1, None),
            height=40,
        )

        selected_label = Label(
            text="No prover selected",
            size_hint=(1, None),
            height=40,
            color=(1, 1, 1, 1),
        )

        def on_spinner_select(spinner, value):
            """Update the label when a selection is made."""
            selected_label.text = f"Selected: {value}"

        prover_spinner.bind(text=on_spinner_select)

        popup_layout.add_widget(Label(text="Choose prover:", size_hint=(1, None), height=40, color=(1, 1, 1, 1)))
        popup_layout.add_widget(prover_spinner)
        popup_layout.add_widget(selected_label)

        button_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=20)
        check_button = Button(text="Check", size_hint_x=0.5)
        cancel_button = Button(text="Cancel", size_hint_x=0.5)

        def check_action(instance):
            if prover_spinner.text == 'Select prover':
                error_popup = Popup(
                    title="No Prover Selected",
                    content=Label(text="Please select a prover."),
                    size_hint=(0.6, 0.4),
                )
                error_popup.open()
                return
            elif prover_spinner.text == 'vampire':
                error_popup = Popup(
                    title="Not Implemented",
                    content=Label(text="Vampire prover is not implemented yet."),
                    size_hint=(0.6, 0.4),
                )
                error_popup.open()
                return
            elif prover_spinner.text == 'z3':
                states = self.collect_all_states_with_attributes(self.tree_data["root"])
                result = check_disjointness(states)
                self.display_prover_result(result)

        check_button.bind(on_release=check_action)
        cancel_button.bind(on_release=lambda x: popup.dismiss())

        button_layout.add_widget(check_button)
        button_layout.add_widget(cancel_button)

        main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(popup_layout)
        main_layout.add_widget(button_layout)

        popup = Popup(title="Prover", content=main_layout, size_hint=(0.8, 0.6), auto_dismiss=False)
        popup.open()

    def display_prover_result(self, result):
        """Display the result of the prover on the screen."""
        result_popup = Popup(
            title="Prover Result",
            content=Label(text=f"Prover Result: {result}"),
            size_hint=(0.6, 0.4),
        )
        result_popup.open()

    def collect_all_states_with_attributes(self, tree):
        """Recursively collect all states with attributes."""
        states = []
        for key, children in tree.items():
            if key.attributes:
                states.append(key)
            if children:
                states.extend(self.collect_all_states_with_attributes(children))
        return states