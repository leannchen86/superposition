from manim import *

# Compatibility: some Manim builds use GRAY not GREY
if 'GREY' not in globals():
    try:
        GREY = GRAY  # type: ignore[name-defined]
    except Exception:
        pass

class ReLUAnimation(Scene):
    def construct(self):
        # Create the coordinate system
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-1, 10, 1],
            axis_config={"color": GREY},
            x_length=8,
            y_length=5,
        )
        # Add numeric labels at every 4 steps on both axes
        axes.add_coordinates(
            range(-8, 12, 4),  # x-axis labels
            range(0, 12, 4),    # y-axis labels
        )
        # Plot the ReLU function
        relu_graph = axes.plot(
            lambda x: max(0, x),
            x_range=[-10, 10],
            color=BLUE,
        )
        relu_graph.set_stroke(width=6)
        # Add a title to indicate this is a ReLU graph
        title = Tex("ReLU", font_size=48).to_edge(UP).shift(DOWN * 0.5)
        # Animate the scene: title first, then axes and the ReLU curve
        self.wait(2)

        # Animation sequence - all self.play calls at the end
        self.play(Write(title))
        self.play(FadeIn(axes))
        self.play(Create(relu_graph))
# To render this animation, run:
# manim -pql relu_animation.py ReLUAnimation
# This will render in low quality for faster preview

# For high quality:
# manim -pqh relu_animation.py ReLUAnimation