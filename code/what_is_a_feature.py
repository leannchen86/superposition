from manim import *
import numpy as np


class WhatIsAFeature(ThreeDScene):
    """Visualize five equally spaced 3-D vectors on a grid."""

    def construct(self):
        # Create a 2-D grid lying on the xy-plane (z = 0)
        start_distance = 8.0
        grid = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={"include_numbers": False},
        )
        # Golden ratio for well-distributed target directions
        phi = (1 + np.sqrt(5)) / 2
        target_directions = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [0, phi, 1/phi],
        ])
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        # Add vertical helper lines for depth perception
        vertical_lines = VGroup(
            *[
                Line(
                    start=grid.c2p(x, y, 0),
                    end=grid.c2p(x, y, 5),
                    color=BLUE_E,
                    stroke_width=1,
                    stroke_opacity=0.5,
                )
                for x in range(-5, 6)
                for y in range(-5, 6)
            ]
        )
        # 3-D axes
        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(0, 5, 1),
            x_length=10,
            y_length=10,
            z_length=5,
            axis_config={"color": WHITE, "include_tip": False, "include_numbers": False},
        )

        vectors = VGroup()
        vector_length = 2.0
        # Normalize target directions to unit length
        normalized_dirs = target_directions / np.linalg.norm(target_directions, axis=1, keepdims=True)
        for i, direction in enumerate(normalized_dirs):
            end_point = (direction * vector_length)
            vectors.add(Arrow3D(start=ORIGIN, end=end_point, color=colors[i % len(colors)]))

        start_distance = 8.0
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, distance=start_distance)

        # Create a 2-D grid lying on the xy-plane (z = 0)
        grid = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={"include_numbers": False},
        )

        # Golden ratio for well-distributed target directions
        phi = (1 + np.sqrt(5)) / 2
        target_directions = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [0, phi, 1/phi],
        ])
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]

        # Add vertical helper lines for depth perception
        vertical_lines = VGroup(
            *[
                Line(
                    start=grid.c2p(x, y, 0),
                    end=grid.c2p(x, y, 5),
                    color=BLUE_E,
                    stroke_width=1,
                    stroke_opacity=0.5,
                )
                for x in range(-5, 6)
                for y in range(-5, 6)
            ]
        )

        # 3-D axes
        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(0, 5, 1),
            x_length=10,
            y_length=10,
            z_length=5,
            axis_config={"color": WHITE, "include_tip": False, "include_numbers": False},
        )

        vectors = VGroup()
        vector_length = 2.0
        # Normalize target directions to unit length
        normalized_dirs = target_directions / np.linalg.norm(target_directions, axis=1, keepdims=True)
        for i, direction in enumerate(normalized_dirs):
            end_point = (direction * vector_length)
            vectors.add(Arrow3D(start=ORIGIN, end=end_point, color=colors[i % len(colors)]))

        # Add the static elements to the scene
        self.add(grid, vertical_lines, axes)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, distance=start_distance / 1.5, zoom=2.0, run_time=2)
        self.play(*[FadeIn(v) for v in vectors])   
        self.wait(1.5)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(3.5)
        feature_vectors = Tex(r'feature vectors', font_size=45, color=WHITE).move_to(LEFT + 1.3+ UP + 0.8)
        self.add_fixed_orientation_mobjects(feature_vectors)
        self.play(FadeIn(feature_vectors), run_time=1)
        self.wait(2)
        self.play(FadeOut(feature_vectors), run_time=0.5)
        self.wait(4.5)
        # Stop ambient camera rotation before zooming in on vectorsn
        self.stop_ambient_camera_rotation()
        # Dim all background elements and non-target vectors once
        background_elements = VGroup(grid, vertical_lines, axes)
        other_vectors = VGroup(*[v for i, v in enumerate(vectors) if i != 0])  # All except red
        self.play(background_elements.animate.set_opacity(0.1), other_vectors.animate.set_opacity(0.1), run_time=0.5)
        
        # the camera faces and zooms in on the red vector, and show the tex(r'positive sentiment')
        red_vector_pos = vectors[0].get_end()
        self.move_camera(frame_center=red_vector_pos, distance=0.5, run_time=1)
        positive_sentiment = Tex(r'positive sentiment', font_size=40, color=RED)
        positive_sentiment.move_to(red_vector_pos + UP * 0.03 + RIGHT * 0.3 + 0.5)
        self.add_fixed_orientation_mobjects(positive_sentiment)
        self.play(FadeIn(positive_sentiment), run_time=1)
        self.play(FadeOut(positive_sentiment), run_time=0.5)

        # Dim red vector, brighten yellow vector
        self.play(vectors[0].animate.set_opacity(0.1))
        
        # then the camera faces and zooms in on the yellow, and show the tex(r'warm color')
        yellow_vector_pos = vectors[3].get_end()
        warm_color = Tex(r'warm color', font_size=40, color=YELLOW)
        warm_color.move_to(yellow_vector_pos + UP * 0.01 + 0.3 + RIGHT * 0.08)
        self.add_fixed_orientation_mobjects(warm_color)
        self.move_camera(frame_center=yellow_vector_pos, distance=0.5, run_time=1)
        self.play(
            vectors[3].animate.set_opacity(1.0),
            FadeIn(warm_color),
            run_time=0.3)
        self.wait(0.5)
        self.play(FadeOut(warm_color), run_time=0.5)

        # Dim yellow vector, brighten green vector
        self.play(vectors[3].animate.set_opacity(0.1))
        
        # then the camera faces and zooms in on the green, and show the tex(r'has fur')
        green_vector_pos = vectors[2].get_end()
        self.move_camera(frame_center=green_vector_pos, distance=0.5, run_time=1)
        has_fur = Tex(r'has fur', font_size=40, color=GREEN)
        has_fur.move_to(green_vector_pos + UP * 0.7)
        self.add_fixed_orientation_mobjects(has_fur)
        self.play(
            vectors[2].animate.set_opacity(1.0),
            FadeIn(has_fur), 
            run_time=0.3)
        self.wait(0.5)
        self.play(FadeOut(has_fur), run_time=0.5)

        # Restore background elements and all vectors to full opacity
        self.play(
            background_elements.animate.set_opacity(1.0),
            *[vector.animate.set_opacity(1.0) for vector in vectors],
            run_time=1
        )

        # Zoom out way farther than the initial view
        final_distance = start_distance * 4.5  # Much farther than initial distance
        self.move_camera(frame_center=ORIGIN, distance=final_distance, run_time=2.5)
        self.wait(1.5)

        # then the camera faces and zooms in on the blue, and show the tex(r'furry animal')
        purple_vector_pos = vectors[4].get_end()
        self.move_camera(frame_center=purple_vector_pos, distance=0.5, run_time=1)
        # Dim other vectors, brighten purple vector
        self.play(background_elements.animate.set_opacity(0.1), *[v.animate.set_opacity(0.1) for v in vectors if v != vectors[4]])
        self.play(vectors[4].animate.set_opacity(1.0), run_time=0.3)
        furry_animal = Tex(r'furry animal', font_size=40, color=PURPLE)
        furry_animal.move_to(purple_vector_pos + UP * 0.7 + 0.2)
        self.add_fixed_orientation_mobjects(furry_animal)
        self.play(
            vectors[4].animate.set_opacity(1.0),
            FadeIn(furry_animal),
            run_time=0.3)
        self.wait(0.5)
        self.play(FadeOut(furry_animal), run_time=0.5)
        
        # Restore all elements to full opacity before final zoom out
        all_elements = VGroup(background_elements, *vectors)
        self.play(all_elements.animate.set_opacity(1.0), run_time=1)
        
        self.play(FadeOut(all_elements), run_time=1)

        # # Zoom out to show full scene
        self.move_camera(frame_center=ORIGIN, distance=start_distance, run_time=2)
        self.wait(2)
