from manim import *

class MatrixW(Scene):
    def construct(self):
        # Define the matrix W with consistent number formatting for equal spacing
        W = Matrix([
            ["1.0", "0.0", "0.5"],
            ["0.0", "1.0", "0.5"]
        ])
        
        # Add a label for the matrix
        W_label = MathTex("W = ").next_to(W, LEFT)
        
        # Group the label and matrix together
        matrix_group = VGroup(W_label, W)
        
        # Center the group on the screen
        matrix_group.move_to(ORIGIN)
        
        # Animate the matrix appearing
        self.play(Write(W_label), Create(W))
        
        # Keep it on screen for a moment
        self.wait(5)
        
        text_list = ["furry", "loyal", "golden"]
        # emphasis each column of the matrix one by one
        # first, emphasize the first vertical column, the 2 numbers scale up simultaneously, and then the second vertical column
        entries = W.get_entries()
        for i in range(3):  # 3 columns in the matrix
            emphasized_group = VGroup(entries[i], entries[i + 3])
            other_groups = [VGroup(entries[j], entries[j + 3]) for j in range(3) if j != i]

            # Emphasize current column while dimming others simultaneously
            self.play(
                emphasized_group.animate.scale(1.2).set_color(YELLOW),
                *[g.animate.set_opacity(0.3) for g in other_groups],
                run_time=0.6
            )

            # Create arrow just below the column, centered under both numbers
            start_point = emphasized_group.get_bottom() + DOWN * 0.2
            end_point = emphasized_group.get_bottom() + DOWN * 0.8
            arrow = Arrow(
                start=start_point,
                end=end_point,
                buff=0,
                color=WHITE,
                stroke_width=2
            )
            self.play(Create(arrow), run_time=0.4)

            # Label for the arrow, placed below the arrow
            arrow_label = Tex(text_list[i]).next_to(arrow, DOWN, buff=0.15)
            self.play(Write(arrow_label), run_time=0.3)

            self.wait(0.5)

            # Revert emphasis and dimming; remove arrow and label
            self.play(
                emphasized_group.animate.scale(1/1.2).set_color(WHITE),
                *[g.animate.set_opacity(1.0) for g in other_groups],
                FadeOut(arrow),
                FadeOut(arrow_label),
                run_time=0.6
            )
