from manim import *

class StrawRule(Scene):
    def construct(self):
        # Create the rule text using Tex
        rule_text = Tex(r"Rule: No two straws can point in the same direction.", font_size=48, color=WHITE)
        
        # Position the text in the center
        rule_text.move_to(ORIGIN)
        
        # Add the text to the scene with a simple animation
        self.play(Write(rule_text), run_time=2)
        
        # Hold the text on screen for a moment
        self.wait(2)

        self.play(FadeOut(rule_text), run_time=0.8)