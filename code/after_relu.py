from manim import *

class ReLUAfterVector(Scene):
    def construct(self):
        # Raw and ReLU versions matching your image
        raw_values = ["2.5", "-1.2", "0.1", "-0.4"]
        relu_values = ["2.5", "0.0", "0.1", "0.0"]

        def vector_tex(values, color_neg=RED, spacing=", \\quad"):
            # Build elements for Tex
            elements = ["\\big["]
            for i, v in enumerate(values):
                elements.append(v)
                if i < len(values) - 1:
                    elements.append(spacing)
            elements.append("\\big]")
            vec = Tex(*elements, font_size=44)
            # Color negatives
            if color_neg:
                for i, v in enumerate(values):
                    if "-" in v:
                        vec[1 + 2*i].set_color(color_neg)
            return vec

        # Create mathematical notation and vectors matching your image
        pre_activation_label = MathTex(r"W^T Wx + b", font_size=36)
        pre_activation_desc = Tex(r"(pre-activation vector)", font_size=28)
        pre_activation_colon = Tex(r"=", font_size=36)
        raw_vec = vector_tex(raw_values, color_neg=RED, spacing=", \\,")
        
        activation_label = MathTex(r"ReLU(W^T Wx + b)", font_size=36)
        activation_desc = Tex(r"(activation vector)", font_size=28)
        activation_colon = Tex(r"=", font_size=36)
        relu_vec = vector_tex(relu_values, color_neg=False, spacing=", \\;")

        # Positions - matching your image layout
        FIRST_VEC_Y = 1.5
        SECOND_VEC_Y = -0.5
        EQ_X = 0.0

        # Align equal signs at the same x position; place labels left and vectors right
        pre_activation_colon.move_to([EQ_X, FIRST_VEC_Y, 0])
        activation_colon.move_to([EQ_X, SECOND_VEC_Y, 0])

        pre_left = VGroup(pre_activation_label, pre_activation_desc)
        pre_left.arrange(RIGHT, buff=0.3)
        pre_left.next_to(pre_activation_colon, LEFT, buff=0.3)
        raw_vec.next_to(pre_activation_colon, RIGHT, buff=0.3)

        act_left = VGroup(activation_label, activation_desc)
        act_left.arrange(RIGHT, buff=0.3)
        act_left.next_to(activation_colon, LEFT, buff=0.3)
        relu_vec.next_to(activation_colon, RIGHT, buff=0.3)

        # 1) Show pre-activation vector
        self.play(
            FadeIn(pre_activation_label),
            FadeIn(pre_activation_desc),
            FadeIn(pre_activation_colon),
            FadeIn(raw_vec)
        )
        self.wait(0.8)

        # 2) ReLU transformation with arrow
        arrow1 = Arrow(
            start=[EQ_X, FIRST_VEC_Y - 0.3, 0],
            end=[EQ_X, SECOND_VEC_Y + 0.3, 0],
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.2,
            color=WHITE
        ).scale(0.8)

        # ReLU label next to arrow
        relu_label = Tex(r"ReLU", font_size=32, color=WHITE)
        relu_label.next_to(arrow1, RIGHT, buff=0.3)

        # Animate ReLU step
        self.play(
            FadeIn(arrow1),
            FadeIn(relu_label)
        )
        self.wait(0.5)
        
        self.play(
            FadeIn(activation_label),
            FadeIn(activation_desc),
            FadeIn(activation_colon),
            FadeIn(relu_vec, shift=DOWN * 0.2)
        )
        self.wait(0.8)

        # Highlight consecutive zeroes in relu_vec with a rounded rectangle
        zero_groups = []
        current_group = []
        for idx, v in enumerate(relu_values):
            if v == "0.0":
                current_group.append(idx)
            else:
                if current_group:
                    zero_groups.append(current_group)
                    current_group = []
        if current_group:
            zero_groups.append(current_group)

        highlight_rects = []
        for group in zero_groups:
            mobjects = [relu_vec[1 + 2*i] for i in group]
            rect = SurroundingRectangle(VGroup(*mobjects), color=RED, stroke_width=2, buff=0.08, corner_radius=0.1)
            highlight_rects.append(rect)
        self.play(*[Create(rect) for rect in highlight_rects])
        self.wait(0.5)
        self.play(*[rect.animate.set_stroke(width=5, color=RED) for rect in highlight_rects], run_time=0.8)
        self.play(*[rect.animate.set_stroke(width=2, color=RED) for rect in highlight_rects], run_time=0.5)
        self.wait(0.5)

        # End
        self.wait()