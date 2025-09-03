from manim import Scene, Tex, Write, FadeOut, ORIGIN, WHITE

class QuestionText(Scene):
    def construct(self):
        # Create the rule text using Tex
        text = Tex(r"Superposition", font_size=72, color=WHITE)
        
        # Position the text in the center
        text.move_to(ORIGIN)
        
        # Add the text to the scene with a simple animation
        self.play(Write(text), run_time=2)
        
        # Hold the text on screen for a moment
        self.wait(2)

        self.play(FadeOut(text), run_time=0.8)