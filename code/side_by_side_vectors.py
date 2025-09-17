from manim import (
    Scene,
    Axes,
    Arrow,
    VGroup,
    MathTex,
    Tex,
    Angle,
    ORIGIN,
    RIGHT,
    UP,
    UR,
    WHITE,
    GREY,
    YELLOW,
    BLUE,
    PURPLE,
    RED,
    GREEN,
    Create,
    FadeIn,
    Write,
    FadeOut,
    config,
)
import numpy as np

# Define GREY if only GRAY exists in this Manim build
try:
    GREY
except NameError:
    try:
        GREY = GRAY  # type: ignore[name-defined]
    except Exception:
        pass


class SideBySideVectors(Scene):
    def construct(self):
        left_group, left_axes, left_arrows = self._build_left_chart_from_matrix_w()
        right_group, right_axes, right_arrows = self._build_right_chart_three_vectors_120()

        # Ensure equal visual space for each chart
        target_width = (config.frame_width - 2.0) / 2.0
        left_group.scale_to_fit_width(target_width)
        right_group.scale_to_fit_width(target_width)

        # Position independently on left and right halves BEFORE creating them
        left_center = np.array([-config.frame_width / 4.0, 0.0, 0.0])
        right_center = np.array([config.frame_width / 4.0 - 0.5, 0.0, 0.0])

        left_group.move_to(left_center)
        right_group.move_to(right_center)

        # Create in-place (no overlap at origin) with original colors
        self.play(FadeIn(left_axes), *[Create(a) for a in left_arrows])
        self.play(FadeIn(right_axes), *[Create(a) for a in right_arrows])
        # (Arc moved to occur after scaling the RIGHT chart up, before graying out RIGHT)
        # This ensures the arc sits correctly between the two vectors in their scaled state.

        # Desired original arrow colors for restoration
        left_arrow_colors = [YELLOW, BLUE, PURPLE]
        

        # 1) Gray out LEFT while scaling RIGHT up to 1.2x
        self.play(
            left_axes.animate.set_color(GREY).set_opacity(0.35),
            *[a.animate.set_color(GREY).set_opacity(0.35) for a in left_arrows],
            right_group.animate.scale(1.2),
        )
        
        # Show 120° angle arc AFTER scaling up the RIGHT chart, BEFORE graying out RIGHT
        angle_arc = Angle(right_arrows[0], right_arrows[1], radius=0.5, other_angle=False)
        angle_label = MathTex(r"120^\circ").next_to(angle_arc, UR, buff=0.1)
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(1.0)
        self.play(FadeOut(angle_arc), FadeOut(angle_label))
        self.wait(0.4)
        # 2) Scale RIGHT back to original size WHILE graying it out (entire group for visibility)
        self.play(
            right_group.animate.set_color(GREY).set_opacity(0.35).scale(1/1.2),
        )

        # 3) Restore LEFT to original colors
        self.play(
            left_axes.animate.set_color(GREY).set_opacity(1.0),
            *[
                a.animate.set_color(c).set_opacity(1.0)
                for a, c in zip(left_arrows, left_arrow_colors)
            ],
        )
        self.wait(0.2)

    def _build_left_chart_from_matrix_w(self):
        """
        Recreates the 2D vectors from 2x3matrixW.py (W1, W2, W3) in a standalone chart.
        - Axes range and styles mirror those used in 2x3matrixW.py
        - Vectors: W1(1,0) [YELLOW], W2(0,1) [BLUE], W3(0.5,0.5) [PURPLE]
        """
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREY},
            tips=False,
        )

        # Coordinates (scaled 2x to match right chart)
        w1_coords = axes.coords_to_point(2.0, 0.0)
        w2_coords = axes.coords_to_point(0.0, 2.0)
        w3_coords = axes.coords_to_point(1.6, 1.6)
        origin = axes.coords_to_point(0.0, 0.0)

        # Arrows (match VectorOrthogonality.py style)
        def make_vec_arrow(start, end, color):
            return Arrow(
                start=start,
                end=end,
                buff=0,
                stroke_width=4,
                color=color,
            )

        arrow_to_w1 = make_vec_arrow(origin, w1_coords, YELLOW)
        arrow_to_w2 = make_vec_arrow(origin, w2_coords, BLUE)
        arrow_to_w3 = make_vec_arrow(origin, w3_coords, PURPLE)

        group = VGroup(
            axes,
            arrow_to_w1,
            arrow_to_w2,
            arrow_to_w3,
        )
        return group, axes, [arrow_to_w1, arrow_to_w2, arrow_to_w3]

    def _build_right_chart_three_vectors_120(self):
        """
        Recreates the three 2D vectors separated by 120 degrees (referencing VectorOrthogonality.py).
        - Vectors length: 2
        - Colors: RED, BLUE, GREEN (first three used in VectorOrthogonality)
        - Includes 120° angle arc like VectorOrthogonality.py
        """
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREY},
            tips=False,
        )

        angles_deg = [0, 120, 240]

        # Arrows (match VectorOrthogonality.py style)
        def make_vec_arrow(start, end, color):
            return Arrow(
                start=start,
                end=end,
                buff=0,
                stroke_width=4,
                color=color,
            )

        arrows = []
        colors = [RED, BLUE, GREEN]
        origin = axes.coords_to_point(0.0, 0.0)
        for angle_deg, color in zip(angles_deg, colors):
            angle_rad = np.deg2rad(angle_deg)
            x = 2.0 * np.cos(angle_rad)
            y = 2.0 * np.sin(angle_rad)
            end = axes.coords_to_point(x, y)
            arrows.append(make_vec_arrow(origin, end, color))

        group = VGroup(axes, *arrows)
        return group, axes, arrows


