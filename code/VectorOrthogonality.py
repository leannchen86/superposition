from manim import *
import numpy as np

class VectorOrthogonality(Scene):
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
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(0.5)
        
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
        
        # Step 1: Show 2 orthogonal vectors
        vec1 = Arrow(ORIGIN, 2*RIGHT, color=colors[0], buff=0)
        vec2 = Arrow(ORIGIN, 2*UP, color=colors[1], buff=0)
        
        self.play(GrowArrow(vec1), GrowArrow(vec2))
        self.wait(0.5)
        
        # Show angle between vectors
        angle_arc = Angle(vec1, vec2, radius=0.5, other_angle=False)
        angle_label = MathTex("90°").next_to(angle_arc, UR, buff=0.1)
        
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(0.5)
        
        # Show dot product = 0
        dot_product_text = MathTex("\\text{dot product} = 0").shift(3*UP)
        self.play(Write(dot_product_text))
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
        angle_text = MathTex("120°\\text{ apart}").shift(3*UP)
        self.play(Write(angle_text))
        self.wait(1.5)
        self.play(FadeOut(angle_text))
        
        # Step 3: Add fourth vector and rotate all vectors to be 90° apart
        vec4 = get_vector(135, colors[3])
        self.play(GrowFromPoint(vec4, ORIGIN))

        target_angles_4 = [0, 90, 180, 270]  # Desired final angles (degrees)
        rotations_4 = [
            Rotate(vec1, angle=np.deg2rad(target_angles_4[0] - 0), about_point=ORIGIN),
            Rotate(vec2, angle=np.deg2rad(target_angles_4[1] - 120), about_point=ORIGIN),
            Rotate(vec3, angle=np.deg2rad(target_angles_4[2] - 240), about_point=ORIGIN),
            Rotate(vec4, angle=np.deg2rad(target_angles_4[3] - 135), about_point=ORIGIN),
        ]
        self.play(*rotations_4)
        self.wait(1)
        
        # Show 90° label
        angle_text = MathTex("90°\\text{ apart}").shift(3*UP)
        self.play(Write(angle_text))
        self.wait(1.5)
        self.play(FadeOut(angle_text))
        
        # Step 4: Add fifth vector and rotate all vectors to be 72° apart
        vec5 = get_vector(225, colors[4])
        self.play(GrowFromPoint(vec5, ORIGIN))

        target_angles_5 = [0, 72, 144, 216, 288]  # Desired final angles (degrees)
        rotations_5 = [
            Rotate(vec1, angle=np.deg2rad(target_angles_5[0] - 0), about_point=ORIGIN),
            Rotate(vec2, angle=np.deg2rad(target_angles_5[1] - 90), about_point=ORIGIN),
            Rotate(vec3, angle=np.deg2rad(target_angles_5[2] - 180), about_point=ORIGIN),
            Rotate(vec4, angle=np.deg2rad(target_angles_5[3] - 270), about_point=ORIGIN),
            Rotate(vec5, angle=np.deg2rad(target_angles_5[4] - 225), about_point=ORIGIN),
        ]
        self.play(*rotations_5)
        self.wait(2)

        existing_vecs = [vec1, vec2, vec3, vec4, vec5]
        
        # Show 72° label and final message
        angle_text = MathTex("72°\\text{ apart}").shift(3*UP)
        self.play(Write(angle_text))
        self.wait(1)
        
        # Final message about interference
        interference_text = Text(
            "With 5 vectors in 2D: overlap is inevitable!", 
            font_size=24
        ).shift(3.5*DOWN)
        self.play(Write(interference_text))
        self.wait(1)
        
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
        proj_dot = Dot(proj_point, color=ORANGE, radius=0.1)
        proj_line = DashedLine(
            start=2*vec_b_dir, 
            end=proj_point,
            color=ORANGE,
            stroke_width=3,
            dash_length=0.2
        )
        
        # Show projection
        self.play(Create(proj_line))
        self.play(FadeIn(proj_dot))
        self.wait(0.5)
        
        # Add projection label
        proj_text = Text(
            "Projection causes overlap", 
            font_size=20,
            color=ORANGE
        ).shift(2.5*LEFT + 1*UP)
        self.play(Write(proj_text))
        self.wait(1.5)
        
        # Show interference visualization with overlapping regions
        overlap_region = Circle(
            radius=0.3,
            color=YELLOW,
            fill_opacity=0.3,
            stroke_width=2
        ).move_to(proj_point)
        
        interference_label = Text(
            "Interference!", 
            font_size=18,
            color=YELLOW
        ).next_to(overlap_region, DOWN)
        
        self.play(FadeIn(overlap_region), Write(interference_label))
        self.wait(2)