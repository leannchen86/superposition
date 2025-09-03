from manim import (
    Scene,
    Rectangle,
    Circle,
    Dot,
    Line,
    rgb_to_color,
    PI,
    WHITE,
    Create,
    FadeIn,
    FadeOut,
    Write,
    Tex,
)
import numpy as np

class NeuralStrawPacking(Scene):
    def construct(self):
        
        # Create the box for straws (left side)
        straw_box = Rectangle(width=4, height=3, color=WHITE, stroke_width=2).move_to([-3.2, 0, 0])
        box_label = Tex(r"Space", font_size=28, color=WHITE).move_to([-3.2, 2.2, 0])
        
        # Create the feature space circle (right side)
        feature_circle = Circle(radius=1.5, color=WHITE, stroke_width=2).move_to([3.2, 0, 0])
        feature_center = Dot(point=[3.2, 0, 0], color=WHITE, radius=0.05)
        angle_label = Tex(r"Direction", font_size=28, color=WHITE).move_to([3.2, 2.2, 0])
        
        # Initialize tracking variables
        straws = []
        features = []
        feature_labels = []
        num_straws = 12
        
        # Show containers and labels
        self.play(
            Create(straw_box),
            Create(feature_circle),
            FadeIn(feature_center),
            Write(box_label),
            Write(angle_label),
            run_time=1.0
        )
        self.wait(0.8)

        # Auto-pack straws with optimal angular distribution
        for i in range(num_straws):
            # Calculate optimal angle for this straw
            angle = (i * PI) / num_straws
            
            # Create straw in the box
            straw_length = 1.5
            straw_center = np.array([-3.2, 0, 0]) + np.array([
                (np.random.random() - 0.5) * 2,  # Random x offset
                (np.random.random() - 0.5) * 1,  # Random y offset
                0
            ])
            
            # Create straw as a line
            straw_start = straw_center + 0.5 * straw_length * np.array([np.cos(angle), np.sin(angle), 0])
            straw_end = straw_center - 0.5 * straw_length * np.array([np.cos(angle), np.sin(angle), 0])
            
            # Color gradient for visual appeal
            hue = i / num_straws
            straw_color = rgb_to_color([
                0.5 + 0.5 * np.sin(2 * PI * hue),
                0.5 + 0.5 * np.sin(2 * PI * hue + 2 * PI / 3),
                0.5 + 0.5 * np.sin(2 * PI * hue + 4 * PI / 3)
            ])
            straw = Line(straw_start, straw_end, color=straw_color, stroke_width=6)
            straws.append(straw)
            
            # Create corresponding feature in neural network space
            feature_end = np.array([3.2, 0, 0]) + 1.4 * np.array([np.cos(angle), np.sin(angle), 0])
            feature_line = Line([3.2, 0, 0], feature_end, color=straw_color, stroke_width=4)
            features.append(feature_line)

            # Feature label
            label_pos = np.array([3.2, 0, 0]) + 1.7 * np.array([np.cos(angle), np.sin(angle), 0])
            feature_label_obj = Tex(r"F" + f"{i+1}", font_size=20, color=straw_color).move_to(label_pos)
            feature_labels.append(feature_label_obj)

        # Animation sequence - all self.play calls at the end
        for i in range(num_straws):
            # Animate adding both straw and feature simultaneously
            self.play(
                Create(straws[i]),
                Create(features[i]),
                Write(feature_labels[i]),
                run_time=0.5
            )
        
        self.wait(4.5)
        
        # Fade out everything at the same time
        self.play(
            FadeOut(straw_box),
            FadeOut(feature_circle),
            FadeOut(feature_center),
            FadeOut(box_label),
            FadeOut(angle_label),
            *[FadeOut(straw) for straw in straws],
            *[FadeOut(feature) for feature in features],
            *[FadeOut(label) for label in feature_labels],
            run_time=1
        )