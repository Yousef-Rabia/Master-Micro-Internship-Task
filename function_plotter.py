import sys
from PySide2.QtWidgets import QApplication, QWidget, QLabel, QMessageBox, QGridLayout, QDoubleSpinBox, QVBoxLayout, QHBoxLayout, QLineEdit, QDialog, QGroupBox, QPushButton, QLabel
from PySide2.QtGui import QFont, QColor, QPalette, QIcon
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
import numpy as np
import utilities

myFont = QFont("Sanserif", 13)
ranges = (-10000, 10000)
defRange = (-10, 10)

class PlotterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Function Plotter")
        self.setMinimumSize(700, 500)
        self.setWindowIcon(QIcon("images/mm_logo.jpg"))

        # Color of window
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(40, 84, 166))
        self.setPalette(palette)

        #  create widgets
        self.view = FigureCanvas(Figure(figsize=(20, 20)))
        self.axes = self.view.figure.subplots()

        self.groupBox = QGroupBox("Function Plotter")
        self.groupBox.setFont(QFont("Sanserif", 13))
        self.groupBox.setStyleSheet('color: white;')
        gridLayout = QGridLayout()

        # Min and max values of x
        self.max = QDoubleSpinBox()
        self.min = QDoubleSpinBox()
        self.minLabel = QLabel(text="Min X: ")
        self.maxLabel = QLabel(text="Max X: ")
        self.min.setFont(myFont)
        self.minLabel.setFont(myFont)
        self.max.setFont(myFont)
        self.maxLabel.setFont(myFont)
        self.min.setRange(*ranges)
        self.max.setRange(*ranges)
        self.max.setValue(defRange[1])
        self.min.setValue(defRange[0])
        self.min.setStyleSheet('color: black; font-size: 12pt;')
        self.max.setStyleSheet('color: black; font-size: 12pt;')

        # Buttons
        self.button1 = QPushButton(" Plot", self)
        self.button1.setIcon(QIcon("images/chart.png"))
        self.button1.setStyleSheet('color: black; font-size: 12pt;')
        self.button1.setMinimumHeight(40)

        self.button2 = QPushButton(" Exit", self)
        self.button2.setIcon(QIcon("images/exit.png"))
        self.button2.setStyleSheet('color: black; font-size: 12pt;')
        self.button2.setMinimumHeight(40)

        self.function = QLineEdit()
        self.function.setFont(myFont)
        self.func_label = QLabel(text="F(x): ")
        self.function.setText("x^2")
        self.func_label.setFont(myFont)
        self.function.setStyleSheet('color: black; font-size: 12pt;')

        # Grid layout
        gridLayout.addWidget(self.func_label, 0, 0)
        gridLayout.addWidget(self.function, 0, 1, 1, 3)

        gridLayout.addWidget(self.minLabel, 1, 0)
        gridLayout.addWidget(self.min, 1, 1)
        gridLayout.addWidget(self.maxLabel, 1, 2)
        gridLayout.addWidget(self.max, 1, 3)

        gridLayout.setColumnStretch(0, 0)
        gridLayout.setColumnStretch(1, 2)
        gridLayout.setColumnStretch(2, 0)
        gridLayout.setColumnStretch(3, 2)

        gridLayout.addWidget(self.button1, 3, 0, 1, 2)
        gridLayout.addWidget(self.button2, 3, 2, 1, 2)

        self.groupBox.setLayout(gridLayout)
        vbox = QVBoxLayout()
        vbox.addWidget(self.view)
        vbox.addWidget(self.groupBox)
        self.setLayout(vbox)

        self.error_dialog = QMessageBox()
        self.error_dialog.setFont(myFont)

        # connect inputs with on_change method
        self.button2.clicked.connect(self.confirmExit)
        self.min.valueChanged.connect(lambda _: self.entryChange(1))
        self.max.valueChanged.connect(lambda _: self.entryChange(2))
        self.button1.clicked.connect(lambda _: self.entryChange(3))
        self.entryChange(0)

    def confirmExit(self):
        confirm = QMessageBox.question(self, "Confirm Exit", "Are you sure you want to exit?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            QApplication.quit()

    def entryChange(self, val):  # val is needed to identify what value is changed
        min_val = self.min.value()
        max_val = self.max.value()

        # Warning: min x can't be greater than or equal to max x
        if val == 1 and min_val >= max_val:
            self.min.setValue(max_val - 1)
            self.error_dialog.setText("'Min x' should be less than 'Max x'")
            self.error_dialog.show()
            return

        # Warning: max x can't be less than or equal to min x
        if val == 2 and max_val <= min_val:
            self.max.setValue(min_val + 1)
            self.error_dialog.setText("'Min x' should be less than 'Max x'")
            self.error_dialog.show()
            return


        x = np.linspace(min_val, max_val,500)
        try:
            y = utilities.validate_function(self.function.text())(x)
            print("############################################################################")
            print(x)
            print(y)
        except ValueError as e:
            self.axes.clear()
            self.view.draw()
            self.error_dialog.setWindowTitle("Function Error!")
            self.error_dialog.setText(str(e))
            self.error_dialog.show()
            return
        
        try:
            self.axes.clear()
            self.axes.plot(x, y)

        except ValueError as e:
            self.axes.clear()
            self.view.draw()
            self.error_dialog.setWindowTitle("Function Error!")
            self.error_dialog.setText("Function Error!")
            self.error_dialog.show()
            return

        self.axes.grid(True, linestyle='--', color='gray', alpha=0.9)
        self.axes.set_xlabel("X-axis Label")
        self.axes.set_ylabel("Y-axis Label")    
        self.axes.axvline(x=0, color=(40/255, 84/255, 166/255), linestyle='--')
        self.axes.axhline(y=0, color=(40/255, 84/255, 166/255), linestyle='--')
        self.view.draw()
