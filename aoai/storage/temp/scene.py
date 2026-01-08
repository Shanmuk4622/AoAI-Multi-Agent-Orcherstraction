from manim import *

class GeneratedScene(Scene):
    def construct(self):
        text1 = Text("Introduction to Circle")
        dot1 = Dot()
        self.play(FadeIn(text1), FadeIn(dot1))
        self.wait()

        line1 = Line()
        dot2 = Dot()
        text2 = Text("Defining Radius")
        self.play(Create(line1), FadeIn(dot2), Write(text2))
        self.wait()

        circle1 = Circle()
        dot3 = Dot()
        text3 = Text("Drawing the Circle")
        self.play(Create(circle1), Transform(dot2, dot3), Write(text3))
        self.wait()