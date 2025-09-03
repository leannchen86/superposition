from manim import *
import numpy as np
import random

class NetworkCompressionVisualization(Scene):
    def construct(self):
        # Create the large virtual network (right side)
        large_network = self.create_large_sparse_network()
        large_network.shift(RIGHT * 4)
        # Create the compressed network (left side)
        small_network = self.create_small_dense_network()
        small_network.shift(LEFT * 4)
        # Create and show the projector (positioned between networks)
        projector = self.create_projector()
        projector.move_to(LEFT * 0.8)
        # Create projection beam
        beam = self.create_projection_beam()
        # Transform the large network into the small one
        # Create a copy of the small network for transformation
        small_network_copy = small_network.copy()
        # Animate the transformation

        # Animation sequence - all self.play calls at the end
        self.play(FadeIn(small_network),
                  FadeIn(projector))
        self.wait(1)
                  
        self.play(
            Create(beam))
        self.play(
            Transform(small_network_copy, large_network),
            run_time=2.5,
            rate_func=smooth
        )
        self.wait(5)

        self.play(
            FadeOut(small_network),
            FadeOut(projector),
            FadeOut(beam),
            FadeOut(small_network_copy),
        )
        self.wait(2)

    def create_large_sparse_network(self):
        """Create a large, sparse-looking virtual network"""
        group = VGroup()
        
        # Create layers with many nodes but sparse connections
        layers = []
        layer_sizes = [12, 16, 20, 16, 12]  # Larger layers
        layer_positions = [i * 1.2 for i in range(len(layer_sizes))]
        
        # Create nodes for each layer
        all_nodes = []
        for i, (size, x_pos) in enumerate(zip(layer_sizes, layer_positions)):
            layer_nodes = []
            for j in range(size):
                y_pos = (j - size/2) * 0.3
                # Make nodes semi-transparent to look "virtual"
                node = Circle(radius=0.08, color=BLUE, fill_opacity=0.3, stroke_opacity=0.6)
                node.move_to([x_pos - 2.4, y_pos, 0])
                layer_nodes.append(node)
                group.add(node)
            all_nodes.append(layer_nodes)
            layers.append(layer_nodes)
        
        # Create sparse connections (only some connections)
        for i in range(len(layers) - 1):
            for node1 in layers[i]:
                # Only connect to some nodes in the next layer (sparse)
                connected_nodes = random.sample(layers[i + 1], 
                                              min(3, len(layers[i + 1])))
                for node2 in connected_nodes:
                    if np.random.random() > 0.7:  # Make it even sparser
                        line = Line(node1.get_center(), node2.get_center(), 
                                  color=BLUE, stroke_width=1, stroke_opacity=0.3)
                        group.add(line)
        
        return group
    
    def create_small_dense_network(self):
        """Create a smaller, dense network"""
        group = VGroup()
        
        # Create layers with fewer nodes but dense connections
        layers = []
        layer_sizes = [6, 8, 6, 4]  # Smaller layers
        layer_positions = [i * 1.0 for i in range(len(layer_sizes))]
        
        # Create nodes for each layer
        all_nodes = []
        for i, (size, x_pos) in enumerate(zip(layer_sizes, layer_positions)):
            layer_nodes = []
            for j in range(size):
                y_pos = (j - size/2) * 0.4
                # Make nodes solid and bright to look "real"
                node = Circle(radius=0.12, color=GREEN, fill_opacity=0.8, stroke_opacity=1)
                node.move_to([x_pos - 1.5, y_pos, 0])
                layer_nodes.append(node)
                group.add(node)
            all_nodes.append(layer_nodes)
            layers.append(layer_nodes)
        
        # Create dense connections
        for i in range(len(layers) - 1):
            for node1 in layers[i]:
                for node2 in layers[i + 1]:
                    # Dense connections (most nodes connected)
                    if np.random.random() > 0.2:
                        line = Line(node1.get_center(), node2.get_center(), 
                                  color=GREEN, stroke_width=1.5, stroke_opacity=0.7)
                        group.add(line)
        
        return group
    
    def create_projector(self):
        """Create a projector visualization with supporting feet"""
        # Main projector body - made smaller
        body = Rectangle(
            width=1.0,  # Smaller width
            height=0.5, # Smaller height
            fill_color=GRAY_D,
            fill_opacity=0.9,
            stroke_width=2,
            stroke_color=WHITE,
        )
        
        # Add two supporting feet as simple angled lines (45 degrees)
        left_foot = Line(
            start=body.get_bottom() + LEFT * 0.4,
            end=body.get_bottom() + LEFT * 0.4 + DOWN * 0.2,
            stroke_width=3,
            stroke_color=WHITE,
        )
        
        right_foot = Line(
            start=body.get_bottom() + RIGHT * 0.4,
            end=body.get_bottom() + RIGHT * 0.4 + DOWN * 0.2,
            stroke_width=3,
            stroke_color=WHITE,
        )
        
        projector = VGroup(body, left_foot, right_foot)
        return projector
    
    def create_projection_beam(self):
        """Create the projection beam from projector (adapted from 3D version)"""
        # Create light beam using polygon - less expanding
        def create_light_beam(start_point, end_point, width_start=0.1, width_end=0.6):  # Reduced expansion
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
        
        # Main light beam - start from right middle of projector (projector is at LEFT * 0.8)
        # Projector body width is 1.0, so right edge is at x = -0.8 + 0.5 = -0.3
        beam_start = np.array([-0.3, 0, 0])  # From right middle edge of projector
        beam_end = np.array([1.2, 0, 0])     # Beam extends to projection area
        main_beam = create_light_beam(beam_start, beam_end)
        
        # Additional light rays for realistic effect
        light_rays = VGroup()
        for i in range(5):
            offset_y = (i - 2) * 0.15
            ray_start = beam_start + np.array([0, offset_y * 0.3, 0])
            ray_end = beam_end + np.array([0, offset_y, 0])
            
            ray = create_light_beam(ray_start, ray_end, 0.05, 0.4)  # Less expanding rays
            ray.set_fill(YELLOW, opacity=0.2)
            light_rays.add(ray)
        
        return VGroup(main_beam, light_rays)