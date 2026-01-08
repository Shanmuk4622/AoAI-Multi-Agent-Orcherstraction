from manim import *

class TestAnimation(Scene):
    def construct(self):
        # Create circle and square
        circle = Circle(color=BLUE, fill_opacity=0.5)
        square = Square(color=RED, fill_opacity=0.5)
        
        # Show them
        self.play(Create(circle))
        self.wait(1)
        self.play(Transform(circle, square))
        self.wait(2)
# "cd ..; .\.venv\Scripts\python.exe -m manim -pql .\aoai\storage\outputs\scene.py GeneratedScene"