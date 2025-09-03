from manim import *
import numpy as np

class NeuralNetwork(Scene):
    def construct(self):
        # Title equation
        title = MathTex("h = Wx", "\\quad\\text{or}\\quad", "z = Wx")
        title.scale(1.2)
        title.to_edge(UP)
        
        # Define the network architecture
        layers = [3, 4, 3]  # 3 input nodes, 4 hidden nodes, 3 output nodes
        
        # Create nodes for each layer
        network_nodes = []
        layer_spacing = 4
        
        for i, layer_size in enumerate(layers):
            layer_nodes = []
            x_pos = (i - 1) * layer_spacing
            
            # Calculate vertical spacing for nodes in this layer
            if layer_size == 1:
                y_positions = [0]
            else:
                y_spacing = 3.5 / (layer_size - 1) if layer_size > 1 else 0
                y_positions = [(j - (layer_size - 1) / 2) * y_spacing for j in range(layer_size)]
            
            for j, y_pos in enumerate(y_positions):
                node = Circle(radius=0.3, color=WHITE, fill_opacity=0)
                node.set_stroke(WHITE, width=2)
                node.move_to([x_pos, y_pos, 0])
                layer_nodes.append(node)
            
            network_nodes.append(layer_nodes)
        
        # Create edges between layers
        edges_layer1_to_2 = []  # Dotted connections
        edges_layer2_to_3 = []  # Solid connections
        
        # Connect input layer to hidden layer (dotted lines)
        for input_node in network_nodes[0]:
            for hidden_node in network_nodes[1]:
                edge = Line(
                    input_node.get_center(),
                    hidden_node.get_center(),
                    stroke_width=1.5,
                    color=GRAY
                )
                edge.set_stroke(opacity=0.6)
                # Make it dotted
                edge.add_updater(lambda m: m.set_stroke(GRAY, width=1.5))
                edge.get_dashed_line = lambda: DashedLine(
                    input_node.get_center(),
                    hidden_node.get_center(),
                    dash_length=0.1,
                    stroke_width=1.5,
                    color=GRAY,
                    stroke_opacity=0.6
                )
                edges_layer1_to_2.append(
                    DashedLine(
                        input_node.get_center(),
                        hidden_node.get_center(),
                        dash_length=0.1,
                        stroke_width=1.5,
                        color=GRAY,
                        stroke_opacity=0.6
                    )
                )
        
        # Connect hidden layer to output layer (solid lines)
        for hidden_node in network_nodes[1]:
            for output_node in network_nodes[2]:
                edge = Line(
                    hidden_node.get_center(),
                    output_node.get_center(),
                    stroke_width=2,
                    color=WHITE,
                    stroke_opacity=0.8
                )
                edges_layer2_to_3.append(edge)
        
        # Group all elements
        all_nodes = VGroup(*[node for layer in network_nodes for node in layer])
        all_edges_dotted = VGroup(*edges_layer1_to_2)
        all_edges_solid = VGroup(*edges_layer2_to_3)
        
        # Center the entire network
        full_network = VGroup(all_edges_dotted, all_edges_solid, all_nodes)
        full_network.move_to(ORIGIN)
        
        # Animation sequence - all self.play calls at the end
        self.play(Write(title))
        self.wait(0.5)
        
        # Animate nodes appearing
        for i, layer in enumerate(network_nodes):
            self.play(
                *[GrowFromCenter(node) for node in layer],
                run_time=0.8
            )
        
        # Animate dotted edges (first layer connections)
        self.play(
            *[Create(edge) for edge in edges_layer1_to_2],
            run_time=1.5
        )
        
        # Animate solid edges (second layer connections)
        self.play(
            *[Create(edge) for edge in edges_layer2_to_3],
            run_time=1.5
        )
        
        # Add some pulsing animation to show signal flow
        self.wait(1)
        
        # Optional: Add a signal propagation animation
        for _ in range(2):
            # Highlight input layer
            self.play(
                *[node.animate.set_fill(BLUE, opacity=0.5) for node in network_nodes[0]],
                run_time=0.5
            )
            
            # Propagate to hidden layer
            self.play(
                *[node.animate.set_fill(GREEN, opacity=0.5) for node in network_nodes[1]],
                *[node.animate.set_fill(WHITE, opacity=0) for node in network_nodes[0]],
                run_time=0.5
            )
            
            # Propagate to output layer
            self.play(
                *[node.animate.set_fill(RED, opacity=0.5) for node in network_nodes[2]],
                *[node.animate.set_fill(WHITE, opacity=0) for node in network_nodes[1]],
                run_time=0.5
            )
            
            # Reset
            self.play(
                *[node.animate.set_fill(WHITE, opacity=0) for node in network_nodes[2]],
                run_time=0.5
            )
            
        self.wait(2)