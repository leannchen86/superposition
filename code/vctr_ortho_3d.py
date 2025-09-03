from manim import *
import numpy as np

class VectorOrthogonality3D(ThreeDScene):
    def construct(self):
        # Setup 3D axes
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"color": GREY},
            tips=False,
        )
        
        # Add axis labels that face the camera
        x_label = Tex(r"x", font_size=30).move_to(axes.x_axis.get_end() + RIGHT * 0.5)
        y_label = Tex(r"y", font_size=30).move_to(axes.y_axis.get_end() + UP * 0.5)
        z_label = Tex(r"z", font_size=30).move_to(axes.z_axis.get_end() + OUT * 0.5)
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)
        
        # Set initial camera position similar to what_is_a_feature.py
        start_distance = 8.0
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, distance=start_distance)
        
        # Create the three orthogonal vectors
        vec_x = Arrow3D(
            start=ORIGIN,
            end=2*RIGHT,
            color=RED,
            thickness=0.02,
            height=0.3,
            base_radius=0.1,
        )
        
        vec_y = Arrow3D(
            start=ORIGIN,
            end=2*UP,
            color=BLUE,
            thickness=0.02,
            height=0.3,
            base_radius=0.1,
        )
        
        vec_z = Arrow3D(
            start=ORIGIN,
            end=2*OUT,
            color=GREEN,
            thickness=0.02,
            height=0.3,
            base_radius=0.1,
        )
        
        # Add axes and vectors
        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label))
        self.wait(0.5)
        self.play(FadeIn(vec_x, vec_y, vec_z), run_time=0.5)
        
        # Show 90° angle between X and Y
        xy_angle = Angle(
            Line(ORIGIN, 2*RIGHT),
            Line(ORIGIN, 2*UP),
            radius=0.5,
            color=YELLOW,
            stroke_width=4
        )
        # Move camera to better view XY angle
        self.move_camera(
            phi=60 * DEGREES,
            theta=30 * DEGREES,
            frame_center=xy_angle.get_center(),
            distance=4,
            run_time=2
        )
        
        xy_angle_label = Tex(r"90°", color=WHITE, font_size=35)
        xy_angle_label.move_to(0.8*RIGHT + 0.8*UP)
        self.add_fixed_orientation_mobjects(xy_angle_label)
        
        self.play(FadeIn(xy_angle))
        self.play(FadeIn(xy_angle_label), run_time=1)
        self.wait(2)
        
        # Show 90° angle between X and Z using Arc
        xz_angle = Arc(
            radius=0.5,
            start_angle=0,
            angle=PI/2,
            color=YELLOW,
            stroke_width=4
        ).rotate(PI/2, axis=UP, about_point=ORIGIN)
        xz_angle_label = Tex(r"90°", color=WHITE, font_size=35)
        xz_angle_label.move_to(0.8*RIGHT + 0.8*OUT)
        self.add_fixed_orientation_mobjects(xz_angle_label)
        
        self.play(FadeIn(xz_angle))
        self.play(FadeIn(xz_angle_label), run_time=1)
        self.wait(2)
        
        # Show 90° angle between Y and Z using Arc
        yz_angle = Arc(
            radius=0.5,
            start_angle=0,
            angle=PI/2,
            color=YELLOW,
            stroke_width=4
        ).rotate(-PI/2, axis=RIGHT, about_point=ORIGIN)
        yz_angle_label = Tex(r"90°", color=WHITE, font_size=35)
        yz_angle_label.move_to(0.8*UP + 0.8*OUT)
        self.add_fixed_orientation_mobjects(yz_angle_label)
        
        self.play(FadeIn(yz_angle))
        self.play(FadeIn(yz_angle_label), run_time=1)
        self.wait(2)
        
        # Show all three angles simultaneously in isometric view
        angle_xy = Angle(
            Line(ORIGIN, 2*RIGHT),
            Line(ORIGIN, 2*UP),
            radius=0.5,
            color=YELLOW,
            stroke_width=3,
        )
        angle_xz = Arc(
            radius=0.5,
            start_angle=0,
            angle=PI/2,
            color=YELLOW,
            stroke_width=3,
        ).rotate(PI/2, axis=UP, about_point=ORIGIN)
        angle_yz = Arc(
            radius=0.5,
            start_angle=0,
            angle=PI/2,
            color=YELLOW,
            stroke_width=3,
        ).rotate(-PI/2, axis=RIGHT, about_point=ORIGIN)
        all_angles = VGroup(angle_xy, angle_xz, angle_yz)
        
        self.play(FadeIn(all_angles))
        self.wait(2)
        
        # Fade out everything
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
        )