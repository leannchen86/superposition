from manim import *
import math

# Set Consolas as the default for all Text and DecimalNumber mobjects
Text.set_default(font="Consolas")
DecimalNumber.set_default(font="Consolas")

class UpdatersExampleCE(Scene):
    def construct(self):
        square = Square().set_fill(BLUE_E, 1)
        # Brace always redraws itself around the square
        brace = always_redraw(lambda: Brace(square, UP))
        # Now Text and DecimalNumber will both be in Consolas
        text   = Text("Width = ")
        number = DecimalNumber(0, num_decimal_places=2, include_sign=True)
        label  = VGroup(text, number).arrange(RIGHT)
        label.add_updater(lambda m: m.next_to(brace, UP))
        number.add_updater(lambda m: m.set_value(square.width))
        self.add(square, brace, label)
        self.wait()
        self.wait()
        self.wait()
        phase = ValueTracker(0)
        square.add_updater(
            lambda m, dt: (
                phase.increment_value(dt),
                m.set_width(2 * math.cos(phase.get_value()) + 2)
            )
        )

        # Animation sequence - all self.play calls at the end
        self.play(square.animate.scale(2),
                  rate_func=there_and_back, run_time=2)
        self.play(square.animate.set_width(5, stretch=True), run_time=3)
        self.play(square.animate.set_width(2), run_time=3)
        self.wait(4 * math.pi)
        square = Square().set_fill(BLUE_E, 1)

        # Brace always redraws itself around the square
        brace = always_redraw(lambda: Brace(square, UP))

        # Now Text and DecimalNumber will both be in Consolas
        text   = Text("Width = ")
        number = DecimalNumber(0, num_decimal_places=2, include_sign=True)
        label  = VGroup(text, number).arrange(RIGHT)

        label.add_updater(lambda m: m.next_to(brace, UP))
        number.add_updater(lambda m: m.set_value(square.width))

        self.add(square, brace, label)

        self.play(square.animate.scale(2),
                  rate_func=there_and_back, run_time=2)
        self.wait()
        self.play(square.animate.set_width(5, stretch=True), run_time=3)
        self.wait()
        self.play(square.animate.set_width(2), run_time=3)
        self.wait()

        phase = ValueTracker(0)
        square.add_updater(
            lambda m, dt: (
                phase.increment_value(dt),
                m.set_width(2 * math.cos(phase.get_value()) + 2)
            )
        )
        self.wait(4 * math.pi)
