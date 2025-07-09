from manim import *
import numpy as np

class PCAAnimation(ThreeDScene):
    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        
        # Generate sample 3D data points that have a clear principal direction
        np.random.seed(42)  # For reproducible results
        
        # Create data with correlation (elongated cloud)
        n_points = 15
        t = np.linspace(0, 4, n_points)
        
        # Base points along a line with some noise
        data_points = np.array([
            t + np.random.normal(0, 0.3, n_points),
            0.5 * t + np.random.normal(0, 0.2, n_points), 
            0.2 * t + np.random.normal(0, 0.15, n_points)
        ]).T
        
        # Center the data
        data_points = data_points - np.mean(data_points, axis=0)
        
        # Scale for better visualization
        data_points *= 1.5
        
        # Create 3D coordinate system
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1], 
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # Create data points as 3D dots
        dots_3d = VGroup()
        for point in data_points:
            dot = Dot3D(point=point, color=BLUE, radius=0.08)
            dots_3d.add(dot)
        
        # Add title
        title = Text("Principal Component Analysis (PCA)", font_size=36)
        title.to_edge(UP)
        
        # Compute PCA
        # Center the data (already done above)
        cov_matrix = np.cov(data_points.T)
        eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)
        
        # Sort by eigenvalues (descending)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # First principal component (direction of maximum variance)
        pc1 = eigenvectors[:, 0]
        
        # Create the principal component line
        line_length = 4
        pc_line_start = -line_length * pc1
        pc_line_end = line_length * pc1
        
        pc_line = Line3D(
            start=pc_line_start,
            end=pc_line_end,
            color=RED,
            stroke_width=6
        )
        
        # Scene 1: Show 3D data
        self.add_fixed_in_frame_mobjects(title)
        self.play(Create(axes))
        self.wait(0.5)
        
        subtitle1 = Text("Original 3D Data Points", font_size=24, color=BLUE)
        subtitle1.next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(subtitle1)
        
        self.play(LaggedStart(*[Create(dot) for dot in dots_3d], lag_ratio=0.1))
        self.wait(2)
        
        # Scene 2: Show principal component
        subtitle2 = Text("First Principal Component (Maximum Variance Direction)", 
                         font_size=24, color=RED)
        subtitle2.next_to(title, DOWN)
        
        self.play(Transform(subtitle1, subtitle2))
        self.play(Create(pc_line))
        self.wait(2)
        
        # Scene 3: Show projections
        subtitle3 = Text("Projecting Points onto Principal Component", 
                         font_size=24, color=GREEN)
        subtitle3.next_to(title, DOWN)
        
        self.play(Transform(subtitle1, subtitle3))
        
        # Create projected points and connection lines
        projected_points = []
        projection_lines = VGroup()
        projected_dots = VGroup()
        
        for point in data_points:
            # Project point onto PC1
            projection_scalar = np.dot(point, pc1)
            projected_point = projection_scalar * pc1
            projected_points.append(projected_point)
            
            # Create projection line (perpendicular connection)
            proj_line = Line3D(
                start=point,
                end=projected_point,
                color=YELLOW,
                stroke_width=2
            )
            projection_lines.add(proj_line)
            
            # Create projected point
            proj_dot = Dot3D(point=projected_point, color=GREEN, radius=0.06)
            projected_dots.add(proj_dot)
        
        # Animate projections one by one
        for i, (line, proj_dot) in enumerate(zip(projection_lines, projected_dots)):
            self.play(
                Create(line),
                Create(proj_dot),
                run_time=0.3
            )
        
        self.wait(2)
        
        # Scene 4: Show dimension reduction
        subtitle4 = Text("3D → 1D: Dimension Reduction Complete!", 
                         font_size=24, color=PURPLE)
        subtitle4.next_to(title, DOWN)
        
        self.play(Transform(subtitle1, subtitle4))
        
        # Fade out original 3D points and projection lines
        self.play(
            FadeOut(dots_3d),
            FadeOut(projection_lines),
            run_time=1.5
        )
        
        # Highlight the 1D representation
        self.play(
            projected_dots.animate.set_color(PURPLE),
            pc_line.animate.set_color(PURPLE),
            run_time=1
        )
        
        self.wait(2)
        
        # Scene 5: Add explanation
        explanation = VGroup(
            Text("• Original data: 3 dimensions", font_size=20),
            Text("• Projected data: 1 dimension", font_size=20),
            Text("• Maximum variance preserved", font_size=20),
            Text("• Information loss minimized", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        explanation.to_corner(UL, buff=0.5)
        explanation.shift(DOWN * 2)
        
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        
        # Rotate camera for final view
        self.play(
            self.camera.phi_tracker.animate.set_value(85 * DEGREES),
            self.camera.theta_tracker.animate.set_value(0 * DEGREES),
            run_time=3
        )
        
        self.wait(3)

# To run this animation, save the file and use:
# manim -pql filename.py PCAAnimation
# 
# Options:
# -pql: Preview with low quality (fast rendering)
# -pqh: Preview with high quality
# -s: Save last frame as image