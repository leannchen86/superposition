from manim import (
    Scene,
    Matrix,
    MathTex,
    VGroup,
    ORIGIN,
    Write,
    Create,
    Axes,
    WHITE,
    RIGHT,
    LEFT,
    DOWN,
    UR,
    DR,
    Arrow,
    BLUE,
    PURPLE,
    GrowArrow,
    Tex,
    FadeOut,
    YELLOW,
)

class MatrixW(Scene):
    def construct(self):
        # Define the matrix W with consistent number formatting for equal spacing
        W = Matrix([
            ["1.0", "0.0", "0.5"],
            ["0.0", "1.0", "0.5"]
        ]).scale(0.9)
        
        # Add a label for the matrix
        W_label = MathTex("W = ", font_size=42).next_to(W, LEFT)
        
        # Group the label and matrix together
        matrix_group = VGroup(W_label, W)
        
        # Center the group on the screen
        matrix_group.move_to(ORIGIN)

        # --- Begin integrated 2D features animation (adapted from 2d_features.py) ---
        axes = Axes(
            x_range=[-0.5, 1.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            x_length=7,
            y_length=7,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "include_ticks": False,
            },
            tips=True,
        )
        # Place axes more towards the middle
        axes.move_to(RIGHT * 2.5)

        # Define points
        w1_coords = axes.coords_to_point(1, 0)
        w2_coords = axes.coords_to_point(0, 1)
        w3_coords = axes.coords_to_point(0.5, 0.5)
        origin = axes.coords_to_point(0, 0)

        # Labels for points
        w1_label = (
            MathTex("W_1(1, 0)", color=WHITE, font_size=32)
            .next_to(w1_coords, DOWN, buff=0.2)
            .set_z_index(10)
        )
        w2_label = (
            MathTex("W_2(0, 1)", color=WHITE, font_size=32)
            .next_to(w2_coords, LEFT, buff=0.2)
            .set_z_index(10)
        )
        w3_label = (
            MathTex("W_3(0.5, 0.5)", color=WHITE, font_size=32)
            .next_to(w3_coords, UR, buff=0.2)
            .set_z_index(10)
        )

        # Arrows from origin to W1, W2, and W3
        arrow_to_w1 = Arrow(
            origin,
            w1_coords,
            color=YELLOW,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_to_w2 = Arrow(
            origin,
            w2_coords,
            color=BLUE,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_to_w3 = Arrow(
            origin,
            w3_coords,
            color=PURPLE,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        # --- End integrated 2D features animation ---
        
        w_labels = VGroup(w1_label, w2_label, w3_label)
        w_arrows = VGroup(arrow_to_w1, arrow_to_w2, arrow_to_w3)
        entries = W.get_entries()
        
        # Create feature description texts
        feature_texts = [
            Tex("direction of feature ‘golden’", font_size=32, color=YELLOW).next_to(w1_coords, DOWN, buff=0.8),
            Tex("direction of feature ‘loyal’", font_size=32, color=BLUE).next_to(w2_coords, RIGHT*0.4 + DOWN*0.2, buff=0.8),
            Tex("direction of feature ‘furry’", font_size=32, color=PURPLE).next_to(w3_coords, DOWN + RIGHT * 0.2, buff=0.8)
        ]

        # Animation sequence - all self.play calls at the end
        # Animate the matrix appearing
        self.play(Write(W_label), Create(W))
        
        # Keep it on screen for a moment
        self.wait(1)

        # Move the matrix group to the left to make room for the 2D features animation
        self.play(matrix_group.animate.to_edge(LEFT, buff=0.8))
        self.wait(0.2)

        # Play the 2D features sequence
        self.play(Create(axes), run_time=1.2)

        col_colors = [YELLOW, BLUE, PURPLE]

        for i in range(3):  # 3 columns in the matrix
            emphasized_group = VGroup(entries[i], entries[i + 3])
            other_groups = [VGroup(entries[j], entries[j + 3]) for j in range(3) if j != i]

            # Emphasize current column, dim others, and show corresponding 2D arrow/label
            self.play(
                emphasized_group.animate.scale(1.2).set_color(col_colors[i]),
                *[g.animate.set_opacity(0.3) for g in other_groups],
                GrowArrow(w_arrows[i]),
                Write(w_labels[i]),
                run_time=0.8,
            )
            
            # Quick fade in and out of feature description
            self.play(
                Write(feature_texts[i]),
                run_time=0.8
            )
            self.wait(1)
            # Fade out feature text while reverting emphasis and dimming simultaneously
            self.play(
                FadeOut(feature_texts[i]),
                emphasized_group.animate.scale(1/1.2).set_color(col_colors[i]),
                *[g.animate.set_opacity(1.0) for g in other_groups],
                run_time=0.8,
            )