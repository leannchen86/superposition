from manim import *
import numpy as np

# Alternative scene with 3D perspective using improved projector body
class ProjectorWithLightBeams3D(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        
        # Nice starting camera angle (from projector.py)
        self.set_camera_orientation(phi=60 * DEGREES,
                                    theta=-60 * DEGREES,
                                    distance=10)
        
        # ─── Projector body (from projector.py) ────────────────────────────
        body = Prism(
            dimensions=[2, 1, 1],          # width, height, depth
            fill_color=GRAY_D,
            fill_opacity=0.9,
            stroke_width=0,
        ).shift(LEFT)                      # scoot it left so the beam has room

        # ─── Lens ring (from projector.py) ────────────────────────────────
        lens_ring = Annulus(
            inner_radius=0.30,
            outer_radius=0.40,
            fill_color=BLUE_E,
            fill_opacity=1,
            stroke_width=0,
        )
        lens_ring.rotate(PI / 2, axis=UP)         # face the ring forward
        lens_ring.next_to(body, RIGHT, buff=0)    # attach to body's front
        
        # Screen
        screen = Rectangle(width=2.5, height=2, fill_color=WHITE, fill_opacity=0.9)
        screen.shift(RIGHT * 3)
        
        # Create light beams using polygons (improved beaming from 2D version)
        def create_light_beam_3d(start_point, end_point, width_start=0.1, width_end=1.2):
            # Calculate beam vertices
            direction = end_point - start_point
            perpendicular = np.array([-direction[1], direction[0], 0])
            perpendicular = perpendicular / np.linalg.norm(perpendicular)
            
            # Create beam shape
            vertices = [
                start_point + perpendicular * width_start / 2,
                start_point - perpendicular * width_start / 2,
                end_point - perpendicular * width_end / 2,
                end_point + perpendicular * width_end / 2
            ]
            
            return Polygon(*vertices, fill_opacity=0.3, fill_color=YELLOW, stroke_width=0)
        
        # Main light beam from lens center
        lens_center = lens_ring.get_center()
        main_beam = create_light_beam_3d(
            lens_center,
            np.array([2.8, 0, 0])    # To screen area
        )
        
        # Additional light rays for more realistic effect
        light_rays = VGroup()
        for i in range(7):
            offset_y = (i - 3) * 0.15
            offset_z = np.sin(i * 0.8) * 0.1  # Add some z variation for 3D effect
            ray_start = lens_center + np.array([0, offset_y * 0.3, offset_z * 0.3])
            ray_end = np.array([2.8, offset_y, offset_z])
            
            ray = create_light_beam_3d(ray_start, ray_end, 0.05, 0.8)
            ray.set_fill(YELLOW, opacity=0.2)
            light_rays.add(ray)
        
        # Create projected content on screen
        projected_image = Rectangle(
            width=2,
            height=1.5,
            fill_color=BLUE,
            fill_opacity=0.6,
            stroke_width=0
        ).shift(RIGHT * 3)
        
        # Add some text being projected
        projected_text = Text("MANIM", font_size=24, color=WHITE).move_to(projected_image.get_center())
        
        # Create light particles for added effect
        particles = VGroup()
        for _ in range(15):
            particle = Dot(
                radius=0.02,
                color=YELLOW,
                fill_opacity=0.8
            )
            # Random position within the light beam area with 3D spread
            x_pos = np.random.uniform(lens_center[0], 2.5)
            beam_width = 0.5 * (1 + (x_pos - lens_center[0]) / 3.5)
            y_pos = np.random.uniform(-beam_width, beam_width)
            z_pos = np.random.uniform(-beam_width * 0.3, beam_width * 0.3)
            particle.move_to([x_pos, y_pos, z_pos])
            particles.add(particle)
        
        # ─── Assemble and animate ─────────────────────────────────────────
        projector = VGroup(body, lens_ring)
        
        # Animation sequence
        self.play(
            FadeIn(projector, shift=LEFT * 0.2),
            FadeIn(screen),
            run_time=1.5
        )
        
        self.play(
            FadeIn(main_beam),
            FadeIn(light_rays),
            run_time=1.5
        )
        
        self.play(
            FadeIn(projected_image),
            Write(projected_text),
            run_time=2
        )
        
        self.play(
            FadeIn(particles),
            run_time=1
        )
        
        # Animate the light particles floating
        particle_animations = []
        for particle in particles:
            # Each particle moves slightly in 3D
            new_pos = particle.get_center() + np.random.uniform(-0.15, 0.15, 3)
            particle_animations.append(particle.animate.move_to(new_pos))
        
        # Animate beam intensity variation
        beam_pulse = main_beam.animate.set_fill(opacity=0.5)
        rays_pulse = light_rays.animate.set_fill(opacity=0.4)
        
        self.play(
            AnimationGroup(*particle_animations),
            beam_pulse,
            rays_pulse,
            run_time=2
        )
        
        # Fade back to normal
        self.play(
            main_beam.animate.set_fill(opacity=0.3),
            light_rays.animate.set_fill(opacity=0.2),
            run_time=1
        )
        
        self.wait(2)

# To render these scenes, save this file as projector_animation.py and run:
# manim projector_animation.py ProjectorWithLightBeams -pql  # for low quality preview
# manim projector_animation.py ProjectorWithLightBeams -pqh  # for high quality
# manim projector_animation.py ProjectorWithLightBeams3D -pql  # for 3D version