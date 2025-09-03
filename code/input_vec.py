from manim import *
import numpy as np

class InputVectorVisualization(Scene):
    def construct(self):
        # Create the title
        toy_emb_txt = Tex("Toy embedding for the word ‘dog’", font_size=60, color=WHITE).move_to(ORIGIN)
        
        title = Tex("input vector X =", font_size=50).move_to(ORIGIN)
        
        # Create the vector notation
        vector_values = MathTex(r"\begin{bmatrix} 0.3 \\ 0.7 \\ 0.6 \end{bmatrix}", font_size=50)
        vector_values.next_to(title, RIGHT, buff=0.3)
        
        # Alternative: Show as row vector with proper spacing
        row_vector = MathTex(r"[", r"0.3", r"\quad", r"0.7", r"\quad", r"0.6", r"]", font_size=50)
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
        label1 = Tex('golden', font_size=40, color=YELLOW)
        label1.next_to(arrow1.get_end(), DOWN, buff=0.4)
        
        label2 = Tex('loyal', font_size=40, color=BLUE)
        label2.next_to(arrow2.get_end(), DOWN, buff=0.4)
        
        label3 = Tex('furry', font_size=40, color=PURPLE)
        label3.next_to(arrow3.get_end(), DOWN, buff=0.4)
        
        labels = VGroup(label1, label2, label3)
        
        self.play(Write(toy_emb_txt))
        self.play(toy_emb_txt.animate.shift(UP * 1.2))
        self.play(Write(input_vec))
        self.play(FadeOut(toy_emb_txt))
        self.wait(1)
        
        # Animate each arrow growing, followed by its label
        for arrow, label in zip(arrows, labels):
            self.play(GrowArrow(arrow), run_time=1.5)
            self.play(FadeIn(label), run_time=0.5)
            self.wait(0.3)
        
        self.play(FadeOut(input_vec, labels, arrows))