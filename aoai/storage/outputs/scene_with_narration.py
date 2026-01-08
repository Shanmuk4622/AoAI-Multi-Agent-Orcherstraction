from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Scene 0: Title + Narration
        title = Text("Pythagorean Theorem", font_size=48, color=BLUE)
        narration0 = Text(
            "Welcome to the world of triangles!\nLet's explore a special one,\nthe right-angled triangle.",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(narration0))
        self.wait(5)  # Duration from narrator agent
        self.play(FadeOut(title), FadeOut(narration0))
        
        # Scene 1: Triangle with squares + Narration
        triangle = Polygon(
            [-2, -1, 0], [2, -1, 0], [2, 2, 0],
            color=WHITE, stroke_width=3
        )
        
        square_a = Square(side_length=1.5, color=YELLOW, fill_opacity=0.4).next_to(triangle, LEFT, buff=0).shift(DOWN * 0.75)
        square_b = Square(side_length=2, color=GREEN, fill_opacity=0.4).next_to(triangle, DOWN, buff=0).shift(LEFT * 1)
        square_c = Square(side_length=2.5, color=RED, fill_opacity=0.4).next_to(triangle.get_center(), UR, buff=0.5)
        
        narration1 = Text(
            "Now, imagine building squares\non each side. What do you think\nwill happen?",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Create(triangle))
        self.play(FadeIn(narration1))
        self.play(Create(square_a), Create(square_b), Create(square_c))
        self.wait(4)
        self.play(FadeOut(narration1))
        
        # Scene 2: Formula + Narration
        formula = Text("a² + b² = c²", font_size=56, color=WHITE).to_edge(UP)
        example = Text("3² + 4² = 5²\n9 + 16 = 25", font_size=36, color=GOLD).move_to(ORIGIN)
        
        narration2 = Text(
            "The secret's out! The areas are related:\na² + b² = c²",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Write(formula))
        self.play(FadeIn(narration2))
        self.wait(2)
        self.play(FadeIn(example))
        self.wait(4)
        
        # Highlight the relationship
        self.play(
            square_a.animate.set_fill(YELLOW, opacity=0.8),
            square_b.animate.set_fill(GREEN, opacity=0.8),
            square_c.animate.set_fill(RED, opacity=0.8),
        )
        self.wait(2)
