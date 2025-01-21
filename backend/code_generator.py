class CodeGenerator:
    def __init__(self, states, transitions):
        self.states = states
        self.transitions = transitions
        # self.code = ""
        # self.states = {}

        # self.states = self.collect_all_states(states)
        self.states = self.collect_all_states_objects(states)
        

    def collect_all_states(self, tree):
        """Recursively collect all states."""
        states = []
        for key, children in tree.items():
            if key != 'root': states.append(key.name)
            if children:
                states.extend(self.collect_all_states(children))
        return states
    
    def generate_code(self, language):
        if language == "Java":
            self.generate_java_code()
            return
        code_string = '''from abc import ABC, abstractmethod

# Interface representing a state
class State(ABC):
    # Abstract method to handle an event in the context
    @abstractmethod
    def handle_event(self, context):
        pass\n\n'''
        for state in self.states:
            code_string += f"class {state.name}(State):\n   def handle_event(self, context):\n"
            for transition in self.transitions:
                if(transition['from'] == state):
                    code_string += f"       if {transition['event']}:\n"
                    if(len(transition['guard']) != 0):
                        code_string += f"           if {transition['guard']}:\n"
                        if(len(transition['action']) != 0):
                            code_string += f"               {transition['action']}()\n"
                            code_string += f"               context.set_state({transition['to'].name}())\n"
                        else:
                            code_string += f"               context.set_state({transition['to'].name}())\n"
                    else:
                        if(len(transition['action']) != 0):
                            code_string += f"           {transition['action']}()\n"
                            code_string += f"           context.set_state({transition['to'].name}())\n"
                        else:
                            code_string += f"       context.set_state({transition['to'].name}())\n"
        
            code_string += "\n\n"

        code_string += f'''class Context:
    def __init__(self):
        # Setting initial state to State1a
        self.current_state = {self.states[0].name}
    # Method to set the current state
    def set_state(self, state):
        self.current_state 
    # Method to handle an event
    def handle_event(self):
        # Delegating event to the current state
        self.current_state.handle_event(self)'''
        
        number_of_transitions = len(self.transitions)
        
        code_string += f'''\n\nif __name__ == "__main__":
    context = Context()
    for i in range({number_of_transitions}):
        context.handle_event()'''
        
        with open("generated_code.py", "w") as file:
            file.write(code_string)
                        
        

    # def generate_code(self, graph):
    #     self.print_nested_dict(graph)
    #     self.states = graph

    # def print_nested_dict(self, d, indent=0):
    #     for key, value in d.items():
    #         if isinstance(value, dict):  
    #             print("  " * indent + f"{key}:")
    #             self.print_nested_dict(value, indent + 1)
    #         else:
    #             print("  " * indent + f"{key}: {value}")

    def collect_all_states_objects(self, tree):
        """Recursively collect all states."""
        states = []
        for key, children in tree.items():
            if key != 'root': 
                key.name = key.name.replace(" ", "_").replace('&', 'and')
                states.append(key)
            if children:
                states.extend(self.collect_all_states_objects(children))
        return states
    
    def generate_java_code(self):
        code_string = """// Interface representing a state
    public interface State {
        // Method to handle an event in the context
        void handleEvent(Context context);
    }

    """

        for state in self.states:
            code_string += f"public class {state.name} implements State {{\n"
            code_string += f"    @Override\n"
            code_string += f"    public void handleEvent(Context context) {{\n"
            for transition in self.transitions:
                if transition['from'] == state:
                    code_string += f"        if ({transition['event']}) {{\n"
                    if len(transition['guard']) != 0:
                        code_string += f"            if ({transition['guard']}) {{\n"
                        if len(transition['action']) != 0:
                            code_string += f"                {transition['action']}();\n"
                            code_string += f"                context.setState(new {transition['to'].name}());\n"
                        else:
                            code_string += f"                context.setState(new {transition['to'].name}());\n"
                        code_string += f"            }}\n"
                    else:
                        if len(transition['action']) != 0:
                            code_string += f"            {transition['action']}();\n"
                            code_string += f"            context.setState(new {transition['to'].name}());\n"
                        else:
                            code_string += f"            context.setState(new {transition['to'].name}());\n"
                    code_string += f"        }}\n"
            code_string += f"    }}\n"
            code_string += f"}}\n\n"

        code_string += """public class Context {
        private State currentState;

        public Context() {
            // Setting initial state to the first state
            this.currentState = new """ + self.states[0].name + """();
        }

        public void setState(State state) {
            this.currentState = state;
        }

        public void handleEvent() {
            // Delegating event handling to the current state
            this.currentState.handleEvent(this);
        }
    }

    public class Main {
        public static void main(String[] args) {
            Context context = new Context();
            for (int i = 0; i < """ + str(len(self.transitions)) + """; i++) {
                context.handleEvent();
            }
        }
    }"""

        with open("GeneratedCode.java", "w") as file:
            file.write(code_string)