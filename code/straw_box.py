from manim import *

class StrawBoxWithCage(ThreeDScene):
    def construct(self):
        # Set camera for a perspective-like view
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        # self.camera.frame.scale(0.75)

        # Parameters
        rows, cols = 5, 4
        straw_radius = 0.05
        straw_height = 4
        spacing_y = 1
        spacing_z = 1

        straws = VGroup()

        # Create array of vertical straws (cylinders)
        for i in range(rows):
            for j in range(cols):
                y = i * spacing_y - (rows - 1) * spacing_y / 2
                z = j * spacing_z - (cols - 1) * spacing_z / 2
                x = 0  # Keep all straws centered in x

                straw = Cylinder(
                    radius=straw_radius,
                    height=straw_height,
                    direction=RIGHT,  # Lying flat toward foreground
                    fill_opacity=0.4,
                    fill_color=BLUE,
                    stroke_opacity=0.1,
                ).move_to([x, y, z])
                straws.add(straw)

        # Dimensions for the box
        box_width = straw_height + 0.5
        box_height = (rows - 1) * spacing_y + 1
        box_depth = (cols - 1) * spacing_z + 1


        # Create a translucent box around the straws
        box = Cube(
            side_length=1,  # Will scale manually
            fill_opacity=0.4,
            fill_color=GRAY,
            stroke_opacity=0.2,
        ).scale([box_width, box_height, box_depth / 1.0])  # Scale box to fit array
        box.move_to(ORIGIN)

        # Group and show
        self.add(box, straws)

        # Camera work (this adds ~ 2 mins to render, remove if unnecessary)
        self.begin_ambient_camera_rotation(rate=0.1)  # slow rotation
        self.wait(5)  # rotate for 5 seconds
        self.stop_ambient_camera_rotation()
