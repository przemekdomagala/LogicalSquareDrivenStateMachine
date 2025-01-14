from kivy.graphics import Line, Color
from kivy.uix.widget import Widget

class SquareWidget(Widget):
    def __init__(self, **kwargs):
        super(SquareWidget, self).__init__(**kwargs)
        self.bind(size=self.update_square, pos=self.update_square)

    def update_square(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.8, 0.8, 0.8, 1)
            size = min(self.width, self.height) * 0.5
            x = self.x + (self.width - size) / 2
            y = self.y + (self.height - size) / 2
            self.square = Line(rectangle=(x, y, size, size), width=2)