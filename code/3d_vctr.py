from manim import *
import numpy as np

class Vectors3D(ThreeDScene):
    def construct(self):
        # Set up the 3D axes
        axes = ThreeDAxes(
            x_range=[-2, 3, 1],
            y_range=[-1, 4, 1],
            z_range=[-3, 4, 1],
            x_length=6,
            y_length=7,
            z_length=7,
        )
        
        # XY-plane grid and vertical helper lines (like in what_is_a_feature.py)
        grid = NumberPlane(
            x_range=(-2, 3, 1),
            y_range=(-1, 4, 1),
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
                    start=grid.c2p(x, y, -3),
                    end=grid.c2p(x, y, 4),
                    color=BLUE_E,
                    stroke_width=1,
                    stroke_opacity=0.3,
                )
                for x in range(-2, 4)
                for y in range(-1, 5)
            ]
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y"))
        z_label = axes.get_z_axis_label(Tex("z"))
        
        # Define vector coordinates
        vector_a_coords = [2, 1, -2]
        vector_b_coords = [1, 3, 1]
        vector_c_coords = [-1, 2, 3]
        
        # Compute the axes' origin in scene coordinates
        origin = axes.coords_to_point(0, 0, 0)

        # Create vectors as arrows from origin
        vector_a = Arrow3D(
            start=origin, 
            end=axes.coords_to_point(*vector_a_coords),
            color=RED,
            thickness=0.02,
            height=0.3,
            base_radius=0.05
        )
        
        vector_b = Arrow3D(
            start=origin,
            end=axes.coords_to_point(*vector_b_coords),
            color=GREEN,
            thickness=0.02,
            height=0.3,
            base_radius=0.05
        )
        
        vector_c = Arrow3D(
            start=origin,
            end=axes.coords_to_point(*vector_c_coords),
            color=BLUE,
            thickness=0.02,
            height=0.3,
            base_radius=0.05
        )
        
        # Create labels that always face the camera (billboard-style)
        label_a = always_redraw(
            lambda: Tex(r"$\vec{a}(2, 1, -2)$", color=RED)
            .scale(0.8)
            .move_to(axes.coords_to_point(*vector_a_coords) + np.array([0.25, 0.15, 0.2]))
            .rotate(-self.camera.get_phi(), axis=RIGHT)
            .rotate(self.camera.get_theta(), axis=UP)
            .rotate(PI, axis=OUT)
        )

        label_b = always_redraw(
            lambda: Tex(r"$\vec{b}(1, 3, 1)$", color=GREEN)
            .scale(0.8)
            .move_to(axes.coords_to_point(*vector_b_coords) + np.array([0.2, 0.25, 0.2]))
            .rotate(-self.camera.get_phi(), axis=RIGHT)
            .rotate(self.camera.get_theta(), axis=UP)
            .rotate(PI, axis=OUT)
        )

        label_c = always_redraw(
            lambda: Tex(r"$\vec{c}(-1, 2, 3)$", color=BLUE)
            .scale(0.8)
            .move_to(axes.coords_to_point(*vector_c_coords) + np.array([-0.25, 0.2, 0.2]))
            .rotate(-self.camera.get_phi(), axis=RIGHT)
            .rotate(self.camera.get_theta(), axis=UP)
            .rotate(PI, axis=OUT)
        )
        
        # Set camera orientation for better 3D view
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        
        # Add title
        title = Text("3D Vector Space", font_size=36).to_edge(UP)
        
        # Animation sequence - all self.play calls at the end
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(grid), FadeIn(vertical_lines), Create(axes), Write(x_label), Write(y_label), Write(z_label))
        self.wait(1)
        
        # Add vectors one by one
        self.play(FadeIn(vector_a), FadeIn(label_a))
        self.wait(0.5)
        
        self.play(FadeIn(vector_b), FadeIn(label_b))
        self.wait(0.5)
        
        self.play(FadeIn(vector_c), FadeIn(label_c))
        self.wait(1)
        
        # Rotate camera around the scene
        self.begin_ambient_camera_rotation(rate=0.3)
        # self.wait(8)
        self.stop_ambient_camera_rotation()

        
        # Final camera position
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.wait(2)