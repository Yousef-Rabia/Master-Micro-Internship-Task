from function_plotter import*
import sys
from PySide2.QtWidgets import QApplication


if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    window = PlotterWindow()
    window.show()
    sys.exit(app.exec_())