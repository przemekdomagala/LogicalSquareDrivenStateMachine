class CodeGenerator:
    def __init__(self):
        self.code = ""
    
    def generate_code(self, graph):
        self.print_nested_dict(graph)

    def print_nested_dict(self, d, indent=0):
        """Recursively prints a nested dictionary."""
        for key, value in d.items():
            if isinstance(value, dict):  # Check if the value is a dictionary
                print("  " * indent + f"{key}:")
                self.print_nested_dict(value, indent + 1)  # Recursively call the function
            else:
                print("  " * indent + f"{key}: {value}")
