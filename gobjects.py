
class DetectedObjects:

    def __init__(self):
        self.name = None
        self.score = None
        self.positions = []
        self.image_size = None

    def set_image_size(self, size):
        self.image_size = size
        return self

    def set_name(self, name):
        self.name = name
        return self

    def set_score(self, score):
        self.score = score;
        return self

    def add_position(self, position):
        self.positions.append(position)

    def get_fixed_positions(self):
        modified = []

        for pos in self.positions:
            modified.append([self.image_size[0] * pos[0], self.image_size[1] * pos[1]])

        return modified
