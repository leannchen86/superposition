from manim import Scene, Tex, Write, FadeOut, ORIGIN, WHITE

class QuestionText(Scene):
    def construct(self):
        # Create the rule text using Tex
        rule_text = Tex(r"How would you do it?", font_size=60, color=WHITE)
        
        # Position the text in the center
        rule_text.move_to(ORIGIN)
        
        # Add the text to the scene with a simple animation
        self.play(Write(rule_text), run_time=2)
        
        # Hold the text on screen for a moment
        self.wait(2)

        self.play(FadeOut(rule_text), run_time=0.8)