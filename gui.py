from core import *


def update_information(window):
    window.matrix00.setText(str(round(transformed_grid.basis_vectors[0].transformed[0], 3)))
    window.matrix10.setText(str(round(transformed_grid.basis_vectors[0].transformed[1], 3)))
    window.matrix01.setText(str(round(transformed_grid.basis_vectors[1].transformed[0], 3)))
    window.matrix11.setText(str(round(transformed_grid.basis_vectors[1].transformed[1], 3)))
    if transformed_grid.prev_vector:
        if transformed_grid.prev_vector[1] < len(transformed_grid.vectors):
            window.Vector_x.setText(str(round(transformed_grid.vectors[transformed_grid.prev_vector[1]].transformed[0], 3)))
            window.Vector_y.setText(str(round(transformed_grid.vectors[transformed_grid.prev_vector[1]].transformed[1], 3)))
            window.Vector_x_rel.setText(str(round(transformed_grid.vectors[transformed_grid.prev_vector[1]].cords[0], 3)))
            window.Vector_y_rel.setText(str(round(transformed_grid.vectors[transformed_grid.prev_vector[1]].cords[1], 3)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main_window.ui', self)
        self.ApplyButton.clicked.connect(self.apply)
        self.ResetButton.clicked.connect(self.reset)
        self.AddVector.clicked.connect(self.add_vector)
        self.ChangeVectorRealCords.clicked.connect(self.change_vector_real_cords)

        self.AddVector_rel.clicked.connect(self.add_vector_rel)
        self.ChangeVectorRelativeCords.clicked.connect(self.change_vector_relative_cords)

    def apply(self):
        try:
            matrix = np.array([[float(self.matrix00.text()), float(self.matrix01.text())],
                               [float(self.matrix10.text()), float(self.matrix11.text())]])
            for i in range(2):
                transformed_grid.basis_vectors[i].transform(matrix)
            transformed_grid.transform()
            update_information(self)
            self.ErrorLog.setText('')
        except Exception as err:
            self.ErrorLog.setText('Error')

    def add_vector(self):
        try:
            cords = [float(self.Vector_x.text()), float(self.Vector_y.text())]
            transformed_grid.add_vector(cords)
            transformed_grid.transform()
            transformed_grid.prev_vector = ('common', -1)
            update_information(self)
        except TooManyVectors as err:
            self.ErrorLog.setText('Too many vectors')
        except Exception as err:
            self.ErrorLog.setText('Error')

    def add_vector_rel(self):
        try:
            cords = [float(self.Vector_x_rel.text()), float(self.Vector_y_rel.text())]
            transformed_grid.add_vector_rel(cords)
            transformed_grid.transform()
            update_information(self)
        except TooManyVectors as err:
            self.ErrorLog.setText('Too many vectors')
        except Exception as err:
            self.ErrorLog.setText('Error')

    def change_vector_real_cords(self):
        try:
            cords = [float(self.Vector_x.text()), float(self.Vector_y.text())]
            transformed_grid.vectors[transformed_grid.prev_vector[1]].transformed = cords
            transformed_grid.vectors[transformed_grid.prev_vector[1]].cords = np.linalg.inv(transformed_grid.get_matrix()).dot(
                transformed_grid.vectors[transformed_grid.prev_vector[1]].transformed)
            update_information(self)
        except Exception as err:
            self.ErrorLog.setText('Vector not found. Choose vector.')

    def change_vector_relative_cords(self):
        try:
            cords = [float(self.Vector_x_rel.text()), float(self.Vector_y_rel.text())]
            transformed_grid.vectors[transformed_grid.prev_vector[1]].cords = cords
            transformed_grid.transform()
            update_information(self)
        except Exception as err:
            self.ErrorLog.setText('Vector not found. Choose vector.')
    def reset(self):
        try:
            matrix = np.array([[1, 0], [0, 1]])
            for i in range(2):
                transformed_grid.basis_vectors[i].transform(matrix)
            transformed_grid.transform()
            self.ErrorLog.setText('')
            update_information(self)
        except Exception as err:
            self.ErrorLog.setText('Error')
            raise err
