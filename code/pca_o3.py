from manim import *
import numpy as np

class PCAIntro(ThreeDScene):
    """A concise, intuitive animation that visually explains Principal Component Analysis (PCA).

    Updated to 3-D → 1-D:
    1. Plot a 3-D Gaussian data cloud.
    2. Draw the first principal component (dominant eigenvector of the covariance matrix).
    3. Project every point onto PC-1, collapsing the 3-D cloud into a 1-D line.
    """

    # Tunables for easy experimentation
    N_POINTS = 70
    MEAN = np.array([0, 0, 0])
    # Non-axis-aligned 3×3 covariance so PCA is visually obvious
    COV = np.array([
        [3.0, 1.2, 0.8],
        [1.2, 2.0, 0.6],
        [0.8, 0.6, 1.0],
    ])
    DOT_RADIUS = 0.06

    def construct(self):
        # 1) Generate and show the synthetic 3-D data cloud
        rng = np.random.default_rng(42)
        data = rng.multivariate_normal(self.MEAN, self.COV, self.N_POINTS)

        # Set an initial 3-D camera orientation for better depth perception
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            z_range=[-6, 6, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"color": GRAY, "stroke_width": 2},
        )
        dots = VGroup(*[
            Dot3D(point=[x, y, z], radius=self.DOT_RADIUS, color=BLUE)
            for x, y, z in data
        ])

        self.play(Create(axes))
        self.play(LaggedStart(*[FadeIn(dot) for dot in dots], lag_ratio=0.02))
        self.wait(0.5)

        # 2) Compute principal components (eigenvectors of covariance)
        cov_mat = np.cov(data.T)
        eigvals, eigvecs = np.linalg.eigh(cov_mat)  # eigh guarantees sorted eigenvalues for symmetric matrices
        
        # Check if we have valid eigenvalues and eigenvectors
        if eigvals.size == 0 or eigvecs.size == 0:
            raise ValueError("Eigenvalue decomposition failed - got empty arrays")
        
        if eigvecs.shape[1] < 2:
            raise ValueError(f"Expected at least 2 eigenvectors, got {eigvecs.shape[1]}")
        
        # Sort in descending variance order
        order = eigvals.argsort()[::-1]
        eigvals = eigvals[order]
        eigvecs = eigvecs[:, order]
        
        # Extract principal components more safely
        pc1 = eigvecs[:, 0]  # First principal component
        pc2 = eigvecs[:, 1]  # Second principal component

        # Helper to turn 2‑D vector → Manim 3‑D point
        def v(*xy):
            x, y = xy
            return np.array([x, y, 0])

        # 3) Draw principal component line (scaled to visual length)
        scale = 5

        arrow_pc1 = Line3D(
            start=-pc1 * scale,
            end=pc1 * scale,
            color=YELLOW,
            stroke_width=6,
        )
        self.play(Create(arrow_pc1))
        self.wait(0.5)

        # 5) Project each dot onto PC‑1 and show its 1‑D representation
        projections = VGroup()
        projection_lines = VGroup()
        for x, y, z in data:
            proj_len = np.dot([x, y, z], pc1)  # scalar coordinate along PC-1
            proj_point = proj_len * pc1  # 3-D coordinates on the PC-1 axis
            proj_dot = Dot3D(point=proj_point, radius=self.DOT_RADIUS, color=RED)
            projections.add(proj_dot)

            # Connecting line from each point to its projection on PC-1 (dashed gray for clarity)
            line = DashedLine(
                start=[x, y, z],
                end=proj_point,
                dash_length=0.1,
                stroke_opacity=0.6,
                color=GRAY,
            )
            projection_lines.add(line)

        self.play(LaggedStart(*[Create(line) for line in projection_lines], lag_ratio=0.02))
        self.play(Transform(dots.copy(), projections))
        self.wait(0.5)

        # 6) Fade unnecessary elements to leave only the 1‑D projection + PC‑1 axis
        self.play(FadeOut(projection_lines), FadeOut(axes))
        axis_line = Line3D(start=-pc1 * scale, end=pc1 * scale, color=YELLOW, stroke_width=6)
        self.play(Transform(arrow_pc1, axis_line))

        # --- Camera motion to highlight the collapsed 1-D subspace (inspired by the 3-D animation) ---
        frame = self.camera.frame
        # Zoom in and center on the principal component axis
        self.play(frame.animate.scale(0.7).move_to(axis_line.get_center()), run_time=2)
        self.wait(0.3)

        # 7) Title showing dimensionality reduction
        title = Text("Collapsed to 1-D along PC-1", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(2)

        # Final subtle rotation to echo the cinematic sweep
        self.play(frame.animate.rotate(PI/12, about_point=axis_line.get_center()), run_time=2)
        self.wait(1)

        # Hold final frame
        self.wait()



