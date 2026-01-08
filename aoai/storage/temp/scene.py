import sys
import os
import subprocess

# Add Manim to the system path if it's not already installed
if 'manim' not in sys.modules:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "manim"])

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Introduction to Quadratic Equations
        intro_text = Text("Introduction to Quadratic Equations", font_size=36)
        intro_axes = Axes(
            x_range=[-10, 10, 2],
            y_range=[-10, 10, 2],
            x_length=10,
            y_length=6,
            axis_config={"include_tip": False},
        )
        self.play(FadeIn(intro_text))
        self.play(Create(intro_axes))
        self.play(Write(intro_text))
        self.wait()

        # Visualizing the Parabola
        parabola = intro_axes.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE)
        dot = Dot().move_to(intro_axes.coords_to_point(0, 0))
        self.play(Create(parabola))
        self.play(Create(dot))
        self.play(dot.animate.shift(UP * 2))
        self.play(Transform(dot, Dot().move_to(intro_axes.coords_to_point(2, 4))))
        self.wait()

        # Axis of Symmetry
        axis_line = Line(intro_axes.coords_to_point(-3, 0), intro_axes.coords_to_point(3, 0), color=YELLOW)
        axis_text = Text("Axis of Symmetry", font_size=36).next_to(axis_line, DOWN)
        self.play(Create(axis_line))
        self.play(Write(axis_text))
        self.play(axis_line.animate.shift(UP * 2))
        self.play(Transform(axis_line, Line(intro_axes.coords_to_point(-3, 2), intro_axes.coords_to_point(3, 2), color=YELLOW)))
        self.wait()

        # Conclusion
        conclusion_text = Text("Conclusion", font_size=36)
        conclusion_parabola = intro_axes.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE)
        self.play(FadeOut(intro_text))
        self.play(FadeOut(axis_line))
        self.play(FadeOut(axis_text))
        self.play(FadeOut(parabola))
        self.play(FadeOut(dot))
        self.play(FadeIn(conclusion_text))
        self.play(Create(conclusion_parabola))
        self.play(Transform(conclusion_parabola, intro_axes.plot(lambda x: x**2 + 1, x_range=[-3, 3], color=BLUE)))
        self.play(FadeOut(conclusion_text))
        self.play(FadeOut(conclusion_parabola))