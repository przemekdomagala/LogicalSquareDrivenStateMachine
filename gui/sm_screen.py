from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Line, Color, Rectangle
import math

class SMScreen(Screen):
    def __init__(self, tree_data, **kwargs):
        super(SMScreen, self).__init__(**kwargs)
        self.tree_data = tree_data
        self.transitions = []
        self.state_positions = {}

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        add_transition_button = Button(
            text="Add Transition",
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1)
        )
        add_transition_button.bind(on_release=self.open_add_transition_popup)
        layout.add_widget(add_transition_button)

        back_button = Button(
            text="Back",
            size_hint=(1, 0.2),
            background_color=(0.8, 0.1, 0.1, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_release=self.go_back)
        layout.add_widget(back_button)

        check_attributes_button = Button(
            text="check State Attributes",
            size_hint=(1, 0.2),
            background_color=(0.4, 0.4, 0.4, 1),
            color=(1, 1, 1, 1)
        )
        check_attributes_button.bind(on_release=self.open_check_attributes_popup)
        layout.add_widget(check_attributes_button)

        self.drawing_area = Widget()
        layout.add_widget(self.drawing_area)

        self.add_widget(layout)
        self.bind(size=self.draw_states)

    def on_enter(self):
        self.draw_states()
        
        
    def open_add_transition_popup(self, instance):
        content = FloatLayout()

        all_states = self.collect_all_states(self.tree_data)

        source_spinner = Spinner(
            text='Select Source State',
            values=all_states,
            size_hint=(0.8, 0.1),
            pos_hint={'x': 0.1, 'y': 0.8}
        )
        content.add_widget(source_spinner)

        destination_spinner = Spinner(
            text='Select Destination State',
            values=all_states,
            size_hint=(0.8, 0.1),
            pos_hint={'x': 0.1, 'y': 0.7}
        )
        content.add_widget(destination_spinner)

        event_input = TextInput(
            hint_text='Event',
            size_hint=(0.8, 0.1),
            pos_hint={'x': 0.1, 'y': 0.6}
        )
        content.add_widget(event_input)

        guard_input = TextInput(
            hint_text='Guard (optional)',
            size_hint=(0.8, 0.1),
            pos_hint={'x': 0.1, 'y': 0.5}
        )
        content.add_widget(guard_input)

        action_input = TextInput(
            hint_text='Action (optional)',
            size_hint=(0.8, 0.1),
            pos_hint={'x': 0.1, 'y': 0.4}
        )
        content.add_widget(action_input)

        add_button = Button(
            text='Add Transition',
            size_hint=(0.8, 0.1),
            pos_hint={'x': 0.1, 'y': 0.2}
        )
        popup = Popup(title='Add Transition', content=content, size_hint=(0.8, 0.7))
        add_button.bind(on_release=lambda x: self.add_transition(
            source_spinner.text, 
            destination_spinner.text, 
            event_input.text, 
            guard_input.text, 
            action_input.text, 
            popup
        ))
        content.add_widget(add_button)

        popup.open()

    def add_transition(self, source, destination, popup):
        if source in self.collect_all_states(self.tree_data) and destination in self.collect_all_states(self.tree_data):
            self.transitions.append({'from': source, 'to': destination})
            popup.dismiss()
        # Logic to update the drawing area with the new transition
        self.draw_states()

    def go_back(self, instance):
        self.manager.current = 'tree_screen'

    def draw_states(self, *args):
        self.drawing_area.canvas.clear()
        self.state_positions.clear()
        with self.drawing_area.canvas:
            Color(1, 1, 1, 1)
            self.draw_tree(self.tree_data, self.width / 2, self.height / 2, self.width / 4)
            self.draw_transitions()

    def draw_tree(self, tree, x, y, spacing):
        levels = self.create_hierarchical_layout(tree)
        for level, states in enumerate(levels):
            y_pos = y - level * 150
            x_pos = x - (len(states) - 1) * spacing / 2
            for state in states:
                self.draw_state(x_pos, y_pos, state)
                x_pos += spacing

    def draw_state(self, x, y, state):
        radius = 50
        Color(0.2, 0.6, 0.8, 1)
        Line(circle=(x, y, radius), width=2)
        label = Label(
            text=str(state),  # Ensure state is a string
            font_size=20,
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
        self.state_positions[state] = (x, y)

    def draw_transitions(self):
        for transition in self.transitions:
            source_pos = self.state_positions.get(transition['from'])
            dest_pos = self.state_positions.get(transition['to'])
            if source_pos and dest_pos:
                self.draw_arrow(source_pos, dest_pos)

    def draw_arrow(self, start, end):
        radius = 50
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        start_x = start[0] + radius * math.cos(angle)
        start_y = start[1] + radius * math.sin(angle)
        end_x = end[0] - radius * math.cos(angle)
        end_y = end[1] - radius * math.sin(angle)
        
        with self.drawing_area.canvas:
            Color(1, 0, 0, 1)
            Line(points=[start_x, start_y, end_x, end_y], width=2)
            # Draw arrowhead
            arrow_size = 10
            arrow_x1 = end_x - arrow_size * math.cos(angle - math.pi / 6)
            arrow_y1 = end_y - arrow_size * math.sin(angle - math.pi / 6)
            arrow_x2 = end_x - arrow_size * math.cos(angle + math.pi / 6)
            arrow_y2 = end_y - arrow_size * math.sin(angle + math.pi / 6)
            Line(points=[end_x, end_y, arrow_x1, arrow_y1], width=2)
            Line(points=[end_x, end_y, arrow_x2, arrow_y2], width=2)

    def create_hierarchical_layout(self, tree):
        """Create a hierarchical layout of states."""
        levels = []
        self._create_hierarchical_layout_helper(tree, 0, levels)
        return levels

    def _create_hierarchical_layout_helper(self, tree, level, levels):
        if len(levels) <= level:
            levels.append([])
        for key, children in tree.items():
            if key != 'root':
                levels[level].append(key.name)
            if children:
                self._create_hierarchical_layout_helper(children, level + 1, levels)

    def collect_all_states(self, tree):
        """Recursively collect all states."""
        states = []
        for key, children in tree.items():
            if key != 'root': states.append(key.name)
            if children:
                states.extend(self.collect_all_states(children))
        return states

    def open_check_attributes_popup(self, instance):
        content = FloatLayout()

        all_states = self.collect_all_states(self.tree_data)

        state_spinner = Spinner(
            text='Select State',
            values=all_states,
            size_hint=(0.8, 0.1),
            pos_hint={'x': 0.1, 'y': 0.6}
        )
        content.add_widget(state_spinner)

        check_button = Button(
            text='check Attributes',
            size_hint=(0.8, 0.1),
            pos_hint={'x': 0.1, 'y': 0.4}
        )
        check_button.bind(on_release=lambda x: self.show_state_attributes(state_spinner.text))
        content.add_widget(check_button)

        popup = Popup(title='check State Attributes', content=content, size_hint=(0.8, 0.5))
        popup.open()

    def show_state_attributes(self, state_name):
        state = self.find_state_by_name(state_name)
        if state:
            # attributes = state.attributes
            # attributes_str = "\n".join([str(attr) for attr in attributes])
            for attr in state.attributes:
                attributes_str = attr.name + " = " + attr.value['value']
                # attributes_str = state.attributes[0]['name']+" "+state.attributes[0].value['value']
            content = Label(text=attributes_str)
            popup = Popup(title=f'Attributes of {state_name}', content=content, size_hint=(0.8, 0.5))
            popup.open()

    def find_state_by_name(self, state_name):
        for key, children in self.tree_data.items():
            if key != 'root' and key.name == state_name:
                return key
            if children:
                result = self.find_state_by_name_in_tree(state_name, children)
                if result:
                    return result
        return None

    def find_state_by_name_in_tree(self, state_name, tree):
        for key, children in tree.items():
            if key.name == state_name:
                return key
            if children:
                result = self.find_state_by_name_in_tree(state_name, children)
                if result:
                    return result
        return None

    def update_screen(self, new_tree_data):
        self.tree_data = new_tree_data
        self.draw_states()