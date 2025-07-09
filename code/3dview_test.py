from manim import *

class TetrahedronVolume(ThreeDScene):
    def construct(self):
        # Set up the 3D axes and grid
        axes = ThreeDAxes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            z_range=[-1, 5, 1],
            x_length=8,
            y_length=8,
            z_length=6,
        )
        
        # Create a number plane (grid) in the xy-plane
        grid = NumberPlane(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=8,
            background_line_style={
                "stroke_color": BLUE,
                "stroke_width": 1,
                "stroke_opacity": 0.6,
            },
            axis_config={
                "stroke_color": LIGHT_GREY,
            }
        )
        
        # Define the vertices of the tetrahedron
        # Using generic variable names as shown in the image
        v1 = np.array([1, 1, 1])  # (x₁, y₁, z₁)
        v2 = np.array([2, 2, 2])  # (x₂, y₂, z₂)
        v3 = np.array([3, 3, 3])  # (x₃, y₃, z₃)
        v4 = np.array([4, 4, 4])  # (x₄, y₄, z₄)
        
        # Create the tetrahedron faces
        face1 = Polygon(
            axes.c2p(*v1), axes.c2p(*v2), axes.c2p(*v3),
            fill_opacity=0.5, fill_color=TEAL, stroke_color=WHITE
        )
        face2 = Polygon(
            axes.c2p(*v1), axes.c2p(*v2), axes.c2p(*v4),
            fill_opacity=0.5, fill_color=TEAL, stroke_color=WHITE
        )
        face3 = Polygon(
            axes.c2p(*v1), axes.c2p(*v3), axes.c2p(*v4),
            fill_opacity=0.5, fill_color=TEAL, stroke_color=WHITE
        )
        face4 = Polygon(
            axes.c2p(*v2), axes.c2p(*v3), axes.c2p(*v4),
            fill_opacity=0.5, fill_color=TEAL, stroke_color=WHITE
        )
        
        tetrahedron = VGroup(face1, face2, face3, face4)
        
        # Create vertex dots and labels
        vertices = VGroup()
        labels = VGroup()
        
        vertex_data = [
            (v1, "(x_1, y_1, z_1)"),
            (v2, "(x_2, y_2, z_2)"),
            (v3, "(x_3, y_3, z_3)"),
            (v4, "(x_4, y_4, z_4)")
        ]
        
        for vertex, label_text in vertex_data:
            dot = Dot3D(axes.c2p(*vertex), color=WHITE, radius=0.08)
            label = MathTex(label_text, font_size=24)
            label.next_to(axes.c2p(*vertex), UP+RIGHT, buff=0.1)
            vertices.add(dot)
            labels.add(label)
        
        # Add the question text
        question = Text("What is the volume\nof this solid?", font_size=36)
        question.to_corner(UL)
        
        # Set camera angle for perspective view
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        
        # Add all elements to the scene
        self.add(grid)
        self.add(axes)
        self.add(tetrahedron)
        self.add(vertices)
        self.add_fixed_orientation_mobjects(*labels)
        self.add_fixed_in_frame_mobjects(question)
        
        # Optional: animate the construction
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)


# Alternative version with specific numeric coordinates
class TetrahedronVolumeNumeric(ThreeDScene):
    def construct(self):
        # Set up the 3D axes
        axes = ThreeDAxes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            z_range=[-1, 4, 1],
            x_length=10,
            y_length=10,
            z_length=6,
        )
        
        # Create a number plane with perspective grid effect
        grid = NumberPlane(
            x_range=[-1, 5, 0.5],
            y_range=[-1, 5, 0.5],
            x_length=10,
            y_length=10,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
            },
            faded_line_ratio=2,
        ).shift(axes.c2p(0, 0, 0))
        
        # Define specific vertices (you can adjust these)
        v1 = np.array([1, 1, 1])
        v2 = np.array([2, 2, 2]) 
        v3 = np.array([3, 3, 3])
        v4 = np.array([4, 4, 4])
        
        # Create tetrahedron using lines for edges
        edges = VGroup()
        edge_pairs = [
            (v1, v2), (v1, v3), (v1, v4),
            (v2, v3), (v2, v4), (v3, v4)
        ]
        
        for start, end in edge_pairs:
            edge = Line3D(
                axes.c2p(*start), 
                axes.c2p(*end), 
                color=WHITE,
                stroke_width=2
            )
            edges.add(edge)
        
        # Create semi-transparent faces
        faces = VGroup()
        face_vertices = [
            (v1, v2, v3),
            (v1, v2, v4),
            (v1, v3, v4),
            (v2, v3, v4)
        ]
        
        for vertices in face_vertices:
            face = Polygon(
                *[axes.c2p(*v) for v in vertices],
                fill_opacity=0.3,
                fill_color=TEAL,
                stroke_width=0
            )
            faces.add(face)
        
        # Add vertex labels with coordinates
        labels = VGroup()
        label_texts = [
            "(x_1, y_1, z_1)",
            "(x_2, y_2, z_2)", 
            "(x_3, y_3, z_3)",
            "(x_4, y_4, z_4)"
        ]
        
        for vertex, label_text in zip([v1, v2, v3, v4], label_texts):
            label = MathTex(label_text, font_size=28, color=WHITE)
            label.move_to(axes.c2p(*vertex))
            label.shift(0.5 * (UP + RIGHT))
            labels.add(label)
        
        # Question text
        question = Text("What is the volume\nof this solid?", font_size=40, color=WHITE)
        question.to_corner(UL).shift(0.5 * DOWN)
        
        self.set_camera_orientation(
            phi=25 * DEGREES,    # Much lower elevation angle (almost grazing the plane)
            theta=-135 * DEGREES, # or 225° - viewing from back-right
            distance=15          # Closer to enhance perspective
        )
        
        # Build the scene
        self.add(grid)
        self.play(Create(axes), run_time=1)
        self.play(Create(edges), run_time=1.5)
        self.play(FadeIn(faces), run_time=1)
        self.add_fixed_orientation_mobjects(*labels)
        self.play(Write(question))
        
        # Slowly rotate for better visualization
        self.begin_ambient_camera_rotation(rate=0.05)
        self.wait(6)