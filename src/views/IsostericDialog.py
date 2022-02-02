from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView
from src.widgets.UtilityWidgets import LabelAlignRight
from src.widgets.UtilityWidgets import LabelOutput
from src.widgets.UtilityWidgets import LabelResult


class IsostericDialog(QW.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("IsostericDialog")

        _layout = QW.QGridLayout(self)

        self.options_box = QW.QGroupBox()
        _layout.addWidget(self.options_box, 0, 0, 1, 1)
        self.results_box = QW.QGroupBox()
        _layout.addWidget(self.results_box, 0, 1, 1, 1)

        # Options box
        self.options_layout = QW.QGridLayout(self.options_box)

        # Iso graph and slider
        self.iso_graph = IsoGraphView(y_range_select=True)
        self.iso_graph.setObjectName("iso_graph")
        self.y_select = self.iso_graph.y_range_select
        self.options_layout.addWidget(self.iso_graph, 0, 0, 1, 2)

        # Branch used
        self.branch_label = LabelAlignRight("Branch used:")
        self.branch_dropdown = QW.QComboBox()
        self.points_label = LabelAlignRight("Number of points:")
        self.points_input = QW.QSpinBox()
        self.options_layout.addWidget(self.branch_label, 1, 0, 1, 1)
        self.options_layout.addWidget(self.branch_dropdown, 1, 1, 1, 1)
        # self.options_layout.addWidget(self.points_label, 2, 0, 1, 1)
        # self.options_layout.addWidget(self.points_input, 2, 1, 1, 1)

        # Autodetermine
        self.calc_auto_button = QW.QPushButton()
        self.options_layout.addWidget(self.calc_auto_button, 3, 0, 1, 2)

        # Results graph box
        self.results_layout = QW.QGridLayout(self.results_box)

        # Enthalpy graph
        self.res_graph = GraphView()
        self.results_layout.addWidget(self.res_graph, 0, 0, 2, 2)

        self.output_label = QW.QLabel("Calculation log:")
        self.output = LabelOutput()
        self.results_layout.addWidget(self.output_label, 2, 0, 1, 2)
        self.results_layout.addWidget(self.output, 3, 0, 2, 2)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox()
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Close)
        _layout.addWidget(self.button_box, 2, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1100, 800)

    def connect_signals(self):
        pass

    def translate_UI(self):
        # yapf: disable
        # pylint: disable=line-too-long
        self.setWindowTitle(QW.QApplication.translate("IsostericDialog", "Isosteric Enthalpy", None, -1))
        self.options_box.setTitle(QW.QApplication.translate("IsostericDialog", "Options", None, -1))
        self.results_box.setTitle(QW.QApplication.translate("IsostericDialog", "Results", None, -1))
        self.calc_auto_button.setText(QW.QApplication.translate("IsostericDialog", "Full range calculation", None, -1))
        # yapf: enable
