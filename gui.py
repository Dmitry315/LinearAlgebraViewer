from core import *


def update_information(window):
    window.matrix00.setText(str(round(transformed_grid.basis_vectors[0].transformed[0], 3)))
    window.matrix10.setText(str(round(transformed_grid.basis_vectors[0].transformed[1], 3)))
    window.matrix01.setText(str(round(transformed_grid.basis_vectors[1].transformed[0], 3)))
    window.matrix11.setText(str(round(transformed_grid.basis_vectors[1].transformed[1], 3)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('main_window.ui', self)
        self.ApplyButton.clicked.connect(self.apply)
        self.ResetButton.clicked.connect(self.reset)
        self.AddVector.clicked.connect(self.add_vector)

    def apply(self):
        try:
            matrix = np.array([[float(self.matrix00.text()), float(self.matrix01.text())],
                               [float(self.matrix10.text()), float(self.matrix11.text())]])
            for i in range(2):
                transformed_grid.basis_vectors[i].transform(matrix)
            transformed_grid.transform()
            self.ErrorLog.setText('')
        except Exception as err:
            self.ErrorLog.setText('Error')

    def add_vector(self):
        try:
            cords = [float(self.Vector_x.text()), float(self.Vector_y.text())]
            transformed_grid.add_vector(cords)
        except TooManyVectors as err:
            self.ErrorLog.setText('Too many vectors')
        except Exception as err:
            self.ErrorLog.setText('Error')
            print(err)

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
