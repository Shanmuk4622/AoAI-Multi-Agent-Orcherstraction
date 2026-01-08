from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Introduction to Derivatives
        axes = Axes().to_edge(UP)
        self.play(Create(axes))
        self.wait()
        
        func_graph = axes.plot(lambda x: x**2, x_range=[-10, 10], color=BLUE)
        self.play(Create(func_graph))
        self.wait()
        
        tangent_line = axes.get_tangent_line(func_graph, 2)
        self.play(Create(tangent_line))
        self.wait()
        
        intro_text = Text("Introduction to Derivatives", font_size=36).to_edge(UP)
        self.play(Write(intro_text))
        self.wait()
        
        self.play(FadeOut(intro_text))
        self.wait()
        
        # Visualizing Derivative as Slope
        text_obj = Text("Derivative as Slope", font_size=36).to_edge(UP)
        self.play(Write(text_obj))
        self.wait()
        
        arrow = Arrow(LEFT, RIGHT, color=YELLOW).next_to(text_obj, DOWN)
        self.play(Create(arrow))
        self.wait()
        
        tangent_line_2 = axes.get_tangent_line(func_graph, 3)
        self.play(Create(tangent_line_2))
        self.wait()
        
        self.play(Transform(tangent_line_2, tangent_line))
        self.wait()
        
        self.play(FadeOut(text_obj), FadeOut(arrow), FadeOut(tangent_line_2))
        self.wait()
        
        # Calculating Derivative
        secant_line = Line(axes.coords_to_point(-5, 0), axes.coords_to_point(5, 0), color=RED)
        self.play(Create(secant_line))
        self.wait()
        
        dot = Dot(axes.coords_to_point(0, 0), color=GREEN)
        self.play(Create(dot))
        self.wait()
        
        func_graph_2 = axes.plot(lambda x: x**2, x_range=[-10, 10], color=BLUE)
        self.play(Create(func_graph_2))
        self.wait()
        
        self.play(Transform(secant_line, tangent_line))
        self.wait()
        
        self.play(FadeOut(secant_line), FadeOut(dot), FadeOut(func_graph_2))
        self.wait()