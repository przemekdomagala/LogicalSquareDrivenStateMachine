class Attribute:
    def __init__(self, name, value):
        self.name = name
        self.value = value

        # if value["kind"] == "Value":
        #     self.type = str(type(value["value"])).replace('<class \'', '').replace('\'>', '')
        # else:
        #     self.type = str(type(1.025)).replace('<class \'', '').replace('\'>', '')

    def __str__(self):
        return f"{self.name} {self.value}"