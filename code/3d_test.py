from manim import *

class Vector3DScene(ThreeDScene):
    def construct(self):
        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            z_range=[0, 1, 0.2],
            x_length=6,
            y_length=6,
            z_length=6,
        )

        self.set_camera_orientation(phi=75 * DEGREES, theta= 30 * DEGREES)
        self.add(axes)

        # Define the vector
        vec = [0.3, 0.7, 0.6]
        origin = axes.coords_to_point(0, 0, 0)
        end_point = axes.coords_to_point(*vec)
        vector = Arrow3D(
            start=origin,
            end=end_point,
            color=YELLOW,
            thickness=0.02,
            height=0.3,
            base_radius=0.05,
        )

        # Label the vector
        label = MathTex(r"\vec{v} = [0.3,\ 0.7,\ 0.6]").move_to(end_point + 0.2 * RIGHT + 0.2 * UP)

        # Add the vector and label to the scene
        self.play(Create(vector), Write(label))
        self.wait(2)
