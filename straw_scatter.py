from manim import *
import numpy as np


class StrawScatter(ThreeDScene):
    def construct(self):
        # Camera angled from top with a comfortable viewing distance
        self.set_camera_orientation(phi=20 * DEGREES, theta=0 * DEGREES, distance=8)

        # Parameters, kept consistent with the boxed version
        rows, cols = 6, 4
        num_straws = rows * cols
        straw_radius = 0.05
        straw_height = 4.0

        # Random generator (fixed seed for reproducibility)
        rng = np.random.default_rng(1)

        # Tighter cluster near the origin so straws overlap/crisscross
        scatter_sigma_y = straw_height * 0.25
        scatter_sigma_z = straw_height * 0.25
        scatter_sigma_x = straw_height * 0.05

        y_positions = rng.normal(0.0, scatter_sigma_y, size=num_straws)
        z_positions = rng.normal(0.0, scatter_sigma_z, size=num_straws)
        x_positions = rng.normal(0.0, scatter_sigma_x, size=num_straws)

        # Random orientations: mostly in YZ plane, slight tilt in X to create depth
        angles_yz = rng.uniform(0, 2 * np.pi, size=num_straws)
        x_tilts = rng.normal(0.0, 0.25, size=num_straws)  # smaller magnitude -> mostly flat pile

        straws = VGroup()
        for idx in range(num_straws):
            dir_vec = np.array([
                x_tilts[idx],
                np.cos(angles_yz[idx]),
                np.sin(angles_yz[idx]),
            ])
            dir_vec = dir_vec / np.linalg.norm(dir_vec)

            straw = (
                Cylinder(
                    radius=straw_radius,
                    height=straw_height,
                    direction=dir_vec,
                    fill_opacity=0.4,
                    fill_color=BLUE,
                    stroke_opacity=0.1,
                )
                .move_to([x_positions[idx], y_positions[idx], z_positions[idx]])
            )
            straws.add(straw)

        self.play(Create(straws))

        # # Slow zoom-in for a cinematic effect
        # self.play(straws.animate.scale(1.3), run_time=5)


