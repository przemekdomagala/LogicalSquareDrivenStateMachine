import gui_common as c
from generate_code_screen import GenerateCodeScreen
from backend.code_generator import CodeGenerator

def go_back(self, instance):
    self.manager.current = "square_screen"

def go_next(self, instance):
    """Navigate to the next screen after selecting a state."""
    if not self.selected_leaves:
        popup = c.error_popup("Please select a state to expand.")
        popup.open()
        return
    
def go_to_generate_code(self, instance):
    """Navigate to the GenerateCodeScreen."""
    if "generate_code" not in self.manager.screen_names:
        self.manager.add_widget(GenerateCodeScreen(name="generate_code"))
    self.manager.current = "generate_code"
    code_generator = CodeGenerator()
    code_generator.generate_code(self.tree_data)