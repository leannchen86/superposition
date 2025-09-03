from manim import Scene, Tex, Write, FadeOut, ORIGIN, WHITE

class QuestionText(Scene):
    def construct(self):
        # Create the rule text using Tex
        txt = Tex(r"...but with tradeoffs", font_size=60, color=WHITE)
        
        # Position the text in the center
        txt.move_to(ORIGIN)
        
        # Add the text to the scene with a simple animation
        self.play(Write(txt), run_time=1)

        self.play(FadeOut(txt), run_time=0.8)