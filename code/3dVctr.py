from manim import *
import numpy as np

class VectorProjection3Dto2D(ThreeDScene):
    def construct(self):
        # Set up the 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # Define the original 3D vector and the projected 2D vector
        vector_3d = np.array([0.3, 0.7, 0.6])
        vector_2d = np.array([0.6, 1.0, 0])  # Adding 0 for z-component in 3D space
        
        # Create 3D axes
        axes_3d = ThreeDAxes(
            x_range=[-0.5, 1.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            z_range=[-0.5, 1.5, 0.5],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # Add axis labels for 3D
        x_label_3d = axes_3d.get_x_axis_label(Tex("x"))
        y_label_3d = axes_3d.get_y_axis_label(Tex("y"))
        z_label_3d = axes_3d.get_z_axis_label(Tex("z"))
        
        # Create the 3D vector
        vector_3d_arrow = Arrow3D(
            start=axes_3d.coords_to_point(0, 0, 0),
            end=axes_3d.coords_to_point(*vector_3d),
            color=BLUE,
            stroke_width=8
        )
        
        # Create vector label
        vector_3d_label = MathTex(r"\vec{v}_{3D} = \begin{bmatrix} 0.3 \\ 0.7 \\ 0.6 \end{bmatrix}")
        vector_3d_label.rotate(PI/2, axis=RIGHT)
        vector_3d_label.rotate(PI/4, axis=OUT)
        vector_3d_label.next_to(vector_3d_arrow.get_end(), UP)
        
        # Title
        title = Text("3D Vector Projection to 2D", font_size=36)
        title.to_edge(UP)
        # Fixed-in-frame handled via add_fixed_in_frame_mobjects
        
        # Scene 1: Show 3D vector
        self.add_fixed_in_frame_mobjects(title)
        self.play(Create(axes_3d), Write(x_label_3d), Write(y_label_3d), Write(z_label_3d))
        self.play(Create(vector_3d_arrow))
        self.play(Write(vector_3d_label))
        self.wait(2)
        
        # Create projection plane (xy-plane)
        projection_plane = Surface(
            lambda u, v: axes_3d.coords_to_point(u, v, 0),
            u_range=[-0.5, 1.5],
            v_range=[-0.5, 1.5],
            fill_opacity=0.3,
            fill_color=GREEN
        )
        
        plane_label = Text("Projection Plane (z=0)", font_size=24, color=GREEN)
        plane_label.rotate(PI/2, axis=RIGHT)
        plane_label.move_to(axes_3d.coords_to_point(0.75, 0.75, 0))
        
        # Show projection plane
        self.play(Create(projection_plane))
        self.play(Write(plane_label))
        self.wait(1)
        
        # Show projection process with dotted lines
        projection_lines = VGroup()
        
        # Line from vector tip to projection
        proj_line = DashedLine(
            axes_3d.coords_to_point(*vector_3d),
            axes_3d.coords_to_point(vector_3d[0], vector_3d[1], 0),
            color=YELLOW,
            dash_length=0.1
        )
        projection_lines.add(proj_line)
        
        # Create the projected vector
        vector_2d_arrow = Arrow3D(
            start=axes_3d.coords_to_point(0, 0, 0),
            end=axes_3d.coords_to_point(vector_3d[0], vector_3d[1], 0),
            color=RED,
            stroke_width=8
        )
        
        # Show projection process
        self.play(Create(proj_line))
        self.play(Create(vector_2d_arrow))
        self.wait(1)
        
        # Add transformation matrix
        transformation_text = MathTex(
            r"P = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix}",
            font_size=36
        )
        # Fixed-in-frame handled via add_fixed_in_frame_mobjects
        transformation_text.to_edge(LEFT).shift(UP)
        
        # Show matrix multiplication
        multiplication = MathTex(
            r"P \vec{v}_{3D} = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \end{bmatrix} \begin{bmatrix} 0.3 \\ 0.7 \\ 0.6 \end{bmatrix} = \begin{bmatrix} 0.3 \\ 0.7 \end{bmatrix}",
            font_size=28
        )
        # Fixed-in-frame handled via add_fixed_in_frame_mobjects
        multiplication.next_to(transformation_text, DOWN, aligned_edge=LEFT)
        
        self.add_fixed_in_frame_mobjects(transformation_text, multiplication)
        self.play(Write(transformation_text))
        self.wait(1)
        self.play(Write(multiplication))
        self.wait(2)
        
        # Transition to 2D view
        self.play(
            FadeOut(vector_3d_arrow),
            FadeOut(vector_3d_label),
            FadeOut(projection_plane),
            FadeOut(plane_label),
            FadeOut(proj_line),
            FadeOut(z_label_3d)
        )
        
        # Move camera to 2D view
        self.move_camera(phi=0, theta=-PI/2)
        
        # Create 2D axes
        axes_2d = Axes(
            x_range=[-0.5, 1.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            x_length=6,
            y_length=6
        )
        
        x_label_2d = axes_2d.get_x_axis_label(Tex("x"))
        y_label_2d = axes_2d.get_y_axis_label(Tex("y"))
        
        # Transform the existing vector to 2D representation
        vector_2d_final = Arrow(
            start=axes_2d.coords_to_point(0, 0),
            end=axes_2d.coords_to_point(0.6, 1.0),  # Final transformed vector
            color=RED,
            stroke_width=8
        )
        
        # But wait - let's show the actual mathematical transformation
        # The problem states the result is [0.6, 1], not [0.3, 0.7]
        # This suggests there's a scaling/transformation beyond simple projection
        
        # Update the math to show the complete transformation
        complete_transform = MathTex(
            r"T \vec{v}_{3D} = \begin{bmatrix} 2 & 0 & 0 \\ 0 & \frac{10}{7} & 0 \end{bmatrix} \begin{bmatrix} 0.3 \\ 0.7 \\ 0.6 \end{bmatrix} = \begin{bmatrix} 0.6 \\ 1.0 \end{bmatrix}",
            font_size=24
        )
        # Fixed-in-frame handled via add_fixed_in_frame_mobjects
        complete_transform.to_edge(LEFT).shift(DOWN * 2)
        self.add_fixed_in_frame_mobjects(complete_transform)
        
        # Replace the 3D scene with 2D
        self.play(
            Transform(axes_3d, axes_2d),
            Transform(x_label_3d, x_label_2d),
            Transform(y_label_3d, y_label_2d),
            Transform(vector_2d_arrow, vector_2d_final),
            Transform(multiplication, complete_transform)
        )
        
        # Add final vector label
        vector_2d_label = MathTex(r"\vec{v}_{2D} = \begin{bmatrix} 0.6 \\ 1.0 \end{bmatrix}")
        vector_2d_label.next_to(vector_2d_final.get_end(), UR)
        self.add_fixed_in_frame_mobjects(vector_2d_label)
        
        self.play(Write(vector_2d_label))
        
        # Summary text
        summary = Text("3D → 2D Transformation Complete!", font_size=28, color=GREEN)
        # Fixed-in-frame handled via add_fixed_in_frame_mobjects
        summary.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(summary)
        
        self.play(Write(summary))
        self.wait(3)