from manim import *
import numpy as np

class StrawDirectionConstraint3D(ThreeDScene):
    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        # Create a 3D box
        box = Cube(side_length=4, fill_opacity=0.1, stroke_width=2)
        box.set_color(GRAY)
        
        # Phase 1: Show parallel straws (NOT ALLOWED)
        # Create multiple straws with same directions
        parallel_straws = VGroup()
        
        # Group 1: Horizontal parallel straws
        for i in range(3):
            straw = Cylinder(
                radius=0.08,
                height=3,
                direction=RIGHT,
                fill_color=RED,
                fill_opacity=0.8,
                stroke_width=0
            )
            straw.shift(UP * (i - 1) * 0.5 + LEFT * 0.5)
            parallel_straws.add(straw)
        
        # Group 2: Diagonal parallel straws
        for i in range(2):
            straw = Cylinder(
                radius=0.08,
                height=2.5,
                direction=normalize(RIGHT + UP + OUT * 0.5),
                fill_color=RED,
                fill_opacity=0.8,
                stroke_width=0
            )
            straw.shift(DOWN * 0.5 + RIGHT * (i - 0.5) * 0.8)
            parallel_straws.add(straw)
        
        # "Not Allowed" label
        not_allowed_text = Text("NOT ALLOWED", font_size=24, color=RED)
        not_allowed_text.to_corner(UL)
        
        # Add elements to scene
        self.play(Create(box))
        self.wait(0.5)
        self.play(
            FadeIn(parallel_straws),
            Write(not_allowed_text)
        )
        
        # Highlight the parallel nature with flashing
        self.play(
            parallel_straws.animate.set_fill(RED_E),
            rate_func=there_and_back,
            run_time=0.5
        )
        self.play(
            parallel_straws.animate.set_fill(RED),
            rate_func=there_and_back,
            run_time=0.5
        )
        
        # Rotate camera to show the parallel nature better
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # Phase 2: Transform to unique directions (ALLOWED)
        unique_straws = VGroup()
        
        # Define unique directions for each straw
        directions = [
            RIGHT,
            normalize(RIGHT + UP * 0.3),
            normalize(RIGHT + DOWN * 0.5 + OUT * 0.2),
            normalize(LEFT * 0.5 + UP + OUT * 0.3),
            normalize(RIGHT * 0.7 + DOWN * 0.3 + IN * 0.4)
        ]
        
        colors = [BLUE, GREEN, ORANGE, PURPLE, TEAL]
        
        # Create straws with unique directions
        for i, (direction, color) in enumerate(zip(directions, colors)):
            straw = Cylinder(
                radius=0.08,
                height=2.5 + i * 0.2,
                direction=direction,
                fill_color=color,
                fill_opacity=0.8,
                stroke_width=0
            )
            # Position them in different parts of the box
            if i == 0:
                straw.shift(UP * 0.5 + LEFT * 0.3)
            elif i == 1:
                straw.shift(DOWN * 0.3 + RIGHT * 0.5)
            elif i == 2:
                straw.shift(UP * 0.2 + OUT * 0.4)
            elif i == 3:
                straw.shift(DOWN * 0.5 + IN * 0.3 + LEFT * 0.2)
            else:
                straw.shift(RIGHT * 0.3 + OUT * 0.2)
            
            unique_straws.add(straw)
        
        # "Allowed" label
        allowed_text = Text("ALLOWED", font_size=24, color=GREEN)
        allowed_text.to_corner(UL)
        
        # Smooth transition
        self.play(
            FadeOut(not_allowed_text),
            Transform(parallel_straws, unique_straws),
            run_time=2
        )
        self.play(Write(allowed_text))
        
        # Show the unique directions by rotating
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(4)
        
        # Highlight crossing points
        # Add small spheres where straws cross/touch
        cross_points = VGroup()
        for _ in range(3):
            point = Sphere(radius=0.1, color=YELLOW, fill_opacity=0.8)
            # Place at some intersection points
            point.move_to([
                np.random.uniform(-1, 1),
                np.random.uniform(-1, 1),
                np.random.uniform(-0.5, 0.5)
            ])
            cross_points.add(point)
        
        self.play(FadeIn(cross_points))
        self.wait(2)
        
        # Final camera movement
        self.move_camera(phi=75 * DEGREES, theta=-30 * DEGREES, run_time=2)
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(VGroup(box, parallel_straws, allowed_text, cross_points)),
            run_time=1
        )