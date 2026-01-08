from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Scene 1: Introduction
        text1 = Text("Introduction to Circle", font_size=36)
        self.play(Write(text1))
        self.wait()
        self.play(FadeOut(text1))
        
        # Scene 2: Defining Radius
        text2 = Text("Defining Radius", font_size=36).to_edge(UP)
        center_dot = Dot(ORIGIN, color=RED)
        radius_line = Line(ORIGIN, RIGHT * 2, color=YELLOW)
        radius_label = Text("r", font_size=24, color=YELLOW).next_to(radius_line, DOWN)
        
        self.play(Write(text2))
        self.play(Create(center_dot))
        self.play(Create(radius_line), Write(radius_label))
        self.wait()
        
        # Scene 3: Drawing the Circle
        text3 = Text("Drawing the Circle", font_size=36).to_edge(UP)
        circle = Circle(radius=2, color=BLUE)
        
        self.play(Transform(text2, text3))
        self.play(Create(circle))
        self.wait()
        
        # Final view with all elements
        self.play(
            radius_line.animate.rotate(PI/4),
            radius_label.animate.move_to(radius_line.get_center() + UP * 0.3)
        )
        self.wait(2)