from manim import *
import numpy as np


class Simple3DGreenVector(ThreeDScene):
    def construct(self):
        # Set up 3D camera orientation
        start_distance = 8.0
        self.set_camera_orientation(phi=80 * DEGREES, theta=15 * DEGREES, distance=start_distance, zoom=1.5)

        # Create 3D grid and axes
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

        # Add the 3D space elements
        self.add(grid, vertical_lines, axes)

        # Create the green 3D vector [0.6, 1.0, 0.8]
        reconstructed_raw = np.array([0.6, 1.0, 0.8])
        reconstructed_normalized = reconstructed_raw / np.linalg.norm(reconstructed_raw)
        vector_length = 2.0
        reconstructed_end_point = reconstructed_normalized * vector_length

        # Show the green 3D vector
        reconstructed_vector_arrow = Arrow3D(start=ORIGIN, end=reconstructed_end_point, color=GREEN)
        
        # Add label for the green 3D vector
        reconstructed_label = MathTex(r"\hat{x} = \begin{bmatrix} 0.6 \\ 1.0 \\ 0.8 \end{bmatrix}", font_size=36, color=WHITE)
        reconstructed_label.next_to(reconstructed_vector_arrow.get_end(), LEFT*3.8 + DOWN*0.8, buff=1.5)
        
        # Display the vector and its label
        self.play(FadeIn(reconstructed_vector_arrow), run_time=0.8)
        self.add_fixed_orientation_mobjects(reconstructed_label)
        self.play(FadeIn(reconstructed_label), run_time=0.8)
        self.wait(2.0)