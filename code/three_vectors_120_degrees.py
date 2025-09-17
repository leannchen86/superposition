from manim import *
import numpy as np

class ThreeVectors120Degrees(Scene):
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
        
        # Define colors for vectors
        colors = [RED, BLUE, GREEN]
        
        # Create three vectors 120° apart
        angles = [0, 2*PI/3, 4*PI/3]  # 0°, 120°, 240°
        vectors = []
        
        for i, angle in enumerate(angles):
            vector = Arrow(
                ORIGIN, 
                2*np.array([np.cos(angle), np.sin(angle), 0]), 
                color=colors[i], 
                buff=0,
                stroke_width=4
            )
            vectors.append(vector)
        
        # Show initial setup
        self.play(FadeIn(axes))
        for vector in vectors:
            self.play(Create(vector))
        self.wait(1)
        
        # Show initial angle between red and blue vectors
        red_vector = vectors[0]
        blue_vector = vectors[1]
        
        # Create initial angle arc and label
        angle_arc = Angle(red_vector, blue_vector, radius=0.7, other_angle=False)
        angle_label = Tex(r"120°").next_to(angle_arc, UR, buff=0.1)
        
        self.play(Create(angle_arc), Write(angle_label))
        self.wait(1)
        
        # Rotate blue vector (index 1) from 120° to 90° to be perpendicular with red vector
        rotation_angle = PI/2 - 2*PI/3  # 90° - 120° = -30°
        
        # Create final angle arc and label for 90°
        final_blue_vector = Arrow(
            ORIGIN, 
            2*np.array([np.cos(PI/2), np.sin(PI/2), 0]), 
            color=BLUE, 
            buff=0,
            stroke_width=4
        )
        final_angle_arc = Angle(red_vector, final_blue_vector, radius=0.7, other_angle=False)
        final_angle_label = Tex(r"90°").next_to(final_angle_arc, UR, buff=0.1)
        
        # Animate the rotation with dynamic arc and label updates
        self.play(
            Rotate(blue_vector, angle=rotation_angle, about_point=ORIGIN),
            Transform(angle_arc, final_angle_arc),
            Transform(angle_label, final_angle_label),
            run_time=3
        )
        self.wait(2)