from manim import *
import numpy as np
import random

class NetworkCompressionVisualization(Scene):
    def construct(self):
        # Create title
        title = Text("Neural Network Compression Hypothesis", font_size=36).to_edge(UP)
        subtitle = Text("Dense models as compressed representations of sparse systems", 
                       font_size=24, color=GRAY).next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        
        # Create the large virtual network (right side)
        large_network = self.create_large_sparse_network()
        large_network.shift(RIGHT * 4)
        
        # Create the compressed network (left side)
        small_network = self.create_small_dense_network()
        small_network.shift(LEFT * 4)
        
        # Add parameter count labels
        large_label = Text("Virtual Sparse System\n(Conceptual Scale)", 
                          font_size=20, color=BLUE).next_to(large_network, DOWN, buff=0.5)
        small_label = Text("600 Billion Parameters\n(Dense Model)", 
                          font_size=20, color=GREEN).next_to(small_network, DOWN, buff=0.5)
        
        # Show the large virtual network first
        self.play(FadeIn(large_network), Write(large_label))
        self.wait(1)
        
        # Show the small dense network
        self.play(FadeIn(small_network), Write(small_label))
        self.wait(1)
        
        # Create and show the projector
        projector = self.create_projector()
        projector.move_to(ORIGIN + UP * 0.5)
        
        # Create projection beam
        beam = self.create_projection_beam()
        
        self.play(FadeIn(projector))
        self.wait(0.5)
        
        # Show projection beam
        self.play(Create(beam))
        self.wait(1)
        
        # Add compression explanation
        compression_text = Text("Compression Process", font_size=24, color=YELLOW)
        compression_text.next_to(projector, UP, buff=0.8)
        self.play(Write(compression_text))
        
        # Transform the large network into the small one
        # Create a copy of the large network for transformation
        large_network_copy = large_network.copy()
        
        # Animate the transformation
        self.play(
            Transform(large_network_copy, small_network),
            run_time=3,
            rate_func=smooth
        )
        
        self.wait(1)
        
        # Add final explanation
        explanation = Text("The dense model captures the essential patterns\nof the larger sparse system", 
                          font_size=20, color=WHITE).to_edge(DOWN)
        self.play(Write(explanation))
        
        self.wait(3)
        
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
        """Create a projector visualization"""
        # Main projector body
        body = Rectangle(width=1.0, height=0.6, color=GRAY, fill_opacity=0.8)
        
        # Lens
        lens = Circle(radius=0.15, color=WHITE, fill_opacity=0.9).shift(RIGHT * 0.4)
        
        # Projection symbol
        projection_lines = VGroup()
        for i in range(3):
            angle = (i - 1) * 0.3
            line = Line(ORIGIN, [0.8 * np.cos(angle), 0.8 * np.sin(angle), 0], 
                       color=YELLOW, stroke_width=2)
            line.shift(RIGHT * 0.55)
            projection_lines.add(line)
        
        projector = VGroup(body, lens, projection_lines)
        return projector
    
    def create_projection_beam(self):
        """Create the projection beam from projector"""
        # Create a triangular beam
        beam_points = [
            [-0.5, 0.1, 0],   # Left top
            [-0.5, -0.1, 0],  # Left bottom
            [0.5, -0.3, 0],   # Right bottom
            [0.5, 0.3, 0],    # Right top
        ]
        
        beam = Polygon(*beam_points, color=YELLOW, fill_opacity=0.2, stroke_opacity=0.5)
        return beam