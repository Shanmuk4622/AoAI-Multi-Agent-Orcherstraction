from manim import *

class IntroductionToLimits(Scene):
    def construct(self):
        title = Text("Introduction to Limits", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(FadeIn(title))
        self.wait()

        graph = Graph()
        function_curve = FunctionCurve(lambda x: x**2, x_range=[-3, 3], color=BLUE)
        self.play(Create(graph), Create(function_curve))
        self.wait(2)

        text = Text("As x approaches a certain value, the function approaches a limit.", font_size=32)
        text.next_to(title, DOWN)
        self.play(Write(text))
        self.wait(2)

        self.play(FadeOut(title), FadeOut(text), FadeOut(graph), FadeOut(function_curve))
        self.wait()

class VisualizingContinuity(Scene):
    def construct(self):
        continuous_curve = ContinuousCurve(lambda x: x**2, x_range=[-3, 3], color=BLUE)
        self.play(Create(continuous_curve))
        self.wait(2)

        pencil = Pencil()
        pencil.next_to(continuous_curve, UP)
        self.play(Create(pencil))
        self.wait()

        gap_in_graph = GapInGraph()
        gap_in_graph.next_to(continuous_curve, DOWN)
        self.play(Create(gap_in_graph))
        self.wait(2)

        self.play(FadeOut(pencil), FadeOut(gap_in_graph), FadeOut(continuous_curve))
        self.wait()

class ContinuityAtAPoint(Scene):
    def construct(self):
        point_on_graph = PointOnGraph()
        point_on_graph.to_edge(UP)
        self.play(Create(point_on_graph))
        self.wait()

        limit_value = LimitValue()
        limit_value.next_to(point_on_graph, DOWN)
        self.play(Create(limit_value))
        self.wait()

        function_value = FunctionValue()
        function_value.next_to(limit_value, DOWN)
        self.play(Create(function_value))
        self.wait(2)

        self.play(FadeOut(point_on_graph), FadeOut(limit_value), FadeOut(function_value))
        self.wait()

class GeneratedScene(Scene):
    def construct(self):
        self.play(FadeIn(IntroductionToLimits()))
        self.wait(5)
        self.play(FadeOut(IntroductionToLimits()))
        self.wait()

        self.play(FadeIn(VisualizingContinuity()))
        self.wait(5)
        self.play(FadeOut(VisualizingContinuity()))
        self.wait()

        self.play(FadeIn(ContinuityAtAPoint()))
        self.wait(5)
        self.play(FadeOut(ContinuityAtAPoint()))
        self.wait()