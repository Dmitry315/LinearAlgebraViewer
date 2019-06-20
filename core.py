from config import *


# connect some vertexes
def connect_all(self, window, vertexes, color, weight):
    pygame.draw.line(window, color, self.coords, [i.real_cords() for i in vertexes], weight)


# calculate distance between two points
def distance(pos1, pos2):
    return np.sqrt(np.power(pos1[0] - pos2[0], 2) + np.power(pos1[1] - pos2[1], 2))


# Smallest unit
class Vertex:
    def __init__(self, coords, unit, center):
        # coordinates
        self.coords = coords
        # coords after applying transformation
        self.transformed = coords
        # information to get real coords if vertex
        self.unit = unit
        self.center = center

    # transform grid coords to coords in window
    # don't forget that Oy axis in screen point in down
    # but real Oy axis point in up
    def real_cords(self):
        return [int(self.transformed[0] * self.unit + self.center[0]),
                int(-self.transformed[1] * self.unit + self.center[1])]

    # apply linear transformation to vertex
    def transform(self, matrix):
        cord = np.array(self.coords)
        new = matrix.dot(cord)
        self.transformed = [new[0], new[1]]

    # draw line between two vertexes
    def connect(self, window, another_vertex, color, weight=1):
        pygame.draw.line(window, color, self.real_cords(), another_vertex.real_cords(), weight)


# Vector's start point in the middle of the grid,
# so we can imagine it as vertex that determine end of vector
class Vector(Vertex):
    def __init__(self, coords, unit, central_vertex, color):
        super().__init__(coords, unit, central_vertex.real_cords())
        self.color = color
        # start of vector
        self.central_vertex = central_vertex

    # line between central vertex and end
    def draw(self, window):
        self.connect(window, self.central_vertex, self.color, 2)
        pygame.draw.circle(window, self.color, self.real_cords(), 3)

    # using mouse to drag
    # don't forget that Oy axis in screen point in down
    # but real Oy axis point in up
    def change_cords(self, real):
        self.transformed = [(real[0] - self.center[0]) / self.unit, - (real[1] - self.center[1]) / self.unit]


class BasisVector(Vector):
    def __init__(self, coords, unit, center, color):
        super().__init__(coords, unit, center, color)


# grid that stay after transforming plane
class BackGrid:
    def __init__(self, center, side, cell_size, color):
        self.x = center[0]
        self.y = center[1]
        # size of grid
        self.side = (side // 2) * 2 + 1
        self.cell_size = cell_size
        self.color = color
        # vertexes that determine plane
        self.top_vertexes = [Vertex((i, side // 2), cell_size, center) for i in range(- side // 2, side // 2 + 1)]
        self.bot_vertexes = [Vertex((i, - side // 2), cell_size, center) for i in range(- side // 2, side // 2 + 1)]
        self.left_vertexes = [Vertex((- side // 2, i), cell_size, center) for i in range(- side // 2, side // 2 + 1)]
        self.right_vertexes = [Vertex((side // 2, i), cell_size, center) for i in range(- side // 2, side // 2 + 1)]

    # connect vertexes: top with bot and left with right
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


# If more than 5 custom vectors
class TooManyVectors(Exception):
    pass


# grid that show us transformed plane
class Grid(BackGrid):
    def __init__(self, center, side, cell_size, color):
        super().__init__(center, side, cell_size, color)
        self.central_vertex = Vertex((0, 0), cell_size, center)
        # Basis vectors determine all vertexes in plane.
        # Changing basis vectors coordinates we apply
        # linear transformation to all points in plane:
        #    [ i.x j.x ]
        # M =[ i.y j.y ] , where i, j - basis vectors and x, y - their coordinates
        self.basis_vectors = [BasisVector((1, 0), self.cell_size, self.central_vertex, DARK_BLUE),
                              BasisVector((0, 1), self.cell_size, self.central_vertex, RED)]
        # common vectors, we can drag them by mouse
        self.vectors = []
        self.available_colors = [(145, 38, 191), (242, 183, 5), (217, 61, 4), (57, 140, 191), (128, 191, 132)]
        # buffer for previous vector, for changing it's coords via tab
        self.prev_vector = None

    # draw grid, center and all vectors
    def draw_object(self, window, weight=1):
        super().draw_object(window, weight)
        self.basis_vectors[0].draw(window)
        self.basis_vectors[1].draw(window)
        for vector in self.vectors:
            vector.draw(window)
        pygame.draw.circle(window, BLACK, (self.x, self.y), 3)

    # add vector by changing transformed coords
    def add_vector(self, coords):
        if not self.available_colors:
            raise TooManyVectors()
        untransformed_cords = np.linalg.inv(self.get_matrix()).dot(coords)
        self.vectors.append(
            Vector(untransformed_cords, self.cell_size, self.central_vertex, self.available_colors.pop(-1)))

    # add vector(v) by coordinates using basis vectors i and j, where
    # v = ai, bj, where (a, b) - coords 
    def add_vector_rel(self, coords):
        if not self.available_colors:
            raise TooManyVectors()
        self.vectors.append(Vector(coords, self.cell_size, self.central_vertex, self.available_colors.pop(-1)))

    # apply linear transformation to all vertexes and vectors
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

    # return what vector we grabbed by mouse
    def check_grabbing(self, mouse_cords):
        for i in range(2):
            if distance(mouse_cords, self.basis_vectors[i].real_cords()) < 3:
                return ('basis', i)
        for i in range(len(self.vectors)):
            if distance(mouse_cords, self.vectors[i].real_cords()) < 3:
                return ('common', i)
        return None

    # get matrix of linear transformation, using basis vectors
    def get_matrix(self):
        return np.array([list(self.basis_vectors[0].transformed), list(self.basis_vectors[1].transformed)]).T


# init grids
main_grid = BackGrid((width // 2, height // 2), 20, 60, GREY)
transformed_grid = Grid((width // 2, height // 2), 20, 60, BLUE)
