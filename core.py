from config import *


def connect_all(self, window, vertexes, color, weight):
    pygame.draw.line(window, color, self.cords, [i.real_cords() for i in vertexes], weight)


def distance(pos1, pos2):
    return np.sqrt(np.power(pos1[0] - pos2[0], 2) + np.power(pos1[1] - pos2[1], 2))


class Vertex:
    def __init__(self, cords, unit, center):
        self.cords = cords
        self.unit = unit
        self.center = center
        self.transformed = cords

    def real_cords(self):
        return [int(self.transformed[0] * self.unit + self.center[0]),
                int(-self.transformed[1] * self.unit + self.center[1])]

    def transform(self, matrix):
        cord = np.array(self.cords)
        new = matrix.dot(cord)
        self.transformed = [new[0], new[1]]

    def connect(self, window, another_vertex, color, weight=1):
        pygame.draw.line(window, color, self.real_cords(), another_vertex.real_cords(), weight)


class Vector(Vertex):
    def __init__(self, cords, unit, central_vertex, color):
        super().__init__(cords, unit, central_vertex.real_cords())
        self.color = color
        self.central_vertex = central_vertex

    def draw(self, window):
        self.connect(window, self.central_vertex, self.color, 2)
        pygame.draw.circle(window, self.color, self.real_cords(), 3)

    def change_cords(self, real):
        self.transformed = [(real[0] - self.center[0]) / self.unit, - (real[1] - self.center[1]) / self.unit]


class BasisVector(Vector):
    def __init__(self, cords, unit, center, color):
        super().__init__(cords, unit, center, color)


class BackGrid:
    def __init__(self, center, side, cell_size, color):
        self.x = center[0]
        self.y = center[1]
        self.side = (side // 2) * 2 + 1
        self.cell_size = cell_size
        self.color = color
        self.top_vertexes = [Vertex((i, side // 2), cell_size, center) for i in range(- side // 2, side // 2 + 1)]
        self.bot_vertexes = [Vertex((i, - side // 2), cell_size, center) for i in range(- side // 2, side // 2 + 1)]
        self.left_vertexes = [Vertex((- side // 2, i), cell_size, center) for i in range(- side // 2, side // 2 + 1)]
        self.right_vertexes = [Vertex((side // 2, i), cell_size, center) for i in range(- side // 2, side // 2 + 1)]

    def draw_object(self, window, weight=1):
        for i in range(self.side):
            if i == self.side // 2 and self.__class__ == Grid:
                self.top_vertexes[i].connect(window, self.bot_vertexes[i], BLACK, weight)
            else:
                self.top_vertexes[i].connect(window, self.bot_vertexes[i], self.color, weight)
        for i in range(self.side):
            if i == self.side // 2 and self.__class__ == Grid:
                self.left_vertexes[i].connect(window, self.right_vertexes[i], BLACK, weight)
            else:
                self.left_vertexes[i].connect(window, self.right_vertexes[i], self.color, weight)


class TooManyVectors(Exception):
    pass


class Grid(BackGrid):
    def __init__(self, center, side, cell_size, color):
        super().__init__(center, side, cell_size, color)
        self.central_vertex = Vertex((0, 0), cell_size, center)
        self.basis_vectors = [BasisVector((1, 0), self.cell_size, self.central_vertex, DARK_BLUE),
                              BasisVector((0, 1), self.cell_size, self.central_vertex, RED)]
        self.vectors = []
        self.available_colors = [(145, 38, 191), (242, 183, 5), (217, 61, 4), (57, 140, 191), (128, 191, 132)]

    def draw_object(self, window, weight=1):
        super().draw_object(window, weight)
        self.basis_vectors[0].draw(window)
        self.basis_vectors[1].draw(window)
        for vector in self.vectors:
            vector.draw(window)
        pygame.draw.circle(window, BLACK, (self.x, self.y), 3)

    def add_vector(self, cords):
        if not self.available_colors:
            raise TooManyVectors()
        self.vectors.append(Vector(cords, self.cell_size, self.central_vertex, self.available_colors.pop(-1)))

    def transform(self):
        matrix = self.get_matrix()
        length = range(len(self.top_vertexes))
        for i in length:
            self.top_vertexes[i].transform(matrix)
        for i in length:
            self.bot_vertexes[i].transform(matrix)
        for i in length:
            self.left_vertexes[i].transform(matrix)
        for i in length:
            self.right_vertexes[i].transform(matrix)
        for i in range(len(self.vectors)):
            self.vectors[i].transform(matrix)

    def check_grabbing(self, mouse_cords):
        for i in range(2):
            if distance(mouse_cords, self.basis_vectors[i].real_cords()) < 3:
                return ('basis', i)
        for i in range(len(self.vectors)):
            if distance(mouse_cords, self.vectors[i].real_cords()) < 3:
                return ('common', i)
        return None

    def get_matrix(self):
        return np.array([list(self.basis_vectors[0].transformed), list(self.basis_vectors[1].transformed)]).T


main_grid = BackGrid((width // 2, height // 2), 20, 60, GREY)
transformed_grid = Grid((width // 2, height // 2), 20, 60, BLUE)
