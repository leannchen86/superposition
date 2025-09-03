from manim import *
import numpy as np

class StrawBoxWithCage(ThreeDScene):
    def construct(self):
        # Set camera to face the more square side (yz face), from a top ~45° angle
        # Use an explicit starting distance so we can animate a smooth zoom-in later
        # 45°-ish top-down, closer to ground; facing the square side (yz plane)
        self.set_camera_orientation(phi=80 * DEGREES, theta=0 * DEGREES, distance=6)
        # self.camera.frame.scale(0.75)
        # Parameters
        rows, cols = 6, 4
        straw_radius = 0.05
        straw_height = 4.0
        # Make straws almost touching: spacing ≈ 2*radius + tiny gap
        gap = 0.01
        spacing_y = 2 * straw_radius + gap
        spacing_z = 2 * straw_radius + gap
        # Boxed straws layout (flat, aligned, inside the cage)
        straws = VGroup()
        # Create array of vertical straws (cylinders)
        for i in range(rows):
            for j in range(cols):
                y = i * spacing_y - (rows - 1) * spacing_y / 2
                z = j * spacing_z - (cols - 1) * spacing_z / 2
                x = 0  # Keep all straws centered in x
                straw = Cylinder(
                    radius=straw_radius,
                    height=straw_height,
                    direction=RIGHT,  # Lying flat toward foreground
                    fill_opacity=0.4,
                    fill_color=BLUE,
                    stroke_opacity=0.1,
                ).move_to([x, y, z])
                straws.add(straw)
        # Dimensions for the box (tight rectangular fit with small padding)
        padding_x, padding_y, padding_z = 0.1, 0.06, 0.06
        # Width along x (cylinders lie along x): total length + padding on both sides
        box_width = straw_height + 2 * padding_x
        # Height along y: span of centers + straw radii at both ends + padding
        box_height = (rows - 1) * spacing_y + 2 * straw_radius + 2 * padding_y
        # Depth along z: span of centers + straw radii at both ends + padding
        box_depth = (cols - 1) * spacing_z + 2 * straw_radius + 2 * padding_z
        # Create a translucent box around the straws
        box = Cube(
            side_length=1,  # Will non-uniformly stretch per axis
            fill_opacity=0.4,
            fill_color=GRAY,
            stroke_opacity=0.2,
        )
        box.stretch_to_fit_width(box_width)
        box.stretch_to_fit_height(box_height)
        box.stretch_to_fit_depth(box_depth)
        box.move_to(ORIGIN)
        # Group and show at center first
        scene_group = VGroup(box, straws)
        # Build scatter target layout with the same number of straws and ordering
        num_straws = rows * cols
        rng = np.random.default_rng(1)
        scatter_sigma_y = straw_height * 0.25
        scatter_sigma_z = straw_height * 0.25
        scatter_sigma_x = straw_height * 0.05
        y_positions = rng.normal(0.0, scatter_sigma_y, size=num_straws)
        z_positions = rng.normal(0.0, scatter_sigma_z, size=num_straws)
        x_positions = rng.normal(0.0, scatter_sigma_x, size=num_straws)
        angles_yz = rng.uniform(0, 2 * np.pi, size=num_straws)
        x_tilts = rng.normal(0.0, 0.25, size=num_straws)
        scatter_straws_right = VGroup()
        k = 0
        for i in range(rows):
            for j in range(cols):
                dir_vec = np.array([
                    x_tilts[k],
                    np.cos(angles_yz[k]),
                    np.sin(angles_yz[k]),
                ])
                dir_vec = dir_vec / np.linalg.norm(dir_vec)
                scatter_straw = (
                    Cylinder(
                        radius=straw_radius,
                        height=straw_height,
                        direction=dir_vec,
                        fill_opacity=0.4,
                        fill_color=BLUE,
                        stroke_opacity=0.1,
                    )
                    .move_to([x_positions[k], y_positions[k], z_positions[k]])
                )
                scatter_straws_right.add(scatter_straw)
                k += 1
        
        # With the camera oriented to face the yz-plane (theta≈0), on-screen
        # left/right corresponds to the world ±y direction (same as big_straw_box.py)
        right_unit = np.array([0.0, 1.0, 0.0])  # +y direction (right on screen)
        left_unit = -right_unit                  # -y direction (left on screen)
        
        # Shift amount for left-right separation instead of front-back - increased distance by 1.2x
        gap_lr = 0.8 * 1.2
        shift_amount = (box_height + gap_lr) * 1.2  # Increased by 1.2x from previous
        
        # Move the scattered straws to the right and position the box to the left
        scatter_straws_right.shift(right_unit * shift_amount)

        # Animation sequence - all self.play calls at the end
        # self.add(scene_group)
        self.play(FadeIn(scene_group), run_time=0.5)
        self.play(scene_group.animate.scale(1.8), run_time=0.8)
        # ThreeDScene uses move_camera instead of camera.frame animations
        # Start distance was set to 7; zoom in by ~20% → distance ≈ 5.6
        self.move_camera(distance=5.6, frame_center=box.get_center(), run_time=0.2)
        self.play(
            box.animate.shift(left_unit * shift_amount).scale(1.65),  # Scale box by 1.5 while moving
            Transform(straws, scatter_straws_right),
            run_time=1.8,
        )
        # self.begin_ambient_camera_rotation(rate=0.1)  # slow rotation
        # self.wait(5)  # rotate for 5 seconds
        # self.stop_ambient_camera_rotation()