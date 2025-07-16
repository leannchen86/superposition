from manim import *
import numpy as np

class VectorAnimation(ThreeDScene):
    def construct(self):
        # Set camera to perspective view
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        self.camera.set_focal_distance(20)

        # Define the origin position
        origin_pos = ORIGIN
        
        # Set up 3D axes positioned to the right half of the screen
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1], 
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        axes.shift(origin_pos)  # Move axes to the right
        self.add(axes)

        # Scale factor for vectors (80% of unit length in the scaled coordinate system)
        vector_scale = 2
        
        # Generate 5 random initial directions (normalized)
        np.random.seed(42)  # For reproducible results
        initial_directions = []
        for _ in range(5):
            # Generate random direction
            direction = np.random.randn(3)
            direction = direction / np.linalg.norm(direction)
            initial_directions.append(direction)
        
        # Calculate target positions for equidistant angles
        # Using 5 vertices of a regular dodecahedron for optimal 3D distribution
        phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        
        # These are 5 well-distributed points on a sphere
        target_directions = np.array([
            [1, 1, 1],
            [1, -1, -1],
            [-1, 1, -1],
            [-1, -1, 1],
            [0, phi, 1/phi]
        ])
        
        # Normalize target directions
        for i in range(5):
            target_directions[i] = target_directions[i] / np.linalg.norm(target_directions[i])
        
        # Create vectors with different colors
        colors = [RED, BLUE, GREEN, YELLOW, PURPLE]
        vectors = []
        
        # Create initial vectors
        for i in range(5):
            vector = Arrow3D(
                start=origin_pos,
                end=origin_pos + initial_directions[i] * vector_scale,
                color=colors[i],
                thickness=0.02
            )
            vectors.append(vector)
            self.add(vector)
        
        # Animation function for smooth interpolation
        def update_vectors(mob, alpha):
            for i, vector in enumerate(vectors):
                # Linear interpolation between initial and target directions
                current_direction = (1 - alpha) * initial_directions[i] + alpha * target_directions[i]
                current_direction = current_direction / np.linalg.norm(current_direction)
                
                # Update vector end point
                new_end = origin_pos + current_direction * vector_scale
                vector.become(Arrow3D(
                    start=origin_pos,
                    end=new_end,
                    color=colors[i],
                    thickness=0.02
                ))
        
        # Create the animation using UpdateFromAlphaFunc
        animation = UpdateFromAlphaFunc(
            VGroup(*vectors),
            update_vectors,
            run_time=4,
            rate_func=smooth
        )
        
        # Display initial state briefly
        self.wait(1)
        
        # Run the animation
        self.play(animation)
        
        # Hold final state
        self.wait(2)