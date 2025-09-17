from manim import *
try:
    from manim.utils.color import Color  # Manim Community v0.19
except Exception:
    Color = None
import numpy as np


# Ensure commonly used color constants exist even if not provided by Manim version
def _color(value: str):
    return Color(value) if Color is not None else value

if 'CYAN' not in globals():
    CYAN = _color("#00FFFF")
if 'MAGENTA' not in globals():
    MAGENTA = _color("#FF00FF")
if 'ORANGE' not in globals():
    ORANGE = _color("#FFA500")
if 'TEAL' not in globals():
    TEAL = _color("#008080")
if 'LAVENDER' not in globals():
    LAVENDER = _color("#E6E6FA")
if 'GREY' not in globals():
    GREY = _color("#808080")
if 'WHITE' not in globals():
    WHITE = _color("#FFFFFF")
if 'BLUE_E' not in globals():
    BLUE_E = _color("#1C75E9")

class BirdViewVectors(ThreeDScene):
    """Visualize five equally spaced 3-D vectors on a grid with fixed bird's eye view."""

    def construct(self):
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

        # Golden ratio for well-distributed target directions
        phi = (1 + np.sqrt(5)) / 2
        target_directions = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [0, phi, 1/phi],
        ])
        colors = [CYAN, MAGENTA, ORANGE, TEAL, LAVENDER]

        vectors = VGroup()
        vector_length = 2.0
        # Normalize target directions to unit length
        normalized_dirs = target_directions / np.linalg.norm(target_directions, axis=1, keepdims=True)
        for i, direction in enumerate(normalized_dirs):
            end_point = (direction * vector_length)
            vectors.add(Arrow3D(start=ORIGIN, end=end_point, color=colors[i % len(colors)]))

        # Set fixed bird's eye view camera orientation
        self.set_camera_orientation(phi=80 * DEGREES, theta=0 * DEGREES, distance=12.0)

        # Start very slow ambient camera rotation
        self.begin_ambient_camera_rotation(rate=0.05)
        
        # Add all elements to the scene with dim/gray effect from the beginning
        background_elements = VGroup(grid, vertical_lines, axes)
        background_elements.set_color(GREY).set_opacity(0.35)
        for vector in vectors:
            vector.set_color(GREY).set_opacity(0.35)
        
        self.add(background_elements, vectors)
        self.wait(5)
        
        # Light up vectors one at a time (1 second each)
        original_colors = [CYAN, MAGENTA, ORANGE, TEAL, LAVENDER]
        
        for i, (vector, color) in enumerate(zip(vectors, original_colors)):
            animations = [vector.animate.set_color(color).set_opacity(1.0)]
            
            # Dim the previous vector if not the first one
            if i > 0:
                prev_vector = vectors[i-1]
                animations.append(prev_vector.animate.set_color(GREY).set_opacity(0.35))
            
            self.play(*animations, run_time=1)
        
        # Keep the last vector lit for a short duration
        self.wait(1)



# self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, distance=start_distance)
# self.add_fixed_orientation_mobjects
