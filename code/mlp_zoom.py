from manim import *

class MLPZoomNetwork(Scene):
    def construct(self):
        # Create network components
        network, dotted_connections, solid_connections = self.create_mlp_model()
        
        # Center the entire network
        full_network = VGroup(network, dotted_connections, solid_connections)
        full_network.move_to(ORIGIN)
        
        # Create equation h = W*x on top of network
        equation = MathTex(r"h = W \cdot x", font_size=48)
        equation.move_to(full_network.get_top() + UP * 0.8)
        
        # Prepare layer connections for animation
        layer_connections_list = []
        for i, layer in enumerate(network):
            if i < len(network) - 1:
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
                layer_connections_list.append(layer_connections)
            else:
                layer_connections_list.append([])
        
        # Prepare zoom elements
        last_two_layers = VGroup(network[-2], network[-1])  # Last 2 layers (3 -> 2)
        last_layer_connections = solid_connections          # Connections between last 2 layers
        focus_group = VGroup(last_two_layers, last_layer_connections)
        fade_group = VGroup(network[:-2], dotted_connections, equation)
        scale_factor = 1.2
        
        # Prepare input vector elements
        left_layer = last_two_layers[0]  # 3 neurons (index order: bottom, mid, top)
        nums_spec = [
            ("0.6", 0),  # bottom
            ("0.7", 1),  # middle
            ("0.3", 2),  # top
        ]
        # Consistent horizontal gap for labels
        label_gap = 0.25

        side_nums = VGroup()
        for txt, idx in nums_spec:
            t = MathTex(txt).scale(0.8).set_color(WHITE)
            # Place exactly label_gap units from neuron's left edge
            t.set_x(left_layer[idx].get_left()[0] - label_gap - t.get_width()/2)
            t.set_y(left_layer[idx].get_y())
            side_nums.add(t)
        
        # Create arrows and labels for the input neurons
        arrow_gap = 0.8
        arrows = VGroup()
        feature_labels = VGroup()
        feature_names = ["furry", "loyal", "golden"]  # bottom, middle, top

        # Position arrows based on the actual left edge of the number glyphs
        for num_label, feature_name in zip(side_nums, feature_names):
            left_x = num_label.get_left()[0]
            y_pos = num_label.get_y()

            # Arrow points left, starting just to the left of the number
            arrow_start = [left_x - 0.12, y_pos, 0]
            arrow_end = [left_x - (0.12 + arrow_gap), y_pos, 0]
            feature_arrow = Arrow(start=arrow_start, end=arrow_end, buff=0, color=WHITE, stroke_width=1.5)
            arrows.add(feature_arrow)

            # Keep arrows glued to the numbers during transforms
            feature_arrow.add_updater(lambda m, n=num_label: m.put_start_and_end_on(
                [n.get_left()[0] - 0.12, n.get_y(), 0],
                [n.get_left()[0] - (0.12 + arrow_gap), n.get_y(), 0]
            ))

            # Feature label to the left of arrow end (and keep it following the arrow)
            label = Tex(feature_name, font_size=30, color=WHITE)
            label.next_to(feature_arrow.get_end(), LEFT, buff=0.2)
            label.add_updater(lambda m, a=feature_arrow: m.next_to(a.get_end(), LEFT, buff=0.2))
            feature_labels.add(label)

        # Keep left-side numbers aligned to their neurons during initial movements
        for (txt, idx), label in zip(nums_spec, side_nums):
            label.add_updater(
                lambda m, i=idx: m.set_x(
                    left_layer[i].get_left()[0] - label_gap - m.get_width()/2
                ).set_y(left_layer[i].get_y())
            )
        
        # Prepare result numbers for the right layer (aligned to neurons)
        right_layer = last_two_layers[1]
        right_side_nums = VGroup()
        right_nums_spec = [
            ("1.0", 0),  # bottom neuron value
            ("0.6", 1),  # top neuron value
        ]
        for txt, idx in right_nums_spec:
            r = MathTex(txt).scale(0.8).set_color(WHITE)
            # Place exactly label_gap units from neuron's right edge
            r.set_x(right_layer[idx].get_right()[0] + label_gap + r.get_width()/2)
            r.set_y(right_layer[idx].get_y())
            right_side_nums.add(r)

        # Keep right-side numbers aligned to their neurons during any subsequent transforms
        for (txt, idx), label in zip(right_nums_spec, right_side_nums):
            label.add_updater(
                lambda m, i=idx: m.set_x(
                    right_layer[i].get_right()[0] + label_gap + m.get_width()/2
                ).set_y(right_layer[i].get_y())
            )
        
        # Helper function for brackets
        def bracket_for(mobj, side=LEFT, xpad=0.15, hpad=0.08):
            top = mobj.get_top() + UP*hpad
            bot = mobj.get_bottom() + DOWN*hpad
            if side is LEFT:
                x = mobj.get_left()[0] - xpad
            else:
                x = mobj.get_right()[0] + xpad
            vert = Line([x, top[1], 0], [x, bot[1], 0], stroke_width=2)
            h1 = Line([x, top[1], 0], [x + (0.12 if side is LEFT else -0.12), top[1], 0], stroke_width=2)
            h2 = Line([x, bot[1], 0], [x + (0.12 if side is LEFT else -0.12), bot[1], 0], stroke_width=2)
            return VGroup(vert, h1, h2)
        
        # Prepare arrow elements (will be positioned after movements)
        arrow_start = None
        arrow_end = None
        arrow = None
        
        # Prepare matrix elements
        matrix_W = Matrix([
            ["1.0", "0.0", "0.5"],
            ["0.0", "1.0", "0.5"]
        ]).scale(0.8)
        W_label = MathTex("W = ").next_to(matrix_W, LEFT)
        matrix_group = VGroup(W_label, matrix_W)
        
        # Prepare transformation elements
        input_vec_col = Matrix([["0.3"], ["0.7"], ["0.6"]]).scale(0.8)
        iv_entries = input_vec_col.get_entries()
        iv_entries[0].set_color(WHITE)
        iv_entries[1].set_color(WHITE)
        iv_entries[2].set_color(WHITE)
        
        # Prepare result elements
        equal_sign = MathTex("=")
        result_vec = Matrix([["0.6"], ["1.0"]]).scale(0.8)
        
        # --- ALL ANIMATIONS BELOW ---
        
        # Create neurons, edges, and equation
        equation_written = False
        for i, layer in enumerate(network):
            animations = [GrowFromCenter(node) for node in layer]
            if layer_connections_list[i]:
                animations += [Create(edge) for edge in layer_connections_list[i]]
                if not equation_written:
                    animations.append(Create(equation))
                    equation_written = True
            self.play(*animations, run_time=1.0)
        self.wait(0.3)
        
        # Zoom in on last 2 layers and fade the rest
        self.play(
            FadeOut(fade_group, run_time=1.5),
            focus_group.animate.scale(scale_factor).move_to(ORIGIN),
            run_time=2.0
        )

        # Show input vector with arrows and labels
        self.play(
            FadeIn(side_nums, shift=LEFT * 0.8), 
            *[GrowArrow(arrow) for arrow in arrows],
            *[FadeIn(label) for label in feature_labels],
            run_time=0.8
        )
        
        # Make the input vector, arrows, and labels follow the focus group move
        focus_group.add(side_nums, arrows, feature_labels)

        # Move to upper area (the input vector follows because it's in focus_group)
        self.play(focus_group.animate.to_edge(UP, buff=0.5), run_time=1.0)
        
        # Create and position arrow (after movements are complete)
        # Anchor relative to the last two layers + their connections only,
        # so side annotations don't affect placement.
        anchor_group = VGroup(last_two_layers, last_layer_connections)
        arrow_start = anchor_group.get_bottom() + DOWN * 0.3
        arrow_end = arrow_start + DOWN * 1.0
        arrow = Arrow(start=arrow_start, end=arrow_end, color=WHITE, stroke_width=2, buff=0)
        matrix_group.move_to(arrow_end + DOWN * 1.0)
        
        # Dim neurons, arrows, labels and grow arrow simultaneously
        self.play(
            *[node.animate.set_opacity(0.2) for layer in last_two_layers for node in layer],
            side_nums.animate.set_opacity(0.2),
            arrows.animate.set_opacity(0.2),
            feature_labels.animate.set_opacity(0.2),
            GrowArrow(arrow),
            run_time=1.0
        )
        
        # Clear updaters immediately after dimming to prevent reappearance
        for feature_arrow in arrows:
            feature_arrow.clear_updaters()
        for flabel in feature_labels:
            flabel.clear_updaters()
        
        # Remove arrows and labels from focus_group to prevent them from following transforms
        focus_group.remove(arrows, feature_labels)
        
        # Morph a copy of connections into the matrix for a nice reveal
        connections_copy = solid_connections.copy()
        connections_copy.set_color(WHITE).set_stroke(opacity=0.9, width=4)
        self.play(Write(W_label), ReplacementTransform(connections_copy, matrix_W), run_time=1.5)
        self.wait(0.2)

        # Fade out arrow + 'W =', slide matrix into W's spot
        w_center = W_label.get_center()
        self.play(
            FadeOut(arrow),
            FadeOut(W_label),
            matrix_W.animate.move_to(w_center + RIGHT*0.35),
            run_time=0.8
        )

        # Position elements for final equation
        input_vec_col.next_to(matrix_W, RIGHT, buff=0.35)
        equal_sign.next_to(input_vec_col, RIGHT, buff=0.35)
        result_vec.next_to(equal_sign, RIGHT, buff=0.35)

        # Remove left-side updaters before transforming the side vector into the column vector
        for label in side_nums:
            label.clear_updaters()

        # Fade out arrows and labels first, then do the transformation
        self.play(
            FadeOut(arrows),
            FadeOut(feature_labels),
            run_time=0.3
        )
        
        # Fully remove arrows/labels from scene immediately
        self.remove(arrows, feature_labels)
        
        # Quick flash on neurons while transforming the side vector into the column vector
        self.play(
            LaggedStart(
                Flash(left_layer[2], color=YELLOW),
                Flash(left_layer[1], color=YELLOW),
                Flash(left_layer[0], color=YELLOW),
                lag_ratio=0.15
            ),
            Transform(side_nums, input_vec_col),
            run_time=1.2
        )

        # Quick flash of the connections to imply multiplication
        self.play(Indicate(solid_connections, scale_factor=1.02), run_time=0.35)

        # Show '=' and the resulting vector [0.6, 1.0]
        self.play(FadeIn(equal_sign), FadeIn(result_vec), run_time=0.7)
        
        # Re-align right-side numbers to current neuron positions (after all moves)
        for (txt, idx), label in zip(right_nums_spec, right_side_nums):
            label.set_x(right_layer[idx].get_right()[0] + label_gap + label.get_width()/2)
            label.set_y(right_layer[idx].get_y())

        # Flash neurons on right layer and reveal their numbers
        self.play(
            LaggedStart(
                Flash(right_layer[1], color=YELLOW),
                Flash(right_layer[0], color=YELLOW),
                lag_ratio=0.15
            ),
            FadeIn(right_side_nums, shift=RIGHT * 0.8),
            run_time=1.0
        )
        self.play(FadeOut(right_side_nums))
        # Numbers are placed; no more movement expected, so remove updaters
        for label in right_side_nums:
            label.clear_updaters()
        self.wait(2)

    def create_mlp_model(self, color=BLUE):
        network = VGroup()
        layers = 4
        nodes_per_layer = [3, 5, 3, 2]  # Updated last 2 layers to be 3 and 2 neurons
        layer_spacing = 2.0

        # Create nodes for each layer
        for i in range(layers):
            layer = VGroup()
            for j in range(nodes_per_layer[i]):
                node = Circle(radius=0.2, color=color)
                node.set_fill(color, opacity=0.3)
                node.set_stroke(color, width=2)
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
                            stroke_opacity=0.9,
                            stroke_width=4,
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
        
        return network, dotted_connections, solid_connections