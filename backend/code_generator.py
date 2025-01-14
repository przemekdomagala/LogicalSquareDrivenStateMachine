class CodeGenerator:
    def __init__(self):
        self.code = ""
    
    def generate_code(self, graph):
        self.print_nested_dict(graph)

    def print_nested_dict(self, d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):  
                print("  " * indent + f"{key}:")
                self.print_nested_dict(value, indent + 1)
            else:
                print("  " * indent + f"{key}: {value}")
