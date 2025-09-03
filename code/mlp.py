from manim import *

class MLPNetwork(Scene):
    def construct(self):
        # Create network components
        network, dotted_connections, solid_connections = self.create_mlp_model()
        
        # Center the entire network
        full_network = VGroup(network, dotted_connections, solid_connections)
        full_network.move_to(ORIGIN)
        
        # Animation sequence - create neurons and connections layer by layer
        for i, layer in enumerate(network):
            # Animate nodes appearing for current layer
            self.play(
                *[GrowFromCenter(node) for node in layer],
                run_time=0.8
            )
            
            # If not the last layer, animate connections to next layer
            if i < len(network) - 1:
                # Get connections from current layer to next layer
                layer_connections = []
                for node1 in network[i]:
                    for node2 in network[i + 1]:
                        if i == len(network) - 2:  # Last layer connections (solid)
                            for connection in solid_connections:
                                if (connection.get_start() == node1.get_center()).all() and \
                                   (connection.get_end() == node2.get_center()).all():
                                    layer_connections.append(connection)
                        else:  # Earlier layer connections (dotted)
                            for connection in dotted_connections:
                                if (connection.get_start() == node1.get_center()).all() and \
                                   (connection.get_end() == node2.get_center()).all():
                                    layer_connections.append(connection)
                
                # Animate these connections
                if layer_connections:
                    self.play(
                        *[Create(edge) for edge in layer_connections],
                        run_time=1.0
                    )
        
        self.wait(1)
    def create_mlp_model(self, color=BLUE):
            network = VGroup()
            layers = 4
            nodes_per_layer = [3, 5, 3, 2]  # Updated last 2 layers to be 3 and 2 neurons
            layer_spacing = 2.7  # Slightly narrower than before

            # Create nodes for each layer
            for i in range(layers):
                layer = VGroup()
                for j in range(nodes_per_layer[i]):
                    node = Circle(radius=0.3, color=color)
                    node.set_fill(color, opacity=0.3)
                    node.set_stroke(color, width=2)
                    # Use the increased layer_spacing
                    node.move_to([i * layer_spacing - (layers-1) * layer_spacing/2, 
                                 j - (nodes_per_layer[i] - 1) / 2, 0])
                    layer.add(node)
                network.add(layer)

            # Create connections with dotted lines for first layers, solid for last layer
            dotted_connections = VGroup()
            solid_connections = VGroup()
            
            for i in range(layers - 1):
                for node1 in network[i]:
                    for node2 in network[i + 1]:
                        if i == layers - 2:  # Last layer connections (solid)
                            connection = Line(
                                node1.get_center(),
                                node2.get_center(),
                                stroke_opacity=0.8,
                                stroke_width=2,
                                color=WHITE
                            )
                            solid_connections.add(connection)
                        else:  # Earlier layer connections (dotted)
                            connection = DashedLine(
                                node1.get_center(),
                                node2.get_center(),
                                dash_length=0.1,
                                stroke_width=1.5,
                                color=GRAY,
                                stroke_opacity=0.6
                            )
                            dotted_connections.add(connection)
            
            full_network = VGroup(network, dotted_connections, solid_connections)

            return full_network