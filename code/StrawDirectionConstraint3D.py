from manim import *
import numpy as np

class StrawDirectionConstraint3D(ThreeDScene):
    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        
        # Phase 1: Show parallel straws (NOT ALLOWED)
        # Create multiple straws with same directions
        horizontal_parallel_straws = VGroup()
        diagonal_parallel_straws = VGroup()
        
        # Group 1: Horizontal parallel straws
        for i in range(3):
            straw = Cylinder(
                radius=0.08,
                height=3,
                direction=RIGHT,
            )
            straw.set_color(RED)
            straw.set_fill(RED, opacity=0.8)
            straw.set_style(fill_color=RED, stroke_color=RED)
            straw.shift(UP * (i - 1) * 0.5 + LEFT * 0.5)
            horizontal_parallel_straws.add(straw)
        
        # Group 2: Diagonal parallel straws
        for i in range(2):
            straw = Cylinder(
                radius=0.08,
                height=2.5,
                direction=normalize(RIGHT + UP + OUT * 0.5),
            )
            straw.set_color(RED)
            straw.set_fill(RED, opacity=0.8)
            straw.set_style(fill_color=RED, stroke_color=RED)
            straw.shift(DOWN * 0.5 + RIGHT * (i - 0.5) * 0.8)
            diagonal_parallel_straws.add(straw)
        
        # Create two initial demonstration straws (blue), one from each group's orientation
        initial_horizontal_straw = Cylinder(
            radius=0.08,
            height=3,
            direction=RIGHT,
            fill_color=None,
            fill_opacity=0.9,
            stroke_width=0,
        )
        initial_diagonal_straw = Cylinder(
            radius=0.08,
            height=2.5,
            direction=normalize(RIGHT + UP + OUT * 0.5),
            fill_color=None,
            fill_opacity=0.9,
            stroke_width=0,
        )


        # Phase 2: Transform to unique directions (ALLOWED)
        allowed_unique_straws = VGroup()
        
        # Define unique directions for each straw
        directions = [
            RIGHT,
            normalize(RIGHT + UP * 0.3),
            normalize(RIGHT + DOWN * 0.5 + OUT * 0.2),
            normalize(LEFT * 0.5 + UP + OUT * 0.3),
            normalize(RIGHT * 0.7 + DOWN * 0.3 + IN * 0.4)
        ]
        
        # Create straws with unique directions
        for i, direction in enumerate(directions):
            straw = Cylinder(
                radius=0.08,
                height=2.5 + i * 0.2,
                direction=direction,
                fill_color=None,
                fill_opacity=0.8,
                stroke_width=0,
                stroke_color=BLUE,
            )
            # Position them in different parts of space
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
            
            allowed_unique_straws.add(straw)
        
        # Animation sequence - all self.play calls at the end
        # Scale all straws by 1.8 to match initial straw scaling
        initial_horizontal_straw.scale(1.8)
        initial_diagonal_straw.scale(1.8)
        horizontal_parallel_straws.scale(1.8)
        diagonal_parallel_straws.scale(1.8)
        allowed_unique_straws.scale(1.8)
        
        self.play(FadeIn(VGroup(initial_horizontal_straw, initial_diagonal_straw)), run_time=1)
        self.wait(0.3)

        self.play(
            ReplacementTransform(VGroup(initial_horizontal_straw, initial_diagonal_straw), allowed_unique_straws),
            run_time=1,
            )
        
        self.wait(2.5)
        
        # Fade out the transformed initial straws (now matching allowed_unique_straws)
        self.play(FadeOut(allowed_unique_straws), run_time=0.5)

        # Bring in horizontal parallel straws (not allowed)
        self.play(FadeIn(horizontal_parallel_straws), run_time=0.1)

        self.wait(2)

        self.play(FadeOut(horizontal_parallel_straws), run_time=0.1)

        # Bring in diagonal parallel straws (not allowed)
        self.play(FadeIn(diagonal_parallel_straws), run_time=0.1)

        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(diagonal_parallel_straws),
            run_time=0.1
        )