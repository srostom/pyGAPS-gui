from qtpy import QtCore as QC
from qtpy import QtWidgets as QW

from src.views.GraphView import GraphView
from src.views.IsoGraphView import IsoGraphView
from src.views.RangeSlider import QHSpinBoxRangeSlider

from src.widgets.UtilityWidgets import LabelAlignRight, LabelOutput, LabelResult


class BETDialog(QW.QDialog):

    isotherm = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("BETDialog")
        self.resize(1000, 800)

        self.layout = QW.QGridLayout(self)
        self.layout.setObjectName("layout")

        # Isotherm display
        self.isoGraph = GraphView(self)
        self.isoGraph.setObjectName("isoGraph")
        self.layout.addWidget(self.isoGraph, 0, 0, 1, 1)

        # BET plot
        self.betGraph = GraphView(self)
        self.betGraph.setObjectName("betGraph")
        self.layout.addWidget(self.betGraph, 0, 1, 1, 1)

        # Rouquerol plot
        self.rouqGraph = GraphView(self)
        self.rouqGraph.setObjectName("rouqGraph")
        self.layout.addWidget(self.rouqGraph, 1, 1, 1, 1)

        # Options/results box

        self.optionsBox = QW.QGroupBox('Options', self)
        self.layout.addWidget(self.optionsBox, 1, 0, 1, 1)

        self.optionsLayout = QW.QGridLayout(self.optionsBox)
        self.pSlider = QHSpinBoxRangeSlider(
            parent=self, dec_pnts=2, slider_range=[0, 1, 0.01], values=[0, 1]
        )
        self.pSlider.setMaximumHeight(50)
        self.pSlider.setEmitWhileMoving(False)
        self.optionsLayout.addWidget(self.pSlider, 0, 0, 1, 4)

        self.optionsLayout.addWidget(QW.QLabel("Fit (R):"), 1, 0, 1, 1)
        self.result_r = LabelResult(self)
        self.optionsLayout.addWidget(self.result_r, 1, 1, 1, 1)
        self.auto_button = QW.QPushButton('Auto-determine', self)
        self.optionsLayout.addWidget(self.auto_button, 1, 3, 1, 1)

        # description labels
        self.optionsLayout.addWidget(
            QW.QLabel("Calculated results:"), 2, 0, 1, 2
        )
        self.optionsLayout.addWidget(LabelAlignRight("BET area:"), 3, 0, 1, 1)
        self.optionsLayout.addWidget(
            LabelAlignRight("C constant:"), 3, 2, 1, 1
        )
        self.optionsLayout.addWidget(
            LabelAlignRight("Monolayer uptake:"), 4, 0, 1, 1
        )
        self.optionsLayout.addWidget(
            LabelAlignRight("Monolayer pressure:"), 4, 2, 1, 1
        )
        self.optionsLayout.addWidget(LabelAlignRight("Slope:"), 5, 0, 1, 1)
        self.optionsLayout.addWidget(LabelAlignRight("Intercept:"), 5, 2, 1, 1)

        # result labels
        self.result_bet = LabelResult(self)
        self.optionsLayout.addWidget(self.result_bet, 3, 1, 1, 1)
        self.result_c = LabelResult(self)
        self.optionsLayout.addWidget(self.result_c, 3, 3, 1, 1)
        self.result_mono_n = LabelResult(self)
        self.optionsLayout.addWidget(self.result_mono_n, 4, 1, 1, 1)
        self.result_mono_p = LabelResult(self)
        self.optionsLayout.addWidget(self.result_mono_p, 4, 3, 1, 1)
        self.result_slope = LabelResult(self)
        self.optionsLayout.addWidget(self.result_slope, 5, 1, 1, 1)
        self.result_intercept = LabelResult(self)
        self.optionsLayout.addWidget(self.result_intercept, 5, 3, 1, 1)

        self.optionsLayout.addWidget(
            QW.QLabel("Calculation output:"), 6, 0, 1, 2
        )
        self.output = LabelOutput(self)
        self.optionsLayout.addWidget(self.output, 7, 0, 2, 4)

        # Bottom buttons
        self.buttonBox = QW.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QC.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QW.QDialogButtonBox.Cancel | QW.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.layout.addWidget(self.buttonBox)

        self.retranslateUi()
        QC.QObject.connect(
            self.buttonBox, QC.SIGNAL("accepted()"), self.accept
        )
        QC.QObject.connect(
            self.buttonBox, QC.SIGNAL("rejected()"), self.reject
        )
        QC.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(
            QW.QApplication.translate(
                "BETDialog", "BET area calculation", None, -1
            )
        )
