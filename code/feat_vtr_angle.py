from manim import *
import numpy as np

class SuperpositionAnimation(Scene):
    def construct(self):
        # Set up the scene layout
        left_center = LEFT * 3.5
        right_center = RIGHT * 3.5

        # Left side: Loss chart
        loss_title = Tex(r"Reconstruction Loss", font_size=20)
        loss_title.move_to(left_center + UP * 2.5)
        
        # Create axes for loss plot
        loss_axes = Axes(
            x_range=[0, 50, 10],
            y_range=[0.12, 0.22, 0.02],
            x_length=5,
            y_length=3,
            axis_config={"color": GRAY},
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0, 10, 20, 30, 40, 50]
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0.12, 0.14, 0.16, 0.18, 0.20, 0.22],
                "decimal_number_config": {"num_decimal_places": 2}
            }
        )
        loss_axes.move_to(left_center + DOWN * 0.5)
        
        # Labels for loss plot
        loss_x_label = Tex("Training Step", font_size=14)
        loss_x_label.next_to(loss_axes, DOWN)
        loss_y_label = Tex("Loss", font_size=14)
        loss_y_label.next_to(loss_axes, LEFT).rotate(PI/2)
        
        # Right side: Feature vectors
        feature_title = Tex(r"Feature Vector Angles", font_size=20)
        feature_title.move_to(right_center + UP * 2.5)
        
        # Create circle for feature vectors
        feature_circle = Circle(radius=1.5, color=GRAY)
        feature_circle.move_to(right_center)
        
        # Step counter
        step_text = Tex(r"Step: 0", font_size=16)
        step_text.move_to(right_center + DOWN * 2.5)
        
        # Add static elements
        self.add(loss_title, loss_axes, loss_x_label, loss_y_label)
        self.add(feature_title, feature_circle, step_text)
        
        # Generate loss data (decreasing with noise)
        steps = np.linspace(0, 50, 100)
        base_loss = 0.09 * np.exp(-steps/15) + 0.13
        noise = 0.02 * np.sin(steps * 0.8) * np.exp(-steps/20)
        loss_values = base_loss + noise
        
        # Create initial feature vectors (random angles)
        num_features = 5
        initial_angles = [0.2, 1.1, 2.8, 4.5, 5.9]  # Somewhat random initial positions
        final_angles = [i * 2 * PI / num_features for i in range(num_features)]  # Evenly spaced
        
        # Create feature vectors
        feature_vectors = VGroup()
        for i in range(num_features):
            vector = Arrow(
                start=feature_circle.get_center(),
                end=feature_circle.get_center() + 1.5 * np.array([np.cos(initial_angles[i]), np.sin(initial_angles[i]), 0]),
                color=interpolate_color(RED, BLUE, i/num_features),
                stroke_width=4,
                max_tip_length_to_length_ratio=0.1
            )
            feature_vectors.add(vector)
        
        self.add(feature_vectors)
        
        # Create loss curve (initially empty)
        loss_curve = VMobject()
        loss_curve.set_color(YELLOW)
        self.add(loss_curve)
        
        # Animation parameters
        total_time = 8
        num_points = len(steps)

        # Create the animated line using UpdateFromAlphaFunc
        animated_line = VMobject()
        
        def update_line(mob, alpha):
            # Clear the mobject
            mob.clear_points()

            # Convert data points to axes coordinates
            points = [loss_axes.coords_to_point(steps[i], loss_values[i]) for i in range(len(steps))]
            
            # Calculate how many points to show based on alpha
            num_points = int(alpha * len(points))
            
            if num_points >= 2:
                # Create line segments connecting points with sharp corners
                current_points = points[:num_points]
                
                # Start with the first point
                mob.start_new_path(current_points[0])
                
                # Add line segments to each subsequent point
                for i in range(1, len(current_points)):
                    mob.add_line_to(current_points[i])
                
                # Set stroke properties for sharp corners
                mob.set_stroke(RED, width=3)
                mob.set_fill(opacity=0)

        # Apply the update function
        animated_line.add_updater(lambda mob, dt: None)  # Dummy updater to make it animatable
        
        def update_feature_vectors(mob, alpha):
            current_step = int(alpha * 50)
            step_text.become(Tex(f"Step: {current_step}", font_size=16))
            step_text.move_to(right_center + DOWN * 2.5)
            
            for i, vector in enumerate(mob):
                # Interpolate between initial and final angles
                current_angle = interpolate(initial_angles[i], final_angles[i], 
                                          smooth(alpha))  # smooth function for easing
                
                # Update vector direction
                new_end = feature_circle.get_center() + 1.5 * np.array([
                    np.cos(current_angle), 
                    np.sin(current_angle), 
                    0
                ])
                
                # Recreate the arrow with new direction
                new_vector = Arrow(
                    start=feature_circle.get_center(),
                    end=new_end,
                    color=interpolate_color(RED, BLUE, i/num_features),
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.1
                )
                vector.become(new_vector)
        
        # Run the animation
        self.play(
            UpdateFromAlphaFunc(animated_line, update_line),
            # UpdateFromAlphaFunc(loss_curve, update_loss_curve),
            UpdateFromAlphaFunc(feature_vectors, update_feature_vectors),
            run_time=total_time,
            rate_func=smooth
        )
        
        # Hold the final frame
        self.wait(2)
        
        # Add final annotations
        final_loss_text = Tex(f"Final Loss: {loss_values[-1]:.3f}", font_size=14)
        final_loss_text.move_to(left_center + DOWN * 2.5)
        
        angle_text = Tex("Evenly Spaced\n(72° apart)", font_size=14)
        angle_text.move_to(right_center + DOWN * 2)
        
        self.play(
            Write(final_loss_text),
            Write(angle_text)
        )
        
        self.wait(3)

# To render this animation, save this code as a .py file and run:
# manim -pql filename.py SuperpositionAnimation
# 
# For higher quality:
# manim -pqh filename.py SuperpositionAnimation