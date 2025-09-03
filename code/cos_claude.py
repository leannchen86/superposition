from manim import *
import numpy as np

class VectorCosineAnimation(Scene):
    def construct(self):
        # Set up coordinate system
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1, 3, 1],
            x_length=6,
            y_length=4,
            axis_config={"color": GRAY_D, "stroke_width": 3},
            tips=True
        )
        # Axis labels
        x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT)
        y_label = axes.get_y_axis_label("y", edge=UP, direction=UP)
        # Vector properties
        vector_length = 2.5
        origin = axes.c2p(0, 0)
        # Initial vector at 0 degrees
        initial_end = axes.c2p(vector_length, 0)
        vector = Arrow(origin, initial_end, color=RED, stroke_width=4, buff=0)
        # Angle arc and text
        angle_arc = Arc(radius=0.5, start_angle=0, angle=0, color=BLUE, stroke_width=2)
        angle_arc.move_arc_center_to(origin)
        angle_text = Text("θ = 0°", font_size=20, color=BLUE)
        # Position text at radius 0.8 along the 0-degree direction initially
        angle_text.move_to(axes.c2p(0.8, 0.1))
        # Initial projection highlight (invisible initially)
        projection_highlight = Line(
            origin, 
            axes.c2p(vector_length, 0), 
            color=BLUE, 
            stroke_width=6
        )
        projection_highlight.set_opacity(0)
        # Projection line (invisible initially) 
        projection_line = DashedLine(
            initial_end,
            axes.c2p(vector_length, 0),
            color=BLUE,
            stroke_width=2
        )
        projection_line.set_opacity(0)
        # Step 1: FadeIn initial setup (1.5s)
        # Angles to animate through
        angles = [18, 36, 54, 72, 90]
        # Steps 2-6: Rotate vector and show projections (7s total, ~1.4s each)
        for i, angle in enumerate(angles):
            # Calculate new vector end point
            radians = np.radians(angle)
            new_end = axes.c2p(
                vector_length * np.cos(radians),
                vector_length * np.sin(radians)
            )
            # Calculate projection point on x-axis
            projection_point = axes.c2p(vector_length * np.cos(radians), 0)
            # Create new vector and projection elements
            new_vector = Arrow(origin, new_end, color=RED, stroke_width=4, buff=0)
            # Create new angle arc and text
            new_angle_arc = Arc(radius=0.5, start_angle=0, angle=radians, color=BLUE, stroke_width=2)
            new_angle_arc.move_arc_center_to(origin)
            new_angle_text = Text(f"θ = {angle}°", font_size=20, color=BLUE)
            # Position text at the midpoint of the arc angle
            mid_angle = radians / 2
            text_radius = 0.8
            text_x = text_radius * np.cos(mid_angle)
            text_y = text_radius * np.sin(mid_angle)
            new_angle_text.move_to(axes.c2p(text_x, text_y))
            new_projection_line = DashedLine(
                new_end,
                projection_point,
                color=BLUE,
                stroke_width=2
            )
            new_projection_highlight = Line(
                origin,
                projection_point,
                color=BLUE,
                stroke_width=6
            )
            # Animate transformations
            animations = [
                Transform(vector, new_vector),
                Transform(angle_arc, new_angle_arc),
                Transform(angle_text, new_angle_text),
            ]
            # For the first rotation, fade in the projection elements
            if i == 0:
                animations.extend([
                    FadeIn(projection_line),
                    FadeIn(projection_highlight)
                ])
                animations.extend([
                    Transform(projection_line, new_projection_line),
                    Transform(projection_highlight, new_projection_highlight)
                ])
            else:
                animations.extend([
                    Transform(projection_line, new_projection_line),
                    Transform(projection_highlight, new_projection_highlight)
                ])
        # Step 7: FadeOut everything (1.5s)

        # Animation sequence - all self.play calls at the end
        self.play(
            FadeIn(axes),
            FadeIn(x_label),
            FadeIn(y_label),
            FadeIn(vector),
            FadeIn(angle_arc),
            FadeIn(angle_text),
            run_time=1.5
        )
        self.play(*animations, run_time=1.4)
        self.play(
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label),
            FadeOut(vector),
            FadeOut(angle_arc),
            FadeOut(angle_text),   
            FadeOut(projection_line),
            FadeOut(projection_highlight),
            run_time=1.5
        )
# To render this animation, save this file as vector_cosine.py and run:
# manim -pql vector_cosine.py VectorCosineAnimation
# 
# For higher quality:
# manim -pqh vector_cosine.py VectorCosineAnimation