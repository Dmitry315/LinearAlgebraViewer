import pygame
import numpy as np
from numpy import sqrt, log, sin, sinh, cos, cosh, tan, tanh, arccos, arcsin, arctan
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QShortcut
from PyQt5 import uic
from PyQt5.QtCore import Qt
import sys

# screen size
size = width, height = 1200, 800
fps = 30
# colors in rgb
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 255)
BLUE = (100, 149, 237)
GREY = (128, 128, 128)
RED = (255, 0, 0)
Epsilon = 10 ** (-10)
COLORS = {'green': (128, 191, 132),
          'blue': (57, 140, 191),
          'orange': (217, 61, 4),
          'yellow': (242, 183, 5),
          'purple': (145, 38, 191)}
