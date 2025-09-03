from manim import *

class MLPNetwork(Scene):
    def construct(self):
        # Create and position the network at center
        full_network = self.create_mlp_model()
        full_network.move_to(ORIGIN).scale(1.05)
        self.add(full_network)
        
        self.wait(0.5)
        
        # Add concept meteors animation
        self.animate_concept_meteors(full_network)
        
        # Hold the final scene
        self.wait(2)
    
    def create_mlp_model(self, color=BLUE):        
        network = VGroup()
        layers = 4
        nodes_per_layer = [3, 4, 4, 2]
        
        # Store node positions for later reference
        self.node_positions = []
        
        for i in range(layers):
            layer = VGroup()
            layer_positions = []
            for j in range(nodes_per_layer[i]):
                node = Circle(radius=0.3, color=color)
                node.set_fill(color, opacity=0.3)
                position = [i * 2 - 3, j - (nodes_per_layer[i] - 1) / 2, 0]
                node.move_to(position)
                layer.add(node)
                layer_positions.append(position)
            network.add(layer)
            self.node_positions.append(layer_positions)
        
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
    
    def animate_concept_meteors(self, network):
        # Concepts to animate
        concepts = ["floppy ears", "bright", "gloomy", "trees", "dogs"]
        
        # Create meteor objects
        meteors = VGroup()
        meteor_trails = VGroup()
        
        for i, concept in enumerate(concepts):
            # Create concept text
            concept_text = Text(concept, font_size=20, color=YELLOW)
            
            # Position on upper left and upper right corners, alternating
            if i % 2 == 0:  # Even indices come from upper left
                start_x = -8
                start_y = 4
            else:  # Odd indices come from upper right
                start_x = 8
                start_y = 4
            
            concept_text.move_to([start_x, start_y, 0])
            
            # Create realistic comet with downward head and upward expanding tail
            # Position text above the comet
            comet_center = concept_text.get_center() + DOWN * 0.6
            concept_text.move_to(concept_text.get_center() + UP * 0.3)
            
            comet_head = Circle(
                radius=0.15, 
                fill_color=YELLOW, 
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=2
            ).move_to(comet_center + DOWN * 0.1)
            
            # Create shorter expanding tail pointing upward
            tail_lines = VGroup()
            num_tail_segments = 4  # Reduced from 6 to 4
            for j in range(num_tail_segments):
                # Each segment gets progressively wider and more transparent
                tail_width = 2 + j * 1.2
                tail_opacity = 0.8 - j * 0.15
                tail_length = 0.25 + j * 0.15  # Shorter segments
                
                # Create expanding tail segments pointing upward
                tail_segment = Line(
                    comet_center + UP * (j * 0.2),  # Closer spacing
                    comet_center + UP * (j * 0.2 + tail_length),
                    stroke_width=tail_width,
                    stroke_color=YELLOW,
                    stroke_opacity=tail_opacity
                )
                
                # Add slight spreading effect only for outer segments
                if j > 1:
                    left_spread = Line(
                        comet_center + UP * (j * 0.2) + LEFT * (j - 1) * 0.08,
                        comet_center + UP * (j * 0.2 + tail_length) + LEFT * (j - 1) * 0.12,
                        stroke_width=tail_width * 0.6,
                        stroke_color=YELLOW,
                        stroke_opacity=tail_opacity * 0.6
                    )
                    right_spread = Line(
                        comet_center + UP * (j * 0.2) + RIGHT * (j - 1) * 0.08,
                        comet_center + UP * (j * 0.2 + tail_length) + RIGHT * (j - 1) * 0.12,
                        stroke_width=tail_width * 0.6,
                        stroke_color=YELLOW,
                        stroke_opacity=tail_opacity * 0.6
                    )
                    tail_lines.add(left_spread, right_spread)
                
                tail_lines.add(tail_segment)
            
            # Create the complete comet
            comet_visual = VGroup(comet_head, tail_lines)
            
            # Add updater to make comet follow the text while maintaining orientation
            # Keep comet positioned below the text
            comet_visual.add_updater(lambda m, ct=concept_text: m.move_to(
                ct.get_center() + DOWN * 0.6
            ))
            
            meteor = VGroup(comet_visual, concept_text)
            meteors.add(meteor)
            meteor_trails.add(comet_visual)
        
        # Add meteors to scene
        self.add(meteors)
        
        # Animate meteors flying to random positions in the network
        import random
        random.seed(42)  # For consistent random positions
        
        animations = []
        for i, meteor in enumerate(meteors):
            # Choose random target position within the network bounds
            left = network.get_left()[0]
            right = network.get_right()[0]
            bottom = network.get_bottom()[1]
            top = network.get_top()[1]
            target_x = random.uniform(left, right)
            target_y = random.uniform(bottom, top)
            target_pos = [target_x, target_y, 0]
            
            # Create path with slight curve
            if i % 2 == 0:  # Coming from upper left
                path = ArcBetweenPoints(meteor.get_center(), target_pos, angle=PI/4)
            else:  # Coming from upper right
                path = ArcBetweenPoints(meteor.get_center(), target_pos, angle=-PI/4)
            animations.append(
                MoveAlongPath(meteor, path, rate_func=rate_functions.ease_in_quad)
            )
        
        # Play all meteor animations with quick staggered timing
        for i, (meteor, animation) in enumerate(zip(meteors, animations)):
            self.wait(0.8)
            self.play(
                animation,
                run_time=1.5
            )
            
            # Simple fade out when meteor lands
            self.play(
                FadeOut(meteor, scale=0.5),
                run_time=0.3
            )
