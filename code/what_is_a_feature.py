from manim import *
import numpy as np


class WhatIsAFeature(ThreeDScene):
    """Visualize five equally spaced 3-D vectors on a grid."""

    def construct(self):
        # ------------------------------------------------------------------
        # Camera & Scene Setup
        # ------------------------------------------------------------------
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(0.7)

        # Create a 2-D grid lying on the xy-plane (z = 0)
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

        # Add vertical helper lines for depth perception
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

        # 3-D axes
        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(0, 5, 1),
            x_length=10,
            y_length=10,
            z_length=5,
            axis_config={"color": WHITE, "include_tip": False, "include_numbers": False},
        )

        # Add the static elements to the scene
        self.add(grid, vertical_lines, axes)

        # ------------------------------------------------------------------
        # Create 5 equally spaced vectors (length = 2)
        # ------------------------------------------------------------------
        vectors = VGroup()
        radius = 2
        polar_angle = 60 * DEGREES  # tilt above the xy-plane

        for k in range(5):
            azimuth = k * 72 * DEGREES  # 360° / 5 → equally spaced
            end_point = [
                radius * np.sin(polar_angle) * np.cos(azimuth),
                radius * np.sin(polar_angle) * np.sin(azimuth),
                radius * np.cos(polar_angle),
            ]
            vectors.add(Arrow3D(start=ORIGIN, end=end_point, color=RED))

        # Animate the appearance of the vectors
        self.play(*[Create(v) for v in vectors])

        # ------------------------------------------------------------------
        # Camera movement for a dynamic view
        # ------------------------------------------------------------------
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, zoom=1.5, run_time=2)
        self.wait(1)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(10)