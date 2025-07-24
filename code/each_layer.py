from manim import *

class NeuralNetworkAnimation(ThreeDScene):
    def construct(self):
        # Scene 1: Neural Network Overview
        title = Text("Neural Network: Layers and Dimensionality").to_edge(UP)
        self.play(Write(title))

        # Create layers (input, hidden, output layers)
        input_layer = VGroup(*[Dot() for _ in range(5)]).arrange(DOWN, buff=0.3).shift(LEFT * 4)
        hidden_layer = VGroup(*[Dot() for _ in range(8)]).arrange(DOWN, buff=0.2)
        hidden2_layer = VGroup(*[Dot() for _ in range(10)]).arrange(DOWN, buff=0.15).shift(RIGHT * 2)
        output_layer = VGroup(*[Dot() for _ in range(3)]).arrange(DOWN, buff=0.4).shift(RIGHT * 4)

        # Labels for layers
        input_label = Text("Input\nLayer", font_size=24).next_to(input_layer, LEFT)
        hidden_label = Text("Hidden Layer\n768 Neurons", font_size=24).next_to(hidden_layer, UP)
        hidden2_label = Text("Hidden Layer\n2048 Neurons", font_size=24).next_to(hidden2_layer, UP)
        output_label = Text("Output\n256 Neurons", font_size=24).next_to(output_layer, RIGHT)

        # Draw connections between layers
        connections1 = VGroup(*[Line(input_layer[i].get_center(), hidden_layer[j].get_center(), stroke_width=0.5)
                                for i in range(5) for j in range(8)])
        connections2 = VGroup(*[Line(hidden_layer[i].get_center(), hidden2_layer[j].get_center(), stroke_width=0.5)
                                for i in range(8) for j in range(10)])
        connections3 = VGroup(*[Line(hidden2_layer[i].get_center(), output_layer[j].get_center(), stroke_width=0.5)
                                for i in range(10) for j in range(3)])

        # Animate network creation
        self.play(Create(input_layer), Write(input_label))
        self.play(Create(hidden_layer), Write(hidden_label))
        self.play(Create(connections1))
        self.play(Create(hidden2_layer), Write(hidden2_label))
        self.play(Create(connections2))
        self.play(Create(output_layer), Write(output_label))
        self.play(Create(connections3))
        self.wait(1)

        # Scene 2: Zoom into Hidden Layer (High-Dimensional Space)
        high_dim_text = Text("768-Dimensional Space", font_size=36).to_edge(UP)
        self.play(FadeOut(title), FadeIn(high_dim_text))
        self.play(FocusOn(hidden_layer), hidden_layer.animate.scale(1.5))

        # Transition to 3D to suggest high dimensionality
        axes = ThreeDAxes(x_range=[-2, 2], y_range=[-2, 2], z_range=[-2, 2], x_length=4, y_length=4, z_length=4)
        axes.move_to(hidden_layer)
        self.play(Create(axes))
        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, run_time=2)
        dim_label = Text("Each neuron = 1 dimension", font_size=24).next_to(axes, DOWN)
        self.play(Write(dim_label))
        self.wait(1)
        self.play(FadeOut(axes, dim_label), hidden_layer.animate.scale(1/1.5))
        # Return the camera to its original orientation
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES, run_time=2)
        self.wait(1)

        # Scene 3: Data Flow ("cat" Embedding)
        cat_text = Text("“cat”", font_size=36).next_to(input_layer, LEFT)
        embedding = Matrix([[0.1], [0.3], ["..."], [0.7]], v_buff=0.3).next_to(cat_text, RIGHT).scale(0.6)
        embed_label = Text("768-D Vector", font_size=24).next_to(embedding, DOWN)
        self.play(FadeOut(high_dim_text), Write(cat_text), Create(embedding), Write(embed_label))
        self.play(embedding.animate.move_to(hidden_layer), embed_label.animate.next_to(hidden_layer, DOWN))
        self.wait(1)

        # Scene 4: Dimensionality Transformations
        # Transformation to 2048 dimensions
        matrix1 = Matrix([[1, 0, "...", 0], [0, 1, "...", 0], ["...", "...", "...", "..."], [0, 0, "...", 1]],
                         h_buff=0.8, v_buff=0.8).scale(0.5).move_to(LEFT * 1)
        matrix_label1 = Text("Matrix\n(768 → 2048)", font_size=24).next_to(matrix1, DOWN)
        new_embedding = Matrix([[0.2], [0.5], ["..."], [0.9]], v_buff=0.3).scale(0.6).move_to(hidden2_layer)
        new_embed_label = Text("2048-D Vector", font_size=24).next_to(new_embedding, DOWN)
        expand_text = Text("Expands to capture\ncomplex relationships", font_size=24).to_edge(UP)

        self.play(Write(matrix1), Write(matrix_label1), FadeIn(expand_text))
        self.play(Transform(embedding, new_embedding), Transform(embed_label, new_embed_label))
        self.play(FadeOut(matrix1, matrix_label1))
        self.wait(1)

        # Transformation to 256 dimensions
        matrix2 = Matrix([[1, 0, "...", 0], [0, 1, "...", 0], ["...", "...", "...", "..."], [0, 0, "...", 1]],
                         h_buff=0.8, v_buff=0.8).scale(0.5).move_to(RIGHT * 1)
        matrix_label2 = Text("Matrix\n(2048 → 256)", font_size=24).next_to(matrix2, DOWN)
        final_embedding = Matrix([[0.4], ["..."], [0.6]], v_buff=0.3).scale(0.6).move_to(output_layer)
        final_embed_label = Text("256-D Vector", font_size=24).next_to(final_embedding, DOWN)
        compress_text = Text("Compresses to refine\nunderstanding", font_size=24).to_edge(UP)

        self.play(Write(matrix2), Write(matrix_label2), Transform(expand_text, compress_text))
        self.play(Transform(embedding, final_embedding), Transform(embed_label, final_embed_label))
        self.play(FadeOut(matrix2, matrix_label2))
        self.wait(1)

        # Scene 5: Final Highlight
        final_text = Text("Model refines understanding\nthrough transformations", font_size=36).to_edge(UP)
        self.play(Transform(expand_text, final_text))
        self.wait(2)

        # Fade out all mobjects gracefully
        self.play(FadeOut(Group(*self.mobjects)))
        self.wait(1)