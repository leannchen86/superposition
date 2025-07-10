from manim import *
import numpy as np

class SuperpositionAnimation(Scene):
    def construct(self):
        # Set up the scene layout
        left_center = LEFT * 3.5
        right_center = RIGHT * 3.5
        
        # Title
        title = Text("Toy Models of Superposition: Feature Learning", font_size=24)
        title.to_edge(UP)
        self.add(title)
        
        # Left side: Loss chart
        loss_title = Text("Reconstruction Loss", font_size=20)
        loss_title.move_to(left_center + UP * 2.5)
        
        # Create axes for loss plot
        loss_axes = Axes(
            x_range=[0, 50, 10],
            y_range=[0.12, 0.22, 0.02],
            x_length=5,
            y_length=3,
            axis_config={"color": GRAY},
            x_axis_config={"numbers_to_include": [0, 10, 20, 30, 40, 50]},
            y_axis_config={"numbers_to_include": [0.12, 0.14, 0.16, 0.18, 0.20, 0.22]}
        )
        loss_axes.move_to(left_center + DOWN * 0.5)
        
        # Labels for loss plot
        loss_x_label = Text("Training Step", font_size=14)
        loss_x_label.next_to(loss_axes, DOWN)
        loss_y_label = Text("Loss", font_size=14)
        loss_y_label.next_to(loss_axes, LEFT).rotate(PI/2)
        
        # Right side: Feature vectors
        feature_title = Text("Feature Vector Angles", font_size=20)
        feature_title.move_to(right_center + UP * 2.5)
        
        # Create circle for feature vectors
        feature_circle = Circle(radius=1.5, color=GRAY)
        feature_circle.move_to(right_center)
        
        # Step counter
        step_text = Text("Step: 0", font_size=16)
        step_text.move_to(right_center + DOWN * 2.5)
        
        # Add static elements
        self.add(loss_title, loss_axes, loss_x_label, loss_y_label)
        self.add(feature_title, feature_circle, step_text)
        
        # Generate loss data (decreasing with noise)
        steps = np.linspace(0, 50, 100)
        base_loss = 0.22 * np.exp(-steps/15) + 0.13
        noise = 0.005 * np.sin(steps * 0.8) * np.exp(-steps/20)
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
        
        def update_loss_curve(mob, alpha):
            # Clear the curve
            mob.clear_points()
            
            # Calculate how many points to show
            points_to_show = int(alpha * num_points)
            if points_to_show < 2:
                return
            
            # Create the curve up to current point
            current_steps = steps[:points_to_show]
            current_losses = loss_values[:points_to_show]
            
            # Convert to axes coordinates
            points = [loss_axes.coords_to_point(s, l) for s, l in zip(current_steps, current_losses)]
            
            # Create the curve
            if len(points) > 1:
                mob.set_points_smoothly(points)
        
        def update_feature_vectors(mob, alpha):
            current_step = int(alpha * 50)
            step_text.become(Text(f"Step: {current_step}", font_size=16))
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
            UpdateFromAlphaFunc(loss_curve, update_loss_curve),
            UpdateFromAlphaFunc(feature_vectors, update_feature_vectors),
            run_time=total_time,
            rate_func=smooth
        )
        
        # Hold the final frame
        self.wait(2)
        
        # Add final annotations
        final_loss_text = Text(f"Final Loss: {loss_values[-1]:.3f}", font_size=14)
        final_loss_text.move_to(left_center + DOWN * 2.5)
        
        angle_text = Text("Evenly Spaced\n(72° apart)", font_size=14)
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