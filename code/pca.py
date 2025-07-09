from manim import *
import numpy as np

class PCAAnimation(ThreeDScene):
    def construct(self):
        # Set up 3D scene
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # Generate sample 3D data points with correlation
        np.random.seed(42)
        n_points = 12
        
        # Create correlated data along a diagonal direction
        t = np.linspace(-2, 2, n_points)
        noise_scale = 0.3
        
        # Original 3D points with correlation
        x = t + np.random.normal(0, noise_scale, n_points)
        y = 0.8 * t + np.random.normal(0, noise_scale, n_points)
        z = 0.5 * t + np.random.normal(0, noise_scale, n_points)
        
        # Store original data
        original_points = np.column_stack([x, y, z])
        
        # Calculate PCA (simplified)
        # Center the data
        mean_point = np.mean(original_points, axis=0)
        centered_data = original_points - mean_point
        
        # Calculate covariance matrix and eigenvectors
        cov_matrix = np.cov(centered_data.T)
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Get the principal component (eigenvector with largest eigenvalue)
        pc_direction = eigenvectors[:, np.argmax(eigenvalues)]
        pc_direction = pc_direction / np.linalg.norm(pc_direction)
        
        # Create 3D coordinate system
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={"color": GRAY, "stroke_width": 2}
        )
        
        # Create data points as 3D dots
        dots_3d = VGroup()
        colors = [interpolate_color(BLUE, RED, i/n_points) for i in range(n_points)]
        
        for i, point in enumerate(original_points):
            dot = Dot3D(
                point=point,
                radius=0.08,
                color=colors[i]
            )
            dots_3d.add(dot)
        
        # Show initial setup
        self.add(axes)
        self.play(
            *[Create(dot) for dot in dots_3d],
            run_time=2
        )
        self.wait(1)
        
        # Create and show principal component line
        pc_start = mean_point - 3 * pc_direction
        pc_end = mean_point + 3 * pc_direction
        
        pc_line = Line3D(
            start=pc_start,
            end=pc_end,
            color=YELLOW,
            stroke_width=6
        )
        
        self.play(Create(pc_line), run_time=1.5)
        self.wait(0.5)
        
        # Calculate projections onto principal component
        projections = []
        projection_lines = VGroup()
        projected_dots = VGroup()
        
        for i, point in enumerate(original_points):
            # Project point onto principal component line
            point_centered = point - mean_point
            projection_scalar = np.dot(point_centered, pc_direction)
            projection = mean_point + projection_scalar * pc_direction
            projections.append(projection)
            
            # Create dotted line from original point to projection
            proj_line = DashedVMobject(
                Line3D(
                    start=point,
                    end=projection,
                    color=GRAY,
                    stroke_width=2
                ),
                num_dashes=15,
                positive_space_ratio=0.4
            )
            projection_lines.add(proj_line)
            
            # Create projected point
            proj_dot = Dot3D(
                point=projection,
                radius=0.06,
                color=colors[i]
            )
            projected_dots.add(proj_dot)
        
        # Animate projections
        self.play(
            *[Create(line) for line in projection_lines],
            run_time=2
        )
        
        self.play(
            *[Create(dot) for dot in projected_dots],
            run_time=1.5
        )
        self.wait(1)
        
        # Move camera closer to the principal component
        self.play(
            self.camera.frame.animate.set(
                phi=80 * DEGREES,
                theta=0 * DEGREES,
                zoom=1.5
            ),
            run_time=2
        )
        self.wait(0.5)
        
        # Fade out original 3D points and projection lines to focus on 1D result
        self.play(
            *[FadeOut(dot) for dot in dots_3d],
            *[FadeOut(line) for line in projection_lines],
            FadeOut(axes),
            run_time=1.5
        )
        
        # Rotate to show the 1D line more clearly
        self.play(
            self.camera.frame.animate.set(
                phi=90 * DEGREES,
                theta=0 * DEGREES,
                zoom=2
            ),
            run_time=2
        )
        
        # Add simple label
        label = Text("1D Projection", font_size=36, color=WHITE)
        label.rotate(PI/2, axis=RIGHT)
        label.rotate(PI/2, axis=OUT)
        label.next_to(pc_line, UP, buff=0.5)
        
        self.add_fixed_in_frame_mobjects(label)
        self.play(Write(label), run_time=1)
        
        self.wait(2)
        
        # Final rotation to show the result from different angles
        self.play(
            self.camera.frame.animate.set(
                phi=75 * DEGREES,
                theta=45 * DEGREES,
                zoom=1.8
            ),
            run_time=2
        )
        
        self.wait(2)

# Additional scene showing the concept more abstractly
class PCAConceptual(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # Create a cloud of points in 3D
        np.random.seed(123)
        n_points = 20
        
        # Create elongated cloud of points
        t = np.random.normal(0, 1, n_points)
        x = 2 * t + np.random.normal(0, 0.3, n_points)
        y = 1.5 * t + np.random.normal(0, 0.3, n_points)
        z = t + np.random.normal(0, 0.2, n_points)
        
        points_3d = np.column_stack([x, y, z])
        
        # Create axes
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 2, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        
        # Create point cloud
        point_cloud = VGroup()
        for point in points_3d:
            dot = Dot3D(point=point, radius=0.06, color=BLUE)
            point_cloud.add(dot)
        
        self.add(axes)
        self.play(*[FadeIn(dot) for dot in point_cloud], run_time=2)
        
        # Show PCA direction
        mean_pos = np.mean(points_3d, axis=0)
        centered = points_3d - mean_pos
        cov = np.cov(centered.T)
        eigenvals, eigenvecs = np.linalg.eig(cov)
        pc1 = eigenvecs[:, np.argmax(eigenvals)]
        
        pc_line = Line3D(
            start=mean_pos - 3*pc1,
            end=mean_pos + 3*pc1,
            color=RED,
            stroke_width=8
        )
        
        self.play(Create(pc_line), run_time=1.5)
        
        # Project all points
        projections = []
        proj_lines = VGroup()
        proj_dots = VGroup()
        
        for i, point in enumerate(points_3d):
            centered_point = point - mean_pos
            proj_scalar = np.dot(centered_point, pc1)
            projection = mean_pos + proj_scalar * pc1
            projections.append(projection)
            
            proj_line = DashedVMobject(Line3D(point, projection, color=GRAY_A), num_dashes=15, positive_space_ratio=0.4)
            proj_lines.add(proj_line)
            
            proj_dot = Dot3D(projection, radius=0.05, color=YELLOW)
            proj_dots.add(proj_dot)
        
        self.play(*[Create(line) for line in proj_lines], run_time=2)
        self.play(*[Create(dot) for dot in proj_dots], run_time=1)
        
        self.wait(1)
        
        # Focus on the 1D result
        self.play(
            *[FadeOut(dot) for dot in point_cloud],
            *[FadeOut(line) for line in proj_lines],
            FadeOut(axes),
            self.camera.frame.animate.set(zoom=2),
            run_time=2
        )
        
        self.wait(3)


# Usage instructions:
# To render this animation, save it as a .py file and run:
# manim -pql filename.py PCAAnimation
# or for higher quality:
# manim -pqh filename.py PCAAnimation