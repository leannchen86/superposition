from manim import *
import numpy as np


class VectorReconstruction2Dto3D(ThreeDScene):
    def construct(self):
        # Match 3D space (grid, axes, vertical lines, camera) from what_is_a_feature.py
        start_distance = 8.0
        self.set_camera_orientation(phi=0 * DEGREES, theta=0 * DEGREES, distance=start_distance / 3 * 0.7, zoom=1.5)

        grid = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.1,
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
                    stroke_opacity=0.1,
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

        # Add static elements (initially faded since we start in 2D view)
        self.add(grid, vertical_lines, axes)

        # Start with the 2D vector h = [0.6, 1.0] (same as the projected result)
        h_vector = np.array([0.6, 1.0, 0.0])
        projected_vector_arrow = Arrow(ORIGIN, h_vector, color=BLUE, buff=0, stroke_width=4)
        
        # Show the 2D vector and its label
        h_label = MathTex(r"h = \begin{bmatrix} 0.6 \\ 1.0 \end{bmatrix}", font_size=36, color=WHITE)
        h_label.next_to(projected_vector_arrow.get_end(), UP + RIGHT*2.0, buff=0.9)
        
        self.add(projected_vector_arrow)
        self.add_fixed_orientation_mobjects(h_label)
        self.play(FadeIn(h_label), run_time=0.8)
        self.wait(1.0)

        # Transition back to 3D view - reverse of the original animation
        focus_center = 0.5 * h_vector
        self.move_camera(
            distance=start_distance / 3,
            added_anims=[Wait(0.001)],
            run_time=0.8,
        )
        
        # Fade in the background elements and zoom out to full 3D view
        background_elements = VGroup(grid, vertical_lines)
        self.play(
            background_elements.animate.set_opacity(0.5),
            run_time=0.5
        )

        # Create target position for h_label during camera transition
        target_position = projected_vector_arrow.get_end() + UP + RIGHT*2.0
        
        self.move_camera(
            phi=80 * DEGREES,     # back to 3D view
            theta=15 * DEGREES,   
            gamma=0 * DEGREES,   # no roll
            frame_center=ORIGIN,
            distance=start_distance,
            added_anims=[h_label.animate.move_to(target_position)],
            run_time=1.5,
        )
        self.wait(0.8)

        # Calculate the reconstructed 3D vector using W^T * h = [0.6, 1.0, 0.8]
        # W = [[1, 0], [0.5, 0], [1, 0.5]], so W^T = [[1, 0.5, 1], [0, 0, 0.5]]
        # W^T * h = [[1, 0.5, 1], [0, 0, 0.5]] * [0.6, 1.0] = [0.6, 1.0, 0.8]
        reconstructed_raw = np.array([0.6, 1.0, 0.8])
        reconstructed_normalized = reconstructed_raw / np.linalg.norm(reconstructed_raw)
        vector_length = 2.0
        reconstructed_end_point = reconstructed_normalized * vector_length

        # Show the yellow dashed line going up from the 2D projection
        projection_line = DashedLine(h_vector, reconstructed_end_point, color=YELLOW, dash_length=0.1)
        self.play(FadeIn(projection_line), run_time=0.6)

        # Show the reconstruction equation W^\top * h
        reconstruction_equation = MathTex(r"W^{\top} \cdot h", font_size=36, color=WHITE)
        reconstruction_equation.next_to(projection_line.get_center(), LEFT*0.2 + UP*0.5, buff=1.2)
        
        self.add_fixed_orientation_mobjects(reconstruction_equation)
        self.play(FadeIn(reconstruction_equation), run_time=0.8)
        self.wait(0.8)

        # Show the reconstructed 3D vector
        reconstructed_vector_arrow = Arrow3D(start=ORIGIN, end=reconstructed_end_point, color=GREEN)
        
        # Add label for the reconstructed 3D vector
        reconstructed_label = MathTex(r"\hat{x} = \begin{bmatrix} 0.6 \\ 1.0 \\ 0.8 \end{bmatrix}", font_size=36, color=WHITE)
        reconstructed_label.next_to(reconstructed_vector_arrow.get_end(), LEFT*3.8 + DOWN*0.8, buff=1.5)
        
        self.play(FadeIn(reconstructed_vector_arrow), run_time=0.8)
        self.add_fixed_orientation_mobjects(reconstructed_label)
        self.play(FadeIn(reconstructed_label), run_time=0.8)
        self.wait(1.0)