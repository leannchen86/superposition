from manim import *

class VectorAdjustment(Scene):
    def construct(self):
        # Create 2D axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": BLUE},
        )
        self.play(Create(axes))

        # Define distinct colors for each vector
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]

        # Helper function to create a vector at a given angle
        def get_vector(angle, color):
            return Vector([np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))], color=color)

        # Step 1: Two vectors at 0° and 90°
        v1 = get_vector(0, colors[0])
        v2 = get_vector(90, colors[1])
        self.play(GrowFromPoint(v1, ORIGIN), GrowFromPoint(v2, ORIGIN))

        # Show 90° angle between them
        angle = Angle(v1, v2, radius=0.5, other_angle=False)
        angle_label = MathTex("90^\circ").next_to(angle, RIGHT)
        self.play(Create(angle), Write(angle_label))

        # Display dot product text
        dot_product_text = Text("dot product = 0", font_size=24).to_edge(UP)
        self.play(Write(dot_product_text))
        self.wait(1)
        self.play(FadeOut(angle), FadeOut(angle_label))

        # Step 2: Add third vector and adjust to 120° apart
        v3 = get_vector(45, colors[2])
        self.play(GrowFromPoint(v3, ORIGIN))
        target_angles_3 = [0, 120, 240]
        rotations_3 = [
            Rotate(v1, angle=np.deg2rad(target_angles_3[0] - 0), about_point=ORIGIN),
            Rotate(v2, angle=np.deg2rad(target_angles_3[1] - 90), about_point=ORIGIN),
            Rotate(v3, angle=np.deg2rad(target_angles_3[2] - 45), about_point=ORIGIN),
        ]
        self.play(*rotations_3)
        self.wait(1)

        # Step 3: Add fourth vector and adjust to 90° apart
        v4 = get_vector(135, colors[3])
        self.play(GrowFromPoint(v4, ORIGIN))
        target_angles_4 = [0, 90, 180, 270]
        rotations_4 = [
            Rotate(v1, angle=np.deg2rad(target_angles_4[0] - 0), about_point=ORIGIN),
            Rotate(v2, angle=np.deg2rad(target_angles_4[1] - 120), about_point=ORIGIN),
            Rotate(v3, angle=np.deg2rad(target_angles_4[2] - 240), about_point=ORIGIN),
            Rotate(v4, angle=np.deg2rad(target_angles_4[3] - 135), about_point=ORIGIN),
        ]
        self.play(*rotations_4)
        self.wait(1)

        # Step 4: Add fifth vector and adjust to 72° apart
        v5 = get_vector(225, colors[4])
        self.play(GrowFromPoint(v5, ORIGIN))
        target_angles_5 = [0, 72, 144, 216, 288]
        rotations_5 = [
            Rotate(v1, angle=np.deg2rad(target_angles_5[0] - 0), about_point=ORIGIN),
            Rotate(v2, angle=np.deg2rad(target_angles_5[1] - 90), about_point=ORIGIN),
            Rotate(v3, angle=np.deg2rad(target_angles_5[2] - 180), about_point=ORIGIN),
            Rotate(v4, angle=np.deg2rad(target_angles_5[3] - 270), about_point=ORIGIN),
            Rotate(v5, angle=np.deg2rad(target_angles_5[4] - 225), about_point=ORIGIN),
        ]
        self.play(*rotations_5)
        self.wait(2)