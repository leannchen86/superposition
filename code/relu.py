from manim import *

class ReLUAnimation(Scene):
    def construct(self):
        # Create the coordinate system
        axes = Axes(
            x_range=[-10, 10, 1],
            y_range=[-1, 10, 1],
            axis_config={"color": GREY},
            x_length=10,
            y_length=6,
        )
        # Add numeric labels at every 2 steps on both axes
        axes.add_coordinates(
            range(-10, 12, 2),  # x-axis labels
            range(0, 11, 2),    # y-axis labels
        )

        # Axis labels
        x_label = axes.get_x_axis_label("x")

        # Plot the ReLU function
        relu_graph = axes.plot(
            lambda x: max(0, x),
            x_range=[-10, 10],
            color=BLUE,
        )

        # Add a title to indicate this is a ReLU graph
        title = Tex("ReLU", font_size=48).to_edge(UP)

        # Animate the scene: title first, then axes and the ReLU curve
        self.play(Write(title))
        self.play(FadeIn(axes), FadeIn(x_label))
        self.play(FadeIn(relu_graph))
        self.wait(2)


# To render this animation, run:
# manim -pql relu_animation.py ReLUAnimation
# This will render in low quality for faster preview

# For high quality:
# manim -pqh relu_animation.py ReLUAnimation