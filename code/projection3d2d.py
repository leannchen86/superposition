from manim import Scene, Arrow, Axes, FadeIn, GrowArrow, MathTex, ORIGIN, YELLOW, BLUE, PURPLE, RED, WHITE, DOWN, RIGHT, LEFT, UR, Indicate
import numpy as np

class SuperpositionHeadToTail(Scene):
    def construct(self):
        # ---- data ----
        # feature directions = columns of W (shown faint gray)
        w1 = np.array([1.0, 0.0, 0.0])
        w2 = np.array([0.0, 1.0, 0.0])
        w3 = np.array([0.5, 0.5, 0.0])

        # input activations
        a1, a2, a3 = 0.3, 0.7, 0.6

        # scaled contributions (2D with z=0)
        c1 = a1 * w1                       # [0.3, 0.0]
        c2 = a2 * w2                       # [0.0, 0.7]
        c3 = a3 * w3                       # [0.3, 0.3]
        y  = c1 + c2 + c3                  # [0.6, 1.0]

        # ---- helpers ----
        def make_arrow(start, vec, color, width=6, opacity=1.0):
            return Arrow(
                start=start,
                end=start + vec,
                buff=0,
                stroke_width=width,
                max_tip_length_to_length_ratio=0.15,
                tip_length=0.15,
                color=color,
                stroke_opacity=opacity,
                fill_opacity=opacity
            )

        def mid_label(text, start, vec, color=WHITE, dy=0.08):
            lbl = MathTex(text).scale(0.6).set_color(color)
            lbl.move_to(start + 0.5*vec + np.array([0, dy, 0]))
            return lbl

        # ---- axes / frame ----
        axes = Axes(
            x_range=[-0.1, 1.3, 0.2],
            y_range=[-0.1, 1.3, 0.2],
            x_length=6, y_length=6,
            axis_config=dict(include_numbers=False, include_ticks=False),
            tips=True,
        ).to_corner(ORIGIN)
        self.play(FadeIn(axes))

        # origin in axes coords
        O = axes.coords_to_point(0, 0)

        # convenience to map vecs from data space to screen
        def P(v):
            return axes.coords_to_point(v[0], v[1])

        # ---- head-to-tail contributions ----
        # 1) yellow: 0.3 * w1 from origin
        a_yellow = make_arrow(O, P(c1) - O, YELLOW, width=6)
        lab_yellow = mid_label(r"0.3\,w_1", O, P(c1) - O, color=YELLOW, dy=-0.08)
        lab_yellow.next_to(a_yellow, DOWN, buff=0.2)
        self.play(GrowArrow(a_yellow), FadeIn(lab_yellow))
        self.wait(0.1)

        # 2) blue: 0.7 * w2 starting at head of yellow
        start_blue = P([c1[0], c1[1], 0])
        a_blue   = make_arrow(start_blue, P(c2) - O, BLUE, width=6)
        lab_blue = mid_label(r"0.7\,w_2", start_blue, P(c2) - O, color=BLUE, dy=0.10)
        lab_blue.next_to(a_blue, RIGHT, buff=0.2)
        self.play(GrowArrow(a_blue), FadeIn(lab_blue))
        self.wait(0.1)

        # 3) purple: 0.6 * w3 starting at head of (blue+blue)
        start_purple = P([c1[0] + c2[0], c1[1] + c2[1], 0])
        a_purple = make_arrow(start_purple, P(c3) - O, PURPLE, width=6)
        lab_purple = mid_label(r"0.6\,w_3", start_purple, P(c3) - O, color=PURPLE, dy=0.08)
        lab_purple.next_to(a_purple, LEFT, buff=0.2)
        self.play(GrowArrow(a_purple), FadeIn(lab_purple))
        self.wait(0.2)

        # ---- resultant y from origin ----
        a_red = make_arrow(O, P(y) - O, RED, width=8)
        lab_red = MathTex(r"pre-activation\;vector=[0.6,\;1.0]").set_color(RED).scale(0.7)
        lab_red.next_to(P(y), UR, buff=0.2)
        self.play(GrowArrow(a_red))
        self.play(FadeIn(lab_red))
        self.wait(0.6)

        # optional: pulse highlight
        self.play(Indicate(a_red, scale_factor=1.03), run_time=1.0)
        self.wait(0.6)
