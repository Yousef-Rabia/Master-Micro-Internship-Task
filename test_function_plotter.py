import pytest
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest
from PySide2.QtWidgets import QApplication
from function_plotter import PlotterWindow


@pytest.fixture(scope="module")
def app(request):
    qApp = QApplication.instance()
    if qApp is None:
        qApp = QApplication([])
    qApp.setAttribute(Qt.AA_Use96Dpi, True)

    def teardown():
        qApp.quit()

    request.addfinalizer(teardown)
    return qApp


class TestPlotterWindow:
    @pytest.fixture(autouse=True)
    def setup_method(self, app):
        self.window = PlotterWindow()
        self.app = app

    def test_plot_generation(self):
        self.window.function.setText("x^2")
        self.window.min.setValue(-5)
        self.window.max.setValue(5)

        QTest.mouseClick(self.window.button1, Qt.LeftButton)

        assert self.window.axes.lines

    def test_min_max_validation(self):
        self.window.min.setValue(30)
        self.window.max.setValue(20)

        QTest.mouseClick(self.window.button1, Qt.LeftButton)

        error_text = self.window.error_dialog.text().lower()

        assert "'min x' should be less than 'max x'" in error_text


    def test_invalid_function(self):
        self.window.function.setText("x**")

        QTest.mouseClick(self.window.button1, Qt.LeftButton)


        error_text = self.window.error_dialog.text()
        assert "Function Error!" in error_text


    def test_default_function_and_range(self):
        QTest.mouseClick(self.window.button1, Qt.LeftButton)

        assert self.window.axes.lines

    def test_function_error_message(self):
        self.window.function.setText("x**2 +")

        QTest.mouseClick(self.window.button1, Qt.LeftButton)

        error_text = self.window.error_dialog.text()
        assert "Function Error!" in error_text

    def test_plot_clear_on_new_entry(self):
        self.window.function.setText("x**2")
        self.window.min.setValue(-5)
        self.window.max.setValue(5)

        QTest.mouseClick(self.window.button1, Qt.LeftButton)

        self.window.function.setText("")

        QTest.mouseClick(self.window.button1, Qt.LeftButton)

        assert not self.window.axes.lines

    def test_empty_function_entry(self):
        self.window.min.setValue(-10)
        self.window.max.setValue(10)

        self.window.function.setText("")

        QTest.mouseClick(self.window.button1, Qt.LeftButton)

        assert not self.window.axes.lines

    def test_valid_function_with_zero_range(self):
        self.window.function.setText("x**2")

        self.window.min.setValue(0)
        self.window.max.setValue(0)

        QTest.mouseClick(self.window.button1, Qt.LeftButton)

        assert self.window.axes.lines

