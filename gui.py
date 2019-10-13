from core import *

def update_information(window):
    if transformed_grid.prev_vector:
        if transformed_grid.prev_vector[1] < len(transformed_grid.vectors):
            window.Vector_x.setText(
                str(round(transformed_grid.vectors[transformed_grid.prev_vector[1]].transformed[0], 3)))
            window.Vector_y.setText(
                str(round(transformed_grid.vectors[transformed_grid.prev_vector[1]].transformed[1], 3)))
            window.Vector_x_rel.setText(
                str(round(transformed_grid.vectors[transformed_grid.prev_vector[1]].coords[0], 3)))
            window.Vector_y_rel.setText(
                str(round(transformed_grid.vectors[transformed_grid.prev_vector[1]].coords[1], 3)))


def update_information_constantly(window):
    window.current_cords00.setText(str(round(transformed_grid.basis_vectors[0].transformed[0], 3)))
    window.current_cords10.setText(str(round(transformed_grid.basis_vectors[0].transformed[1], 3)))
    window.current_cords01.setText(str(round(transformed_grid.basis_vectors[1].transformed[0], 3)))
    window.current_cords11.setText(str(round(transformed_grid.basis_vectors[1].transformed[1], 3)))
    window.determinant.setText(str(round(np.linalg.det(transformed_grid.get_matrix()), 3)))
    window.Green.setText('Green( - ; - )')
    window.Blue.setText('Blue( - ; - )')
    window.Orange.setText('Orange( - ; - )')
    window.Yellow.setText('Yellow( - ; - )')
    window.Purple.setText('Purple( - ; - ))')
    for v in transformed_grid.vectors:
        if v.color == COLORS['green']:
            window.Green.setText(window.Green.text().replace('-','{}').format(*[round(i, 3) for i in v.coords]))
        elif v.color == COLORS['blue']:
            window.Blue.setText(window.Blue.text().replace('-','{}').format(*[round(i, 3) for i in v.coords]))
        elif v.color == COLORS['orange']:
            window.Orange.setText(window.Orange.text().replace('-','{}').format(*[round(i, 3) for i in v.coords]))
        elif v.color == COLORS['yellow']:
            window.Yellow.setText(window.Yellow.text().replace('-','{}').format(*[round(i, 3) for i in v.coords]))
        elif v.color == COLORS['purple']:
            window.Purple.setText(window.Purple.text().replace('-','{}').format(*[round(i, 3) for i in v.coords]))
    window.rotated_function.setText(transformed_grid.transformed_function)

# decorator for checking exceptions in METHODS IN PYQT WINDOWS
def checking_exceptions(method):
    def wrapped(self):
        try:
            self.ErrorLog.setText('')
            return method(self)
        except TooManyVectors as err:
            self.ErrorLog.setText('Too many vectors')
        except Exception as err:
            self.ErrorLog.setText('Error')
            print(err)

    return wrapped


