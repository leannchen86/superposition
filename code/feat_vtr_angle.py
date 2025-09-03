from manim import *
import numpy as np

class SuperpositionAnimation(Scene):
    def construct(self):
        # Set up the scene layout
        left_center = LEFT * 2.5
        right_center = RIGHT * 4

        # Create axes for loss plot
        loss_axes = Axes(
            x_range=[0, 50, 10],
            y_range=[1.2, 1.6, 0.1],
            x_length=5,
            y_length=3,
            axis_config={"color": GRAY},
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": [0, 10, 20, 30, 40, 50]
            },
            y_axis_config={
                "include_numbers": True,
                "numbers_to_include": [1.2, 1.3, 1.4, 1.5, 1.6],
                "decimal_number_config": {"num_decimal_places": 2}
            }
        )
        loss_axes.move_to(left_center + DOWN * 0.5)

        # Labels for loss plot
        loss_x_label = Tex("Training Step", font_size=35)
        loss_x_label.next_to(loss_axes, DOWN)
        loss_y_label = Tex("Loss", font_size=35)
        loss_y_label.next_to(loss_axes, LEFT).rotate(PI / 2)

        # Step counter
        step_text = Tex(r"Step: 0", font_size=35)
        step_text.move_to(np.array([right_center[0], step_text.get_y(), 0]))
        step_text.align_to(loss_x_label, DOWN)

        # Add static elements
        self.add(loss_axes, loss_x_label, loss_y_label)

        # Generate loss data (sharper early drop, flatter & higher tail after 20)
        steps = np.linspace(0, 50, 300)
        # Mixture of exponentials to create a sharp initial decline and a higher, flatter tail
        base_loss = 0.32 * np.exp(-steps / 6) + 0.05 * np.exp(-steps / 28) + 1.26
        # Keep some sharpness after ~20 steps but with smaller magnitude so the curve stays higher
        t_post20 = np.maximum(steps - 20.0, 0.0)
        extra_post20_drop = 0.008 * (1.0 - np.exp(-t_post20 / 6.0))
        base_loss = base_loss - extra_post20_drop
        # Deterministic, decaying noise with mixed frequencies; slightly reduced jitter to avoid touching the bottom
        rng = np.random.default_rng(0)
        harmonic_noise = (0.035 * np.sin(1.4 * steps) + 0.02 * np.sin(0.25 * steps + 1.2)) * np.exp(-steps / 24)
        jitter_noise = 0.006 * np.exp(-steps / 16) * rng.standard_normal(steps.shape)
        loss_values = base_loss + harmonic_noise + jitter_noise
        # Keep a higher floor to avoid touching the bottom axis
        loss_values = np.clip(loss_values, 1.25, 1.6)
        # Enforce a flat/non-increasing tail after step 20 so it doesn't slope upward
        tail_start_idx = np.searchsorted(steps, 20.0)
        if tail_start_idx < len(loss_values):
            loss_values[tail_start_idx:] = np.minimum.accumulate(loss_values[tail_start_idx:])

        # Create initial feature vectors (random angles)
        num_features = 5
        initial_angles = [0.2, 1.1, 2.8, 4.5, 5.9]
        final_angles = [i * 2 * PI / num_features for i in range(num_features)]

        # Create circle for feature vectors
        feature_circle = Circle(radius=2.7, color=GRAY)
        feature_circle.move_to(right_center)

        # Create feature vectors
        feature_vectors = VGroup()
        for i in range(num_features):
            vector = Arrow(
                start=feature_circle.get_center(),
                end=feature_circle.get_center() + 2.7 * np.array([np.cos(initial_angles[i]), np.sin(initial_angles[i]), 0]),
                color=interpolate_color(RED, BLUE, i / num_features),
                stroke_width=4,
                max_tip_length_to_length_ratio=0.1
            )
            feature_vectors.add(vector)

        self.add(feature_vectors, step_text)

        # Create loss curve with a valid initial segment (avoid empty points)
        loss_curve = VMobject(color=RED, stroke_width=4)
        initial_curve_points = [
            loss_axes.coords_to_point(steps[0], loss_values[0]),
            loss_axes.coords_to_point(steps[1], loss_values[1]),
        ]
        loss_curve.set_points_as_corners(initial_curve_points)
        self.add(loss_curve)

        # Animation update functions
        def update_line(mob, alpha):
            points = [loss_axes.coords_to_point(steps[i], loss_values[i]) for i in range(len(steps))]
            accelerated_alpha = alpha ** 0.5
            num_points = int(accelerated_alpha * len(points))

            if num_points < 2:
                return

            current_points = points[:num_points]
            mob.set_points_as_corners(current_points)
            mob.set_stroke(RED, width=4)

            # Update step text in sync with curve progress
            current_step = int(accelerated_alpha * 50)
            step_text.become(Tex(f"Step: {current_step}", font_size=35))
            step_text.move_to(np.array([right_center[0], loss_x_label.get_y(), 0]))
            step_text.align_to(loss_x_label, DOWN)

        def update_feature_vectors(mob, alpha):
            accelerated_alpha = alpha ** 0.5

            for i, vector in enumerate(mob):
                current_angle = interpolate(initial_angles[i], final_angles[i], alpha)
                new_end = feature_circle.get_center() + 2.7 * np.array([
                    np.cos(current_angle),
                    np.sin(current_angle),
                    0
                ])
                new_vector = Arrow(
                    start=feature_circle.get_center(),
                    end=new_end,
                    color=interpolate_color(RED, BLUE, i / num_features),
                    stroke_width=4,
                    max_tip_length_to_length_ratio=0.1
                )
                vector.become(new_vector)

        # Run the animation
        self.play(
            UpdateFromAlphaFunc(loss_curve, update_line),
            UpdateFromAlphaFunc(feature_vectors, update_feature_vectors),
            run_time=3,
            rate_func=linear
        )

        self.wait(1)

# To render this animation, save this code as a .py file and run:
# manim -pql filename.py SuperpositionAnimation
# For higher quality: manim -pqh filename.py SuperpositionAnimation
