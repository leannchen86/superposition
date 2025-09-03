from manim import *
import numpy as np

class VectorOrthogonality(MovingCameraScene):
    def construct(self):
        # Setup the 2D coordinate system
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"color": GREY},
            tips=False,
        )
        # Add axis labels
        x_label = MathTex("x").next_to(axes.x_axis, RIGHT)
        y_label = MathTex("y").next_to(axes.y_axis, UP)
        # Define colors for vectors
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        # Helper to generate a 2-unit vector (arrow) at a given angle in degrees
        def get_vector(angle_deg, color):
            angle_rad = np.deg2rad(angle_deg)
            return Vector(
                2 * np.array([np.cos(angle_rad), np.sin(angle_rad), 0]),
                color=color,
                stroke_width=4,
            )
        
        def get_angle_arc(vec1, vec2):
            return Angle(vec1, vec2, radius=0.5, other_angle=False)
        
        # Step 1: Show 2 orthogonal vectors
        vec1 = Arrow(ORIGIN, 2*RIGHT, color=colors[0], buff=0)
        vec2 = Arrow(ORIGIN, 2*UP, color=colors[1], buff=0)
        
        # Show angle between vectors
        angle_arc = get_angle_arc(vec1, vec2)
        angle_label = Tex(r"90°").next_to(angle_arc, UR, buff=0.1)
        
        # Show dot product = 0
        dot_product_text = MathTex("\\text{dot product} = 0").shift(3*RIGHT + 2*UP)
        
        # Animation sequence - step-by-step demonstration
        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))
        self.play(Create(vec1), Create(vec2), run_time=1.2)
        self.play(Create(angle_arc), Create(angle_label), run_time=1)
        self.play(Write(dot_product_text), run_time=1.5)
        self.wait(1.5)
        
        # Remove angle and dot product text for clarity
        self.play(FadeOut(angle_arc), FadeOut(angle_label), FadeOut(dot_product_text))
        
        # Step 2: Add 3rd vector and redistribute
        vec3 = Arrow(ORIGIN, 2*LEFT, color=colors[2], buff=0, stroke_width=4)
        self.play(GrowArrow(vec3))
        self.wait(0.5)
        
        # Animate redistribution to 120° apart
        new_angles = [0, 2*PI/3, 4*PI/3]
        new_vecs = []
        for i, (vec, angle) in enumerate(zip([vec1, vec2, vec3], new_angles)):
            new_vec = Arrow(
                ORIGIN, 
                2*np.array([np.cos(angle), np.sin(angle), 0]), 
                color=colors[i], 
                buff=0,
                stroke_width=4
            )
            new_vecs.append(new_vec)
        
        self.play(
            Transform(vec1, new_vecs[0]),
            Transform(vec2, new_vecs[1]),
            Transform(vec3, new_vecs[2]),
            run_time=2
        )
        
        # Show 120° label
        angle_arc = get_angle_arc(new_vecs[0], new_vecs[1])
        angle_label = Tex(r"120°").next_to(angle_arc, UR, buff=0.1)
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(1.5)
        self.play(FadeOut(angle_arc), FadeOut(angle_label))
        
        # Step 3: Add fourth vector and rotate all vectors to be 90° apart
        vec4 = get_vector(270, colors[3])
        self.play(GrowFromPoint(vec4, ORIGIN))

        target_angles_4 = [0, 90, 180, 270]  # Desired final angles (degrees)
        rotations_4 = [
            Rotate(vec1, angle=np.deg2rad(target_angles_4[0] - 0), about_point=ORIGIN),
            Rotate(vec2, angle=np.deg2rad(target_angles_4[1] - 120), about_point=ORIGIN),
            Rotate(vec3, angle=np.deg2rad(target_angles_4[2] - 240), about_point=ORIGIN),
            Rotate(vec4, angle=np.deg2rad(target_angles_4[3] - 270), about_point=ORIGIN),
        ]
        self.play(*rotations_4)
        self.wait(1)
        
        # Show 90° label
        angle_arc = get_angle_arc(vec1, vec2)
        angle_label = Tex(r"90°").next_to(angle_arc, UR, buff=0.1)
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(1.5)
        self.play(FadeOut(angle_arc), FadeOut(angle_label))
        
        # Step 4: Add fifth vector and rotate all vectors to be 72° apart
        vec5 = get_vector(300, colors[4])
        self.play(GrowFromPoint(vec5, ORIGIN))

        target_angles_5 = [0, 72, 144, 216, 288]  # Desired final angles (degrees)
        rotations_5 = [
            Rotate(vec1, angle=np.deg2rad(target_angles_5[0] - 0), about_point=ORIGIN),
            Rotate(vec2, angle=np.deg2rad(target_angles_5[1] - 90), about_point=ORIGIN),
            Rotate(vec3, angle=np.deg2rad(target_angles_5[2] - 180), about_point=ORIGIN),
            Rotate(vec4, angle=np.deg2rad(target_angles_5[3] - 270), about_point=ORIGIN),
            Rotate(vec5, angle=np.deg2rad(target_angles_5[4] - 300), about_point=ORIGIN),
        ]
        self.play(*rotations_5)
        self.wait(2)

        existing_vecs = [vec1, vec2, vec3, vec4, vec5]
        
        # Show 72° label and final message
        # Use the updated list of five vectors to show the 72° separation
        angle_arc = get_angle_arc(existing_vecs[0], existing_vecs[1])
        angle_label = Tex(r"72°").next_to(angle_arc, UR, buff=0.1)
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(1)
        self.play(FadeOut(angle_arc), FadeOut(angle_label))
        
        # Show projection effect - demonstrate overlap/interference
        self.show_projection_interference(existing_vecs)
        
        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
    
    def show_projection_interference(self, vectors):
        # Pick two vectors that are close to each other to show overlap
        vec_a = vectors[0]  # First vector (RED)
        vec_b = vectors[1]  # Second vector (BLUE)
        
        # Get vector directions for projection calculation
        vec_a_dir = np.array([np.cos(0), np.sin(0), 0])  # 0° direction
        vec_b_dir = np.array([np.cos(2*PI/5), np.sin(2*PI/5), 0])  # 72° direction
        
        # Calculate projection of vec_b onto vec_a
        proj_scalar = np.dot(vec_b_dir, vec_a_dir)
        proj_point = 2 * proj_scalar * vec_a_dir  # Scale by vector length
        
        # Create projection visualization
        proj_line = DashedLine(
            start=2*vec_b_dir, 
            end=proj_point,
            color=WHITE,
            stroke_width=3,
            dash_length=0.2
        )

        #create a solid orange line from the origin of vec_b to the end of the projection on the x-axis
        proj_line_solid = Line(
            start=ORIGIN,
            end=proj_point,
            color=WHITE,
            stroke_width=5
        )
        
        # Show projection
        #zoom the camera in on the projection
        self.play(self.camera.frame.animate.scale(0.5).move_to(proj_point))
        self.play(Create(proj_line))
        self.play(Create(proj_line_solid))
        self.wait(0.5)
        
        # Add projection label
        proj_text = Tex(r"Projection causes overlap", font_size=20, color=ORANGE).shift(2.5*RIGHT + 0.8 + 1*UP).set_x(0.5)
        self.play(Write(proj_text))
        self.wait(1.5)