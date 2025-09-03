from manim import *
import numpy as np

class BigStrawBox(ThreeDScene):
    def construct(self):
        # Set camera to face the more square side (yz face), from a high angle initially
        # Use an explicit starting distance so we can animate a smooth zoom-in later
        # High angle view; facing the square side (yz plane)
        self.set_camera_orientation(phi=85 * DEGREES, theta=0 * DEGREES, distance=6)
        # self.camera.frame.scale(0.75)
        # Parameters for straw grid
        rows, cols = 15, 15
        straw_radius = 0.05
        straw_height = 4.0
        # Make straws almost touching: spacing ≈ 2*radius + tiny gap
        gap = 0.01
        spacing_y = 2 * straw_radius + gap
        spacing_z = 2 * straw_radius + gap
        # Original stacked straws centered at origin (inside the box)
        straws = VGroup()
        for i in range(rows):
            for j in range(cols):
                y = i * spacing_y - (rows - 1) * spacing_y / 2
                z = j * spacing_z - (cols - 1) * spacing_z / 2
                x = 0
                straw = Cylinder(
                    radius=straw_radius,
                    height=straw_height,
                    direction=RIGHT,
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
        # With the camera oriented to face the yz-plane (theta≈0), on-screen
        # left/right corresponds to the world ±y direction (not ±z).
        # FIX: Use y-axis for left-right movement on screen
        right_unit = np.array([0.0, 1.0, 0.0])  # +y direction (right on screen)
        left_unit = -right_unit                  # -y direction (left on screen)
        # Shift amount chosen so the straw stack ends up clearly outside the box
        # when viewed on-screen. Using half the box height (screen-horizontal size)
        # plus a larger gap ensures visible separation and room for text/arrow.
        gap_lr = 2.0
        shift_amount = box_height / 2 + gap_lr  # Also changed from box_depth to box_height
        # Add box first
        self.add(box)
        # Then animate the box moving left and scaling
        self.play(
            box.animate.shift(left_unit * shift_amount).scale(1.05),
            run_time=1.2,
        )
        # Then create and position the straws
        straws.shift(right_unit * shift_amount).scale(2.3)
        self.add(straws)
        self.play(FadeIn(straws, lag_ratio=0.001), run_time=2.0)
        self.wait(5)
        self.play(FadeOut(straws), run_time=1.0)