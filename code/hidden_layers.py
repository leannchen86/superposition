#create network with customizable layers and ellipsis to indicate additional (hidden) neurons

from manim import (
    VGroup,
    Circle,
    Tex,
    Text,
    Line,
    RIGHT,
    LEFT,
    UP,
    ORIGIN,
    BLUE,
    GREEN,
    Scene,
    FadeIn,
    smooth,
)


def create_mlp_model(color: str = BLUE, nodes_per_layer: list[int] | None = None):
    """Return a VGroup containing an MLP diagram similar to the reference image.

    Parameters
    ----------
    color : Manim color, optional
        Base colour used for the neurons and connections.
    nodes_per_layer : list[int], optional
        Number of real neurons for every layer.  If a layer has more than
        3 neurons only three will be shown (top, bottom and one in-between) and
        a vertical ellipsis (⋮) will be drawn to indicate the hidden ones.
        Defaults to ``[3, 5, 5, 2]`` (3 input, 2 hidden layers with 5 neurons
        each and 2 outputs).
    """

    if nodes_per_layer is None:
        nodes_per_layer = [3, 5, 5, 2]

    layers = len(nodes_per_layer)
    network = VGroup()

    # ------------------------------------------------------------------
    # Build the visible neurons for every layer
    # ------------------------------------------------------------------
    for i, real_count in enumerate(nodes_per_layer):
        layer = VGroup()

        # Decide which neurons to actually draw               ───────────
        if real_count <= 3:
            # draw them all – keep the original vertical positions         
            visible_indices = list(range(real_count))
        else:
            # Show first, last and one in the middle (index ~ real_count/2)
            middle_idx = real_count // 2
            visible_indices = [0, middle_idx, real_count - 1]
        
        # Compute the vertical centre of the full (real) layer so that the
        # diagram stays vertically centred irrespective of `real_count`.
        y_offset = - (real_count - 1) / 2

        # Draw the visible neurons
        for j in visible_indices:
            y_pos = j + y_offset
            node = Circle(radius=0.2, color=color)
            node.set_fill(color, opacity=0.3)
            node.move_to([i * 2 - 6, y_pos, 0])  # x, y, z
            layer.add(node)

        # Add a vertical ellipsis if some neurons are hidden
        if real_count > len(visible_indices):
            ellipsis = Tex(r"\vdots", font_size=36)
            ellipsis.move_to([i * 2 - 6, 0, 0])
            layer.add(ellipsis)

        network.add(layer)

    # ------------------------------------------------------------------
    # Draw the fully-connected edges (ignore ellipsis symbols)
    # ------------------------------------------------------------------
    connections = VGroup()
    for i in range(layers - 1):
        for node1 in network[i]:
            if not isinstance(node1, Circle):
                continue
            for node2 in network[i + 1]:
                if not isinstance(node2, Circle):
                    continue
                connection = Line(
                    node1.get_center(),
                    node2.get_center(),
                    stroke_opacity=0.4,
                    stroke_width=0.7,
                    stroke_color=color,
                )
                connections.add(connection)

    # ------------------------------------------------------------------
    # Optional labels (left/right of network)
    # ------------------------------------------------------------------
    inputs = [
        Tex("Input 1", font_size=30).next_to(network[0][0], LEFT),
        Tex(r"\vdots", font_size=30).next_to(network[0][1], LEFT),
        Tex("Input n", font_size=30).next_to(network[0][-1], LEFT),
    ]
    outputs = [
        Tex("Output 1", font_size=30, color=GREEN).next_to(network[-1][0], RIGHT),
        Tex(r"\vdots", font_size=30, color=GREEN).next_to(network[-1][1], RIGHT),
        Tex("Output m", font_size=30, color=GREEN).next_to(network[-1][-1], RIGHT),
    ]

    return VGroup(network, connections), inputs, outputs


class MLPDiagram(Scene):
    """Minimal Scene that renders the MLP diagram so Manim can run it directly."""

    def construct(self):
        # Create the network diagram and a title
        mlp_model, inputs, outputs = create_mlp_model()
        mlp_title = Text("Multilayer Perceptron", font_size=36).to_edge(UP)

        # Place the model off‐screen to the left for an entrance animation
        mlp_model.shift(LEFT * 4)
        mlp_title.shift(UP * 2)

        # Fade everything in first
        self.play(FadeIn(VGroup(mlp_model, *inputs, *outputs, mlp_title)))
        self.wait(0.5)

        # Slide model and title to their final positions
        self.play(
            mlp_model.animate.move_to(ORIGIN).scale(1.2),
            mlp_title.animate.move_to(ORIGIN).to_edge(UP, buff=0.7).scale(1.2),
            rate_func=smooth,
            run_time=1.5,
        )
        self.wait(2)