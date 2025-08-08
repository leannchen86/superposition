from manim import *

class NeuralNetworkVisualization(Scene):
    """Draws a feed-forward network with ellipsis support and white background.
    The first layer has fewer nodes and smaller height than other layers."""

    def construct(self):
        
        # Fetch only the network VGroup (layers + connection groups)
        network = self.create_mlp_model()
        
        # Initial fade in
        self.play(FadeIn(network), run_time=0.5)
        self.wait(0.5)
        
        # Extract layers and connections from the network
        layer_sizes = [3, 5, 5, 5, 2]
        num_layers = len(layer_sizes)
        
        # Separate layers and connections
        layers = VGroup(*[network[i] for i in range(num_layers)])
        connections = VGroup(*[network[i] for i in range(num_layers, len(network))])
        
        # Create MathTex labels and arrows for hidden layers
        hidden_layer_indices = [1, 2, 3]  # indices of hidden layers (excluding input & output)
        label_numbers = ["786", "2048", "256"]
        label_groups = VGroup()
        for idx, layer_idx in enumerate(hidden_layer_indices):
            layer = layers[layer_idx]
            # Calculate arrow start/end so it is short and points down to the layer
            arrow_end = layer.get_top() + UP * 0.05
            arrow_start = arrow_end + UP * 0.3  # short arrow length (~0.25-0.3)
            arrow = Arrow(
                arrow_start,
                arrow_end,
                buff=0,
                color=BLUE,
                stroke_width=1.5,
            )
            label = MathTex(label_numbers[idx], color=BLUE).scale(0.6)
            label.next_to(arrow, UP, buff=0.05)
            group = VGroup(label, arrow).set_opacity(0)  # start invisible
            label_groups.add(group)
        # Add the label groups to the scene so we can animate their opacity later
        self.add(label_groups)
        
        # Animate through each layer
        for i in range(num_layers):
            # Create animations list
            animations = []
            
            # Dim all layers and connections first
            for j, layer in enumerate(layers):
                if j != i:  # Dim other layers
                    for node in layer:
                        if isinstance(node, (Circle, VGroup)):
                            animations.append(
                                node.animate.set_fill(opacity=0.1).set_stroke(opacity=0.3)
                            )

                else:  # Highlight current layer
                    for node in layer:
                        if isinstance(node, (Circle, VGroup)):
                            animations.append(
                                node.animate.set_fill(opacity=0.9).set_stroke(opacity=1, width=2)
                            )

            # Show or hide the label corresponding to this layer
            for idx, layer_idx in enumerate(hidden_layer_indices):
                target_opacity = 1 if i == layer_idx else 0
                animations.append(label_groups[idx].animate.set_opacity(target_opacity))

            # Keep connections unchanged while iterating through layers
            # (previously we animated their opacity based on the current layer)
            # for j, conn_group in enumerate(connections):
            #     if j == i:
            #         animations.append(conn_group.animate.set_stroke(opacity=0.6, width=1.5))
            #     else:
            #         animations.append(conn_group.animate.set_stroke(opacity=0.1, width=0.5))
            
            # Play all animations together
            self.play(*animations, run_time=0.5)
            self.wait(0.1)
        
        # Reset to normal at the end
        reset_animations = []
        
        # Reset all layers
        for i, layer in enumerate(layers):
            for node in layer:
                if isinstance(node, Circle):
                    reset_animations.append(
                        node.animate.set_fill(opacity=0.3).set_stroke(opacity=1, width=2)
                        )
                elif isinstance(node, VGroup):
                    reset_animations.append(
                        node.animate.set_fill(opacity=0.9).set_stroke(opacity=1, width=2)
                    )
        
        # Reset all connections
        for conn_group in connections:
            reset_animations.append(
                conn_group.animate.set_stroke(opacity=0.4, width=0.7)
            )
        
        # Hide all labels at the end
        for group in label_groups:
            reset_animations.append(group.animate.set_opacity(0))
        
        self.play(*reset_animations, run_time=0.5)
        self.wait(0.5)

    def create_mlp_model(self, color=BLUE):
        """Create neural network with proper structure and ellipsis support"""
        # Configuration
        layer_sizes = [3, 5, 5, 5, 2]  # actual neuron counts
        max_visible = 3  # max neurons to show before ellipsis
        layer_spacing = 2.5
        node_radius = 0.25

        # Create layers
        layers = VGroup()
        all_nodes = []  # Store actual nodes for connections
        
        for i, size in enumerate(layer_sizes):
            layer = VGroup()
            layer_nodes = []
            
            # Calculate x position (centered)
            x = (i - (len(layer_sizes) - 1) / 2) * layer_spacing
            
            # Determine which neurons to show
            if size <= max_visible:
                # Show all neurons
                visible_indices = list(range(size))
                show_ellipsis = False
            else:
                # Show first max_visible-1 and last one, with ellipsis
                visible_indices = list(range(max_visible - 1)) + [size - 1]
                show_ellipsis = True
            
            # Calculate vertical spacing
            if i == 0:  # Input layer - smaller height
                total_height = 1.5
            elif i == len(layer_sizes) - 1:  # Output layer - slightly smaller height
                total_height = 1.5
            else:  # Hidden layers - normal height
                total_height = 2.5

            # Calculate vertical spacing
            if show_ellipsis:
                # 3 visible neurons (top, middle, bottom) and one invisible slot for the ellipsis
                neuron_spacing = total_height / max_visible
            else:
                neuron_spacing = total_height / (size - 1) if size > 1 else 0

            # Create neurons
            for vis_idx, j in enumerate(visible_indices):
                # When we show an ellipsis, leave a gap (one slot) between the
                # second and the last visible neuron so the bottom neuron is
                # rendered beneath the ellipsis.
                if show_ellipsis and vis_idx == len(visible_indices) - 1:
                    eff_idx = vis_idx + 1  # skip the ellipsis slot
                else:
                    eff_idx = vis_idx

                y = total_height / 2 - eff_idx * neuron_spacing
                # For hidden layers (2nd, 3rd, 4th, ...), push the last visible
                # neuron a bit further down so it appears "way lower" than the
                # default bottom position. This gives more visual separation
                # between the ellipsis and the bottom neuron, as requested.
                if (
                    show_ellipsis
                    and vis_idx == len(visible_indices) - 1  # the last visible neuron
                    and 0 < i < len(layer_sizes) - 1  # hidden layers only
                ):
                    # Lower the neuron by an additional half-spacing
                    y -= 0.9 * neuron_spacing
                
                node = Circle(radius=node_radius, color=color)
                node.set_fill(color, opacity=0.3)
                node.set_stroke(color, width=2)
                node.move_to([x, y, 0])
                layer.add(node)
                layer_nodes.append(node)
            
            # Add ellipsis if needed
            if show_ellipsis:
                # Position the ellipsis midway between the second and last neurons
                ellipsis_idx = max_visible - 1  # slot reserved for the ellipsis
                ellipsis_y = total_height / 2 - (ellipsis_idx + 0.3) * neuron_spacing
                dots = VGroup()
                for k in range(3):
                    dot = Dot(
                        point=[x, ellipsis_y - k * 0.2, 0], 
                        radius=0.05,
                        color=color
                    )
                    dots.add(dot)
                layer.add(dots)
            
            layers.add(layer)
            all_nodes.append(layer_nodes)
        
        # Create connections
        # Store connection groups so we can animate them separately.
        # First: connections between **consecutive layers**
        
        connections_by_pair = []

        # Only create connections between immediate consecutive layers
        for i in range(len(layer_sizes) - 1):
            pair_connections = VGroup()

            for node1 in all_nodes[i]:
                for node2 in all_nodes[i + 1]:
                    connection = Line(
                        node1.get_center(),
                        node2.get_center(),
                        stroke_opacity=0.4,
                        stroke_width=0.7,
                        color=BLUE
                    )
                    pair_connections.add(connection)

            connections_by_pair.append(pair_connections)

        # Aggregate all connection pairs
        connections = VGroup(*connections_by_pair)
        
        # Return each layer followed by its corresponding connection VGroup so that the
        # indices match those referenced in construct():
        #   0 .. len(layers)-1   -> layers (input, hidden1, ... , output)
        #   len(layers) ..       -> connection groups between consecutive layers

        network = VGroup(*layers, *connections_by_pair)
        # Only keep layers and their immediate connections
        network = network[:len(layers) + len(connections_by_pair)]

        return network