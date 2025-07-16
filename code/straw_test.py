from manim import *
import numpy as np

class StrawBox3D(ThreeDScene):
    def construct(self):
        # Set up the camera
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES, distance=20)
        
        # Box dimensions
        box_width = 6
        box_height = 5
        box_depth = 4
        
        # Create wireframe box
        box_corners = [
            [-box_width/2, -box_height/2, -box_depth/2],
            [box_width/2, -box_height/2, -box_depth/2],
            [box_width/2, box_height/2, -box_depth/2],
            [-box_width/2, box_height/2, -box_depth/2],
            [-box_width/2, -box_height/2, box_depth/2],
            [box_width/2, -box_height/2, box_depth/2],
            [box_width/2, box_height/2, box_depth/2],
            [-box_width/2, box_height/2, box_depth/2],
        ]
        
        # Define edges of the box
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Front face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Back face
            (0, 4), (1, 5), (2, 6), (3, 7),  # Connecting edges
        ]
        
        # Create wireframe
        box_edges = VGroup()
        for start, end in edges:
            edge = Line3D(
                start=box_corners[start],
                end=box_corners[end],
                color=GREEN,
                stroke_width=3
            )
            box_edges.add(edge)
        
        # Add the box to the scene
        self.add(box_edges)
        
        # Straw colors
        straw_colors = [
            RED, BLUE, YELLOW, PINK, PURPLE, 
            ORANGE, TEAL, LIGHT_PINK, LIGHT_BROWN, MAROON
        ]
        
        # Straw parameters
        straw_radius = 0.1
        straw_length = box_depth - 0.3
        
        # Calculate number of straws per row and layer
        straws_per_row = int((box_width - 0.5) / (straw_radius * 3))
        straws_per_layer = int((box_height - 0.5) / (straw_radius * 3))
        
        # Create straws
        straws = VGroup()
        
        for layer in range(straws_per_layer):
            for row in range(straws_per_row):
                # Alternate offset for each layer (brick pattern)
                offset = (layer % 2) * straw_radius * 1.5
                
                x = -box_width/2 + straw_radius * 2 + row * straw_radius * 3 + offset
                y = -box_height/2 + straw_radius * 2 + layer * straw_radius * 3
                z = 0
                
                # Skip if straw would be outside box
                if x > box_width/2 - straw_radius or x < -box_width/2 + straw_radius:
                    continue
                
                # Create straw (cylinder lying horizontally)
                straw = Cylinder(
                    radius=straw_radius,
                    height=straw_length,
                    direction=Z_AXIS,  # Along Z-axis (horizontal)
                    color=np.random.choice(straw_colors),
                    fill_opacity=1,
                    stroke_width=0
                )
                
                # Position the straw
                straw.move_to([x, y, z])
                
                # Add white stripes to some straws
                if np.random.random() > 0.5:
                    for i in range(3):
                        stripe_z = (i - 1) * straw_length * 0.3
                        stripe = Cylinder(
                            radius=straw_radius * 1.05,
                            height=straw_length * 0.15,
                            direction=Z_AXIS,
                            color=WHITE,
                            fill_opacity=1,
                            stroke_width=0
                        )
                        stripe.move_to([x, y, stripe_z])
                        straws.add(stripe)
                
                straws.add(straw)
        
        # Add all straws to the scene
        self.add(straws)
        
        # Add some ambient rotation to start
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(2)


# To render this animation, save this file and run:
# manim -pql straw_test.py --fps 3
# Options:
# -p: Preview after rendering
# -ql: Low quality (faster rendering)
# -qm: Medium quality
# -qh: High quality
# -qk: 4K quality