from manim import *

class CosineSimilarityRotation(Scene):
    def construct(self):
        import numpy as np

        # ── 1. Axes ────────────────────────────────────────────────────────────────
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_numbers": False},
        ).to_corner(LEFT + DOWN)  # keep plenty of empty canvas on the right

        # ── 2. helper that builds arrow + dotted drop + highlight ────────────────
        arrow_len = 3

        def vector_group(angle_deg: float) -> VGroup:
            θ = angle_deg * DEGREES
            tip = np.array([np.cos(θ), np.sin(θ), 0]) * arrow_len

            arrow = Arrow(ORIGIN, tip, buff=0, stroke_width=8)
            drop  = DashedLine(tip, np.array([tip[0], 0, 0]), dash_length=0.1)
            proj  = Line(ORIGIN, np.array([tip[0], 0, 0]),
                         color=BLUE_E, stroke_width=8, z_index=-1)

            return VGroup(arrow, drop, proj)

        # ── 3. intro frame ────────────────────────────────────────────────────────
        group = vector_group(0)             # vector along +x
        self.play(FadeIn(axes, group))
        self.wait(0.5)

        # ── 4. rotate through 18° steps up to 90° ────────────────────────────────
        for ang in (18, 36, 54, 72, 90):
            new_group = vector_group(ang)
            self.play(Transform(group, new_group), run_time=1)
            self.wait(0.25)

        # ── 5. outro ─────────────────────────────────────────────────────────────
        self.play(FadeOut(axes), FadeOut(group))