# decorator for METHODS IN PYQT WINDOWS
def check_is_vector_grabbed(method):
    def wrapped(self):
        try:
            self.ErrorLog.setText('')
            return method(self)
        except Exception as err:
            self.ErrorLog.setText('Vector not found. Choose vector.')
    return wrapped


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # load pattern
        self.ui = uic.loadUi('main_window.ui', self)

        # apply linear transformation
        self.ApplyButton.clicked.connect(self.apply)

        self.matrix00.returnPressed.connect(self.change_focus)
        self.matrix01.returnPressed.connect(self.change_focus)
        self.matrix10.returnPressed.connect(self.change_focus)
        self.matrix11.returnPressed.connect(self.apply)

        # unapply transformation
        self.ResetButton.clicked.connect(self.reset)

        # adding and changing vector using coords of grid
        self.AddVector.clicked.connect(self.add_vector)
        self.Vector_x.returnPressed.connect(self.change_focus)
        self.Vector_y.returnPressed.connect(self.add_vector)
        self.ChangeVectorRealCords.clicked.connect(self.change_vector_real_cords)

        # adding and changing vector using basis vector
        self.AddVector_rel.clicked.connect(self.add_vector_rel)
        self.Vector_x_rel.returnPressed.connect(self.change_focus)
        self.Vector_y_rel.returnPressed.connect(self.add_vector_rel)
        self.ChangeVectorRelativeCords.clicked.connect(self.change_vector_relative_cords)

        # deleting vectors
        self.green_btn.clicked.connect(self.delete_vector)
        self.blue_btn.clicked.connect(self.delete_vector)
        self.orange_btn.clicked.connect(self.delete_vector)
        self.yellow_btn.clicked.connect(self.delete_vector)
        self.purple_btn.clicked.connect(self.delete_vector)

        self.change_focus_map = {self.matrix00: self.matrix01,
                                 self.matrix01: self.matrix10,
                                 self.matrix10: self.matrix11,
                                 self.Vector_x: self.Vector_y,
                                 self.Vector_x_rel: self.Vector_y_rel}

        # function
        self.draw_btn.clicked.connect(self.draw_function)
        self.rotate_btn.clicked.connect(self.rotate)

    def change_focus(self):
        s = self.sender()
        self.change_focus_map[s].setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            transformed_grid.delete_vector()
        elif event.key() == Qt.Key_R:
            self.reset()
        elif event.key() == Qt.Key_A:
            self.add_vector()
        elif event.key() == Qt.Key_C:
            self.change_vector_real_cords()

    @checking_exceptions
    def rotate(self):
        a = float(self.angle.text()) * np.pi / 180
        # coordinates of rotated basis vectors
        rotate_matrix = transformed_grid.get_matrix().dot(np.array([[cos(a), -sin(a)],[sin(a), cos(a)]]))
        transformed_grid.basis_vectors[0].transform(rotate_matrix)
        transformed_grid.basis_vectors[1].transform(rotate_matrix)
        transformed_grid.transform()
        update_information(self)

    # add dots to plane and init
    @checking_exceptions
    def draw_function(self):
        transformed_grid.function = self.function.text()
        transformed_grid.transformed_function = 'y = ' + self.function.text()
        transformed_grid.init_function()
        self.rotated_function.setText('y = ' + transformed_grid.function)

    # x-button
    @checking_exceptions
    def delete_vector(self):
        color = self.sender().objectName().split('_')[0]
        for num, v in enumerate(transformed_grid.vectors):
            if v.color == COLORS[color]:
                transformed_grid.available_colors.append(COLORS[color])
                del transformed_grid.vectors[num]
                transformed_grid.prev_vector = None
                break



    # get matrix and apply transformation
    @checking_exceptions
    def apply(self):
        matrix = np.array([[float(self.matrix00.text().replace(',', '.')), float(self.matrix01.text().replace(',', '.'))],
                           [float(self.matrix10.text().replace(',', '.')), float(self.matrix11.text().replace(',', '.'))]])
        M = matrix.dot(transformed_grid.get_matrix())
        for i in range(2):
            transformed_grid.basis_vectors[i].transform(M)
        transformed_grid.transform()
        update_information(self)

    # use grid coords
    @checking_exceptions
    def add_vector(self):
        coords = [float(self.Vector_x.text()), float(self.Vector_y.text())]
        transformed_grid.add_vector(coords)
        transformed_grid.transform()
        transformed_grid.prev_vector = ('common', -1)
        update_information(self)

    # use basis vectors
    @checking_exceptions
    def add_vector_rel(self):
        coords = [float(self.Vector_x_rel.text()), float(self.Vector_y_rel.text())]
        transformed_grid.add_vector_rel(coords)
        transformed_grid.transform()
        update_information(self)

    # use grid coords
    @check_is_vector_grabbed
    def change_vector_real_cords(self):
        coords = [float(self.Vector_x.text()), float(self.Vector_y.text())]
        transformed_grid.vectors[transformed_grid.prev_vector[1]].transformed = coords
        transformed_grid.vectors[transformed_grid.prev_vector[1]].coords = np.linalg.inv(
            transformed_grid.get_matrix()).dot(
            transformed_grid.vectors[transformed_grid.prev_vector[1]].transformed)
        update_information(self)

    # use basis vectors
    @check_is_vector_grabbed
    def change_vector_relative_cords(self):
        coords = [float(self.Vector_x_rel.text()), float(self.Vector_y_rel.text())]
        transformed_grid.vectors[transformed_grid.prev_vector[1]].coords = coords
        transformed_grid.transform()
        update_information(self)

    # unapply all transformations
    @checking_exceptions
    def reset(self):
        # identity matrix
        matrix = np.array([[1, 0], [0, 1]])
        for i in range(2):
            transformed_grid.basis_vectors[i].transform(matrix)
        transformed_grid.transform()
        update_information(self)
