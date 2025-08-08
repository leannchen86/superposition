from manim import *

class CoordinatePoints(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-0.5, 1.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            axis_config={
                "color": WHITE,
                "stroke_width": 2,
                "include_ticks": False,
            },
            tips=True,
        )
        
        # Add axis labels (ensure they stay on top)
        x_label = (
            MathTex("x", color=WHITE)
            .next_to(axes.x_axis.get_end(), DOWN, buff=0.4)
            .set_z_index(10)
        )
        y_label = (
            MathTex("y", color=WHITE)
            .next_to(axes.y_axis.get_end(), LEFT, buff=0.4)
            .set_z_index(10)
        )
        
        # Define points
        w1_coords = axes.coords_to_point(1, 0)
        w2_coords = axes.coords_to_point(0, 1)
        w3_coords = axes.coords_to_point(0.5, 0.5)
        origin = axes.coords_to_point(0, 0)
        
        # Create points
        w1_dot = Dot(w1_coords, color=WHITE, radius=0.06)
        w2_dot = Dot(w2_coords, color=WHITE, radius=0.06)
        w3_dot = Dot(w3_coords, color=WHITE, radius=0.06)
        
        # Create labels (keep above other mobjects)
        w1_label = (
            MathTex("W_1(1, 0)", color=WHITE, font_size=32)
            .next_to(w1_dot, DOWN, buff=0.2)
            .set_z_index(10)
        )
        w2_label = (
            MathTex("W_2(0, 1)", color=WHITE, font_size=32)
            .next_to(w2_dot, LEFT, buff=0.2)
            .set_z_index(10)
        )
        w3_label = (
            MathTex("W_3(0.5, 0.5)", color=WHITE, font_size=32)
            .next_to(w3_dot, UR, buff=0.2)
            .set_z_index(10)
        )
        
        # Create arrows from origin to W1, W2, and W3 with distinct colors
        arrow_to_w1 = Arrow(
            origin,
            w1_coords,
            color=RED,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_to_w2 = Arrow(
            origin,
            w2_coords,
            color=GREEN,
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow_to_w3 = Arrow(
            origin, 
            w3_coords, 
            color=BLUE, 
            stroke_width=2,
            buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        
        # Draw axes
        self.play(Create(axes), run_time=1.5)
        self.play(
            Write(x_label),
            Write(y_label),
            run_time=0.8
        )
        
        # Add W1
        self.play(
            Create(w1_dot),
            Write(w1_label),
            run_time=1
        )
        
        # Add W2
        self.play(
            Create(w2_dot),
            Write(w2_label),
            run_time=1
        )
        
        # Draw arrows to W1, W2, and W3
        self.play(GrowArrow(arrow_to_w1), run_time=1.0)
        self.play(GrowArrow(arrow_to_w2), run_time=1.0)
        self.play(GrowArrow(arrow_to_w3), run_time=1.2)
        
        # Add W3
        self.play(
            Create(w3_dot),
            Write(w3_label),
            run_time=1
        )
        
        # Hold final frame
        self.wait(2)
        

# To render this animation, save this code to a file (e.g., coordinate_points.py)
# and run: manim -pql coordinate_points.py CoordinatePoints
# For higher quality: manim -pqh coordinate_points.py CoordinatePoints