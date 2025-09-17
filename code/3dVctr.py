from manim import *
import numpy as np


class VectorProjection3Dto2D(ThreeDScene):
    def construct(self):
        # Match 3D space (grid, axes, vertical lines, camera) from what_is_a_feature.py
        start_distance = 8.0
        self.set_camera_orientation(phi=85 * DEGREES, theta=30 * DEGREES, distance=start_distance, zoom=1.5)

        grid = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={"include_numbers": False},
        )

        vertical_lines = VGroup(
            *[
                Line(
                    start=grid.c2p(x, y, 0),
                    end=grid.c2p(x, y, 5),
                    color=BLUE_E,
                    stroke_width=1,
                    stroke_opacity=0.5,
                )
                for x in range(-5, 6)
                for y in range(-5, 6)
            ]
        )

        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(0, 5, 1),
            x_length=10,
            y_length=10,
            z_length=5,
            axis_config={"color": WHITE, "include_tip": False, "include_numbers": False},
        )

        # Add static elements to match the reference scene
        self.add(grid, vertical_lines, axes)

        # Render the [0.3, 0.7, 0.6] vector like a feature vector (normalized, length 2)
        raw_vector = np.array([0.3, 0.7, 0.6])
        normalized_direction = raw_vector / np.linalg.norm(raw_vector)
        vector_length = 2.0
        end_point = normalized_direction * vector_length

        feature_vector_arrow = Arrow3D(start=ORIGIN, end=end_point, color=RED)
        
        # Add vector label for the red 3D arrow
        vector_label = MathTex(r"x = \begin{bmatrix} 0.3 \\ 0.7 \\ 0.6 \end{bmatrix}", font_size=36, color=WHITE)
        vector_label.next_to(feature_vector_arrow.get_end(), LEFT*3.0 + DOWN*0.9, buff=0.8)
        
        self.play(FadeIn(feature_vector_arrow), run_time=0.8)
        self.add_fixed_orientation_mobjects(vector_label)
        self.play(FadeIn(vector_label), run_time=0.8)
        self.wait(1.0)

        # Projection to the xy-plane (z = 0)
        proj_end_point = np.array([end_point[0], end_point[1], 0.0])

        # Dashed connector from 3D tip to its projection on the plane
        projection_line = DashedLine(end_point, proj_end_point, color=YELLOW, dash_length=0.1)
        
        # Add equation h = W*x when projection line appears
        projection_equation = MathTex(r"W \cdot x", font_size=36, color=WHITE)
        projection_equation.next_to(projection_line.get_center(), LEFT*0.2 + UP*0.5, buff=0.8)
        
        self.play(FadeIn(projection_line), run_time=0.6)
        self.add_fixed_orientation_mobjects(projection_equation)
        self.play(FadeIn(projection_equation), run_time=0.8)

        # 2D projected vector on the xy-plane (2D Arrow like in VectorOrthogonality)
        projected_vector_arrow = Arrow(ORIGIN, proj_end_point, color=BLUE, buff=0, stroke_width=4)
        self.play(FadeIn(projected_vector_arrow), run_time=0.8)
        self.wait(0.8)

        # Fade out 3D elements and emphasize only the blue 2D vector and axes
        background_elements = VGroup(grid, vertical_lines, projection_line)
        self.play(
            background_elements.animate.set_opacity(0.1),
            FadeOut(feature_vector_arrow),
            FadeOut(vector_label),
            FadeOut(projection_equation),
            run_time=0.5
        )

        focus_center = 0.5 * proj_end_point
        self.move_camera(
            phi=0 * DEGREES,     # top-down view onto xy-plane
            theta=0 * DEGREES,   # keep x to the right (0°), y up (90°)
            gamma=0 * DEGREES,   # no roll
            frame_center=focus_center,
            distance=start_distance / 3,
            run_time=1.5,
        )
        self.wait(0.8)

        # Additional zoom-in similar to frame.scale(0.7) (use 0.5 for stronger zoom)
        # Add a tiny Wait so Scene.play always has an animation even if no camera diff is detected
        self.move_camera(distance=(start_distance / 3) * 0.7, added_anims=[Wait(0.001)], run_time=0.8)
        
        # Show the 2D result equation
        result_equation = MathTex(r"h = \begin{bmatrix} 0.6 \\ 1.0 \end{bmatrix}", font_size=36, color=WHITE)
        result_equation.next_to(projected_vector_arrow.get_end(), UP, buff=0.3)
        
        self.add_fixed_orientation_mobjects(result_equation)
        self.play(FadeIn(result_equation), run_time=0.8)
        self.wait(2)