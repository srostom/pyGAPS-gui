from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from qtpy import PYSIDE6
if PYSIDE6:
    import PySide6.QtSvgWidgets as QS
else:
    from qtpy import QtSvg as QS

from src.views.IsoGraphView import IsoModelGraphView
from src.widgets.UtilityWidgets import (EditAlignRight, LabelAlignRight, LabelOutput, LabelResult)


class IsoModelByDialog(QW.QDialog):

    paramWidgets = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_UI()
        self.translate_UI()
        self.connect_signals()

    def setup_UI(self):
        self.setObjectName("IsoModelByDialog")

        layout = QW.QGridLayout(self)
        layout.setObjectName("layout")

        # Model selection and parameters
        self.options_layout = QW.QVBoxLayout()
        layout.addLayout(self.options_layout, 0, 0)

        modelLayout = QW.QFormLayout()
        self.options_layout.addLayout(modelLayout)

        # Model selection
        self.modelLabel = LabelAlignRight("Model:", parent=self)
        self.modelDropdown = QW.QComboBox(self)
        modelLayout.addRow(self.modelLabel, self.modelDropdown)

        # Branch selection
        self.branchLabel = LabelAlignRight("Branch:", parent=self)
        self.branchDropdown = QW.QComboBox(self)
        modelLayout.addRow(self.branchLabel, self.branchDropdown)

        btnLayout = QW.QHBoxLayout()
        self.autoButton = QW.QPushButton(self)
        btnLayout.addWidget(self.autoButton)
        self.manualButton = QW.QPushButton(self)
        btnLayout.addWidget(self.manualButton)
        self.options_layout.addLayout(btnLayout)

        # Parameter box
        self.paramBox = QW.QGroupBox(self)
        self.options_layout.addWidget(self.paramBox)
        self.paramLayout = QW.QVBoxLayout(self.paramBox)
        self.modelFormulaValue = QS.QSvgWidget(self.paramBox)
        self.modelFormulaValue.setMinimumSize(10, 50)
        self.paramLayout.addWidget(self.modelFormulaValue)

        self.options_layout.addStretch()

        # Output log
        self.output_label = QW.QLabel("Output log:")
        layout.addWidget(self.output_label, 1, 0)
        self.output = LabelOutput(self)
        layout.addWidget(self.output, 2, 0)

        # Isotherm display
        self.isoGraph = IsoModelGraphView(self, x_range_select=True)
        self.x_select = self.isoGraph.x_range_select
        layout.addWidget(self.isoGraph, 0, 1, 3, 1)

        # Bottom buttons
        self.button_box = QW.QDialogButtonBox(self)
        self.button_box.setOrientation(QC.Qt.Horizontal)
        self.button_box.setStandardButtons(QW.QDialogButtonBox.Save | QW.QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box, 3, 0, 1, 2)

    def sizeHint(self) -> QC.QSize:
        return QC.QSize(1000, 800)

    def connect_signals(self):
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def translate_UI(self):
        self.setWindowTitle(
            QW.QApplication.translate("IsoModelByDialog", "Isotherm model fitting", None, -1)
        )
        self.paramBox.setTitle(
            QW.QApplication.translate("IsoModelByDialog", "Parameters", None, -1)
        )
        self.autoButton.setText(QW.QApplication.translate("IsoModelByDialog", "Autofit", None, -1))
        self.manualButton.setText(
            QW.QApplication.translate("IsoModelByDialog", "Use selected parameters", None, -1)
        )
