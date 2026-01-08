from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Introduction to Limits
        intro_title = Text("Introduction to Limits", font_size=48, color=BLUE)
        intro_title.to_edge(UP)
        self.play(FadeIn(intro_title))
        self.wait()

        axes = Axes(x_range=[-5, 5, 1], y_range=[-3, 3, 1])
        parabola = axes.plot(lambda x: x**2, x_range=[-3, 3], color=BLUE)
        self.play(Create(axes), Create(parabola))
        self.wait(2)

        limit_text = Text("Limit of a function", font_size=32)
        limit_text.next_to(intro_title, DOWN)
        self.play(Write(limit_text))
        self.wait()

        self.play(FadeOut(intro_title), FadeOut(limit_text), FadeOut(axes), FadeOut(parabola))
        self.wait()

        # Visualizing Continuity
        continuity_title = Text("Visualizing Continuity", font_size=48, color=BLUE)
        continuity_title.to_edge(UP)
        self.play(FadeIn(continuity_title))
        self.wait()

        continuous_curve = axes.plot(lambda x: x**2, x_range=[-3, 3], color=GREEN)
        self.play(Create(axes), Create(continuous_curve))
        self.wait(2)

        pencil = Circle(radius=0.2, color=RED, fill_opacity=0.5)
        pencil.move_to([1, 0, 0])
        self.play(Create(pencil))
        self.wait()

        paper = Square(side_length=2, color=YELLOW)
        paper.move_to([0, -1, 0])
        self.play(Create(paper))
        self.wait()

        self.play(pencil.animate.shift(UP*2), run_time=2)
        self.wait()

        self.play(FadeOut(continuity_title), FadeOut(pencil), FadeOut(paper), FadeOut(axes), FadeOut(continuous_curve))
        self.wait()

        # Conditions for Continuity
        conditions_title = Text("Conditions for Continuity", font_size=48, color=BLUE)
        conditions_title.to_edge(UP)
        self.play(FadeIn(conditions_title))
        self.wait()

        limit_text = Text("Limit exists", font_size=32)
        limit_text.next_to(conditions_title, DOWN)
        self.play(Write(limit_text))
        self.wait()

        function_text = Text("Function is defined", font_size=32)
        function_text.next_to(limit_text, DOWN)
        self.play(Write(function_text))
        self.wait()

        equality_sign = Text("=", font_size=48)
        equality_sign.next_to(function_text, DOWN)
        self.play(Write(equality_sign))
        self.wait()

        self.play(FadeOut(conditions_title), FadeOut(limit_text), FadeOut(function_text), FadeOut(equality_sign))
        self.wait()