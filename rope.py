import pygame

ROPE_COLOR = (139, 69, 19)  # brown rope

class Rope:
    
    def __init__(self, start_pos, end_pos, num_segments):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.num_segments = num_segments
        self.segment_length = (end_pos[0] - start_pos[0]) / num_segments
        self.points = self.generate_points()

    def generate_points(self):
        points = []
        for i in range(self.num_segments + 1):
            x = self.start_pos[0] + i * self.segment_length
            y = self.start_pos[1]
            points.append((x, y))
        return points
    
    def draw(self, win):
        for i in range(len(self.points) - 1):
            pygame.draw.line(win, ROPE_COLOR, self.points[i], self.points[i + 1], 5)
