from manim import *


class VectorsNotEqual(Scene):
    def construct(self):
        # Show the inequality equation x ≠ x̂ at the origin
        inequality_equation = MathTex(r"x \neq \hat{x}", font_size=48, color=WHITE)
        inequality_equation.move_to(ORIGIN)
        
        self.play(FadeIn(inequality_equation), run_time=1.0)
        self.wait(2.0)