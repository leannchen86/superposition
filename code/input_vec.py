from manim import *
import numpy as np

class InputVectorVisualization(Scene):
    def construct(self):
        # Create the title
        title = Tex("input vector X =", font_size=42)
        title.to_edge(UP, buff=1)
        
        # Create the vector notation
        vector_values = MathTex(r"\begin{bmatrix} 0.3 \\ 0.7 \\ 0.6 \end{bmatrix}", font_size=42)
        vector_values.next_to(title, RIGHT, buff=0.3)
        
        # Alternative: Show as row vector with proper spacing
        row_vector = MathTex(r"[", r"0.3", r"\quad", r"0.7", r"\quad", r"0.6", r"]", font_size=42)
        row_vector.next_to(title, RIGHT, buff=0.3)
        
        # Group and position the header + vector first, then compute anchors
        input_vec = VGroup(title, row_vector).move_to(ORIGIN)
        
        # Helper to make a strictly vertical, centered arrow under a given MathTex number
        def arrow_under(mobj: Mobject, start_offset: float = 0.1, length: float = 1.2) -> Arrow:
            x_center = mobj.get_center()[0]
            y_bottom = mobj.get_bottom()[1]
            start = np.array([x_center, y_bottom - start_offset, 0.0])
            #make the arrow shorter
            end = np.array([x_center, y_bottom - length, 0.0])
            return Arrow(
                start=start,
                end=end,
                buff=0,
                color=WHITE,
                stroke_width=1.5,
            )

        # Create arrows pointing down from each value (exactly under each number)
        arrow1 = arrow_under(row_vector[1])
        arrow2 = arrow_under(row_vector[3])
        arrow3 = arrow_under(row_vector[5])
        arrows = VGroup(arrow1, arrow2, arrow3)

        # Create labels with quotes to match the handwritten style
        label1 = Tex('furry', font_size=32)
        label1.next_to(arrow1.get_end(), DOWN, buff=0.4)
        
        label2 = Tex('loyal', font_size=32)
        label2.next_to(arrow2.get_end(), DOWN, buff=0.4)
        
        label3 = Tex('golden', font_size=32)
        label3.next_to(arrow3.get_end(), DOWN, buff=0.4)
        
        # Animation sequence
        self.play(Write(input_vec))
        self.wait(0.5)

        labels = VGroup(label1, label2, label3)
        
        # Animate each arrow growing, followed by its label
        for arrow, label in zip(arrows, labels):
            self.play(GrowArrow(arrow), run_time=1.5)
            self.play(FadeIn(label), run_time=0.5)
            self.wait(0.3)