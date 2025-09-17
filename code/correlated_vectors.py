from manim import *
import numpy as np

class CorrelatedVectorsBias(ThreeDScene):
    """Show 2 correlated vectors, evolve equation, and bias shift one to opposite position."""

    def construct(self):
        # ============= OBJECT CREATION =============
        
        # Create 3D space
        grid = NumberPlane(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={"include_numbers": False},
        )

        vertical_lines = VGroup(
            *[
                Line(
                    start=grid.c2p(x, y, 0),
                    end=grid.c2p(x, y, 3),
                    color=BLUE_E,
                    stroke_width=1,
                    stroke_opacity=0.5,
                )
                for x in range(-3, 4)
                for y in range(-3, 4)
            ]
        )

        axes = ThreeDAxes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            z_range=(-3, 3, 1),
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"color": WHITE, "include_tip": False, "include_numbers": False},
        )

        background_elements = VGroup(grid, vertical_lines, axes)
        background_elements.set_color(GREY).set_opacity(0.4)
        
        # Create vectors with more separation like in zoom_vectors.py
        vector_length = 2.0
        vec1_direction = np.array([1, 1, 1])  # More separated direction
        vec2_direction = np.array([0, (1 + np.sqrt(5)) / 2, 1/((1 + np.sqrt(5)) / 2)])  # Golden ratio like zoom_vectors
        
        vec1_normalized = vec1_direction / np.linalg.norm(vec1_direction)
        vec2_normalized = vec2_direction / np.linalg.norm(vec2_direction)
        
        vec1_end = vec1_normalized * vector_length
        vec2_end = vec2_normalized * vector_length
        
        vector_1 = Arrow3D(start=ORIGIN, end=vec1_end, color=RED)
        vector_2 = Arrow3D(start=ORIGIN, end=vec2_end, color=BLUE)
        
        # Create labels
        ml_text = Tex(r'machine learning', font_size=30, color=RED).next_to(vector_1.get_end(), UP*1.2, buff=0.8)
        ai_text = Tex(r'artificial intelligence', font_size=30, color=BLUE).next_to(vector_2.get_end(), UP*1.2, buff=1.2)
        
        # Create equations with separate parts for selective highlighting
        equation = MathTex(
            r"h = W^{\top}Wx",
            r"+b",
            font_size=40,
            color=WHITE,
        ).move_to([2.5, 3.5, -0.5])  # Position between x and y axis
        opposite_position = -vec1_end
        
        # Reference the parts for highlighting
        main_equation = equation[0]
        bias_term = equation[1]
        
        # Create explanation
        explanation = Tex(
            r"Bias shifts vector to opposite direction\\where ReLU will suppress it",
            font_size=30,
            color=WHITE
        )  # Will be placed as a fixed overlay in the upper-left corner
        
        # ============= ANIMATIONS =============

        # Center on origin so axes are in the middle, then pan to focus
        self.move_camera(
            frame_center=ORIGIN,
            phi=80 * DEGREES,
            theta=0 * DEGREES,
            distance=8.0,
            zoom=1.2,
            run_time=0.001
        )
        self.add(background_elements)
        self.wait(1)
        # Show vectors
        self.play(FadeIn(vector_1), FadeIn(vector_2), run_time=1.5)
        
        # Add vector labels
        self.add_fixed_orientation_mobjects(ml_text, ai_text)
        self.play(FadeIn(ml_text), FadeIn(ai_text))
        self.wait(2)

        # Show initial equation (fix the whole equation's orientation so both parts stay aligned)
        self.add_fixed_orientation_mobjects(equation)
        self.wait(2)

        # Transform equation and shift vector; simultaneously highlight bias then return to original size
        self.play(
            AnimationGroup(
                AnimationGroup(
                    vector_2.animate.put_start_and_end_on(ORIGIN, opposite_position),
                    ai_text.animate.next_to(opposite_position, UP*1.2, buff=1.2),
                    lag_ratio=0.0,
                    run_time=2.5,
                ),
                Succession(
                    AnimationGroup(
                        ApplyMethod(bias_term.set_color, YELLOW),
                        ApplyMethod(bias_term.scale, 1.2),
                        lag_ratio=0.0,
                        run_time=2.0,
                    ),
                    ApplyMethod(bias_term.scale, 1/1.2, run_time=1.5),
                    Wait(run_time=1.5),
                ),
                lag_ratio=0.0,
            ),
            run_time=2.5,
        )
        # Update label for shifted vector
        self.add_fixed_orientation_mobjects(explanation)
        explanation.move_to([0, -2.8, 1.2])  # Move to middle between x and z axis
        self.play(
            FadeIn(explanation),
            run_time=1
        )
        self.wait(1)