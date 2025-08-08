from manim import *

class LearnedConcepts(Scene):
    def construct(self):
        # 1) Create the text object using a LaTeX-style font
        sentence = Text("Where are 'feature vectors' stored in the network?", font="CMU Serif")

        # 2) Optionally, set position / scale
        sentence.scale(0.9)           # Make it a bit larger and keep centered

        # 3) Animate it
        self.play(Write(sentence), run_time=2)     # “Write-on” animation
        self.wait(2)                  # Hold for 2 s before the scene ends