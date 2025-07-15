from manim import *

class VectorRotationProjection(Scene):
    def construct(self):
        # Set up the coordinate system
        axes = Axes(
            x_range=[0, 1.5, 0.5],
            y_range=[0, 1.5, 0.5],
            x_length=5,
            y_length=5,
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        
        # Add axis labels
        x_label = MathTex("x").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = MathTex("y").next_to(axes.y_axis.get_end(), UP)
        
        # Initial vector at 0 degrees (pointing right)
        vector_length = 4
        initial_vector = Arrow(
            start=axes.get_origin(),
            end=axes.get_origin() + RIGHT * vector_length,
            color=RED,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.1
        )
        
        # Step 1: Fade in axes and initial vector
        self.play(
            FadeIn(axes),
            FadeIn(x_label),
            FadeIn(y_label)
        )
        self.play(FadeIn(initial_vector))
        self.wait(1)
        
        # Function to create projection elements
        def create_projection_elements(angle_deg):
            angle_rad = angle_deg * PI / 180
            
            # Vector end point
            vector_end = axes.get_origin() + vector_length * np.array([np.cos(angle_rad), np.sin(angle_rad), 0])
            
            # Projection point on x-axis
            projection_point = axes.get_origin() + vector_length * np.cos(angle_rad) * RIGHT
            
            # Dotted line from vector end to projection point
            dotted_line = DashedLine(
                start=vector_end,
                end=projection_point,
                color=BLUE,
                stroke_width=2
            )
            
            # Highlight the projection on x-axis
            if angle_deg < 90:
                projection_highlight = Line(
                    start=axes.get_origin(),
                    end=projection_point,
                    color=GREEN,
                    stroke_width=6
                )
            else:
                # At 90 degrees, no projection on x-axis
                projection_highlight = VGroup()
            
            # Angle arc
            if angle_deg > 0:
                angle_arc = Arc(
                    radius=0.5,
                    start_angle=0,
                    angle=angle_rad,
                    color=YELLOW,
                    stroke_width=2
                )
                angle_arc.move_arc_center_to(axes.get_origin())
                
                # Angle label
                angle_label = MathTex(f"{angle_deg}°").scale(0.7)
                label_position = axes.get_origin() + 0.8 * np.array([np.cos(angle_rad/2), np.sin(angle_rad/2), 0])
                angle_label.move_to(label_position)
            else:
                angle_arc = VGroup()
                angle_label = VGroup()
            
            return vector_end, dotted_line, projection_highlight, angle_arc, angle_label
        
        # Animation for each angle
        angles = [18, 36, 54, 72, 90]
        current_projections = VGroup()
        current_angle_elements = VGroup()
        
        for angle in angles:
            vector_end, dotted_line, projection_highlight, angle_arc, angle_label = create_projection_elements(angle)
            
            # New vector
            new_vector = Arrow(
                start=axes.get_origin(),
                end=vector_end,
                color=RED,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.1
            )
            
            # Fade out previous projection elements
            if len(current_projections) > 0:
                self.play(FadeOut(current_projections), run_time=0.5)
            if len(current_angle_elements) > 0:
                self.play(FadeOut(current_angle_elements), run_time=0.5)
            
            # Rotate vector and add new elements
            self.play(
                Transform(initial_vector, new_vector),
                run_time=1
            )
            
            # Add projection elements
            new_elements = VGroup()
            if len(projection_highlight) > 0:
                new_elements.add(projection_highlight)
            if len(dotted_line) > 0:
                new_elements.add(dotted_line)
            
            angle_elements = VGroup()
            if len(angle_arc) > 0:
                angle_elements.add(angle_arc)
            if len(angle_label) > 0:
                angle_elements.add(angle_label)
            
            if len(new_elements) > 0:
                self.play(FadeIn(new_elements), run_time=0.8)
                current_projections = new_elements
            
            if len(angle_elements) > 0:
                self.play(FadeIn(angle_elements), run_time=0.8)
                current_angle_elements = angle_elements
            
            self.wait(1.5)
        
        # Step 7: Fade out everything
        all_objects = VGroup(
            axes, x_label, y_label, initial_vector, 
            current_projections, current_angle_elements
        )
        self.play(FadeOut(all_objects))
        self.wait(1)

# To render this animation, save the file and run:
# manim -pql filename.py VectorRotationProjection
# 
# For higher quality:
# manim -pqh filename.py VectorRotationProjection