from manim import *
import numpy as np

class NeuralStrawPacking(Scene):
    def construct(self):
        
        # Create the box for straws (left side)
        straw_box = Rectangle(width=4, height=3, color=WHITE, stroke_width=2).move_to([-4, 0, 0])
        straw_box_label = Text("Fixed Space\n(Neural Layer)", font_size=16, color=GRAY).next_to(straw_box, DOWN, buff=0.3)
        
        # Create the feature space circle (right side)
        feature_circle = Circle(radius=1.5, color=WHITE, stroke_width=2).move_to([4, 0, 0])
        feature_center = Dot(point=[4, 0, 0], color=WHITE, radius=0.05)
        feature_label = Text("Feature Space\n(Representational Dimensions)", font_size=16, color=GRAY).next_to(feature_circle, DOWN, buff=0.3)
        
        self.play(
            Create(straw_box), Write(straw_box_label),
            Create(feature_circle), Create(feature_center), Write(feature_label)
        )
        self.wait(1)
        
        # Add titles for left and right sections
        left_title = Text("Straw Packing", font_size=20, color=BLUE).next_to(straw_box, UP, buff=0.3)
        right_title = Text("Feature Mapping", font_size=20, color=BLUE).next_to(feature_circle, UP, buff=0.3)
        
        self.play(Write(left_title), Write(right_title))
        self.wait(0.5)
        
        # Initialize tracking variables
        straws = []
        features = []
        feature_labels = []
        num_straws = 12
        
        # Efficiency counter
        efficiency_text = Text("Efficiency: 0%", font_size=24, color=GREEN).to_edge(DOWN, buff=1)
        explanation = Text("Optimally packing features for maximum diversity", 
                          font_size=20, color=BLUE).to_edge(DOWN, buff=0.3)
        self.play(Write(efficiency_text), Write(explanation))
        
        # Auto-pack straws with optimal angular distribution
        for i in range(num_straws):
            # Calculate optimal angle for this straw
            angle = (i * PI) / num_straws
            
            # Create straw in the box
            straw_length = 1.5
            straw_center = np.array([-4, 0, 0]) + np.array([
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
            feature_end = np.array([4, 0, 0]) + 1.4 * np.array([np.cos(angle), np.sin(angle), 0])
            feature_line = Line([4, 0, 0], feature_end, color=straw_color, stroke_width=4)
            features.append(feature_line)
            
            # Feature label
            label_pos = np.array([4, 0, 0]) + 1.7 * np.array([np.cos(angle), np.sin(angle), 0])
            feature_label = Text(f"F{i+1}", font_size=12, color=straw_color).move_to(label_pos)
            feature_labels.append(feature_label)
            
            # Animate adding both straw and feature simultaneously
            self.play(
                Create(straw),
                Create(feature_line),
                Write(feature_label),
                run_time=0.4
            )
            
            # Update efficiency counter
            efficiency = min(100, ((i + 1) / num_straws) * 85 + 15)  # Scale to look realistic
            new_efficiency_text = Text(f"Efficiency: {efficiency:.0f}%", 
                                     font_size=24, color=GREEN).to_edge(DOWN, buff=1)
            self.play(Transform(efficiency_text, new_efficiency_text), run_time=0.2)
        
        self.wait(2)