class Attribute:
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.type} {self.name} {self.value}"