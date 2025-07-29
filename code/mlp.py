from manim import *

class MLPNetwork(Scene):
    def construct(self):
        full_network = self.create_mlp_model()
        full_network.shift(LEFT * 12)
        self.add(full_network)
        # Slide MLP in from the left to center
        self.play(
            full_network.animate.move_to(ORIGIN).scale(1.05),
            rate_func=smooth,
            run_time=1.5
        )
        self.wait(0.5)
    
    def create_mlp_model(self, color=BLUE):
            # text for the neural network
            #correct the equation with the right format
            # z = W*x + b
            network_equation = MathTex("z = W*x + b").shift(3*UP)
            self.play(FadeIn(network_equation), run_time=0.5)

            network = VGroup()
            layers = 4
            nodes_per_layer = [3, 5, 5, 2]

            for i in range(layers):
                layer = VGroup()
                for j in range(nodes_per_layer[i]):
                    node = Circle(radius=0.3, color=color)
                    node.set_fill(color, opacity=0.3)
                    node.move_to([i * 2 - 6, j - (nodes_per_layer[i] - 1) / 2, 0])
                    layer.add(node)
                network.add(layer)

            connections = VGroup()
            for i in range(layers - 1):
                for node1 in network[i]:
                    for node2 in network[i + 1]:
                        connection = Line(
                            node1.get_center(),
                            node2.get_center(),
                            stroke_opacity=0.4,
                            stroke_width=0.7,
                            stroke_color=color
                        )
                        connections.add(connection)
            
            full_network = VGroup(network, connections)

            return full_network