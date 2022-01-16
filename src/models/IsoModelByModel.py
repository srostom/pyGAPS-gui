from math import inf
import warnings
import numpy

from pygaps.modelling import _MODELS
from pygaps.modelling import get_isotherm_model
from pygaps import ModelIsotherm

from qtpy import QtCore as QC
from src.utilities.tex2svg import tex2svg
from src.widgets.SpinBoxSlider import QHSpinBoxSlider

from src.widgets.UtilityWidgets import error_dialog


class IsoModelByModel():

    isotherm = None
    model_isotherm = None
    view = None

    # Settings
    branch = "ads"
    limits = None
    auto = True
    current_model = None
    current_model_name = None

    # Results
    output = ""
    success = True

    def __init__(self, isotherm, view):
        """First init"""
        # Save refs
        self.isotherm = isotherm
        self.view = view

        # Fail condition
        if isinstance(isotherm, ModelIsotherm):
            error_dialog("Isotherm selected is already a model")
            self.success = False
            return

        # view setup
        self.view.modelDropdown.addItems(_MODELS),
        self.view.branchDropdown.addItems(["ads", "des"])
        self.view.branchDropdown.setCurrentText(self.branch)

        # plot setup
        self.view.isoGraph.set_isotherms([self.isotherm])
        self.limits = self.view.isoGraph.x_range

        # connect signals
        self.view.modelDropdown.currentIndexChanged.connect(self.select_model)
        self.view.branchDropdown.currentIndexChanged.connect(self.select_branch)
        self.view.x_select.slider.rangeChanged.connect(self.model_with_limits)
        self.view.autoButton.clicked.connect(self.model_auto)
        self.view.manualButton.clicked.connect(self.model_manual)

        # populate initial
        self.select_model()

    def model_auto(self):
        """Automatic calculation."""
        self.auto = True
        self.model()
        self.set_model_params()
        self.output_results()
        self.plot_results()

    def model_with_limits(self, left, right):
        """Set limits on calculation."""
        self.limits = [left, right]
        # self.model_auto()

    def model_manual(self):
        """Use model parameters."""
        self.auto = False
        self.get_model_params()
        self.model()
        self.output_results()
        self.plot_results()

    def model(self):
        self.model_isotherm = None
        with warnings.catch_warnings(record=True) as warning:
            warnings.simplefilter("always")
            try:
                if self.auto:

                    iso_params = self.isotherm.to_dict()
                    pressure = self.isotherm.pressure(
                        branch=self.branch,
                        limits=self.limits,
                        indexed=True,
                    )
                    loading = self.isotherm.loading(
                        branch=self.branch,
                        indexed=True,
                    )
                    loading = loading[pressure.index]

                    self.model_isotherm = ModelIsotherm(
                        pressure=pressure.values,
                        loading=loading.values,
                        branch=self.branch,
                        model=self.current_model_name,
                        **iso_params
                    )
                    self.current_model = self.model_isotherm.model
                else:
                    self.model_isotherm = ModelIsotherm(
                        model=self.current_model,
                        branch=self.branch,
                        **self.isotherm.to_dict(),
                    )

            # We catch any errors or warnings and display them to the user
            except Exception as e:
                self.output += f'<font color="red">Model fitting failed! <br> {e}</font>'

            if warning:
                self.output += '<br>'.join([
                    f'<font color="red">Fitting warning: {a.message}</font>' for a in warning
                ])

    def select_model(self):
        self.model_isotherm = None
        self.current_model_name = self.view.modelDropdown.currentText()
        self.current_model = get_isotherm_model(self.current_model_name)

        # Model formula display
        if self.current_model.formula:
            self.view.modelFormulaValue.setVisible(True)
            self.view.modelFormulaValue.load(tex2svg(self.current_model.formula))
            aspectRatioMode = QC.Qt.AspectRatioMode(QC.Qt.KeepAspectRatio)
            self.view.modelFormulaValue.renderer().setAspectRatioMode(aspectRatioMode)
        else:
            self.view.modelFormulaValue.setVisible(False)

        # Model parameters
        for param in self.view.paramWidgets:
            self.view.paramWidgets[param].deleteLater()
        self.view.paramWidgets = {}

        for param in self.current_model.param_names:
            widget = QHSpinBoxSlider(parent=self.view.paramBox)
            widget.setText(param)
            minv, maxv = self.current_model.param_bounds[param]
            if not minv or minv == -numpy.inf:
                minv = 0
            if not maxv or maxv == numpy.inf:
                maxv = 100
            widget.setRange(minv=minv, maxv=maxv)
            self.view.paramLayout.addWidget(widget)
            self.view.paramWidgets[param] = widget

        # Update plot
        self.plot_results()

    def set_model_params(self):
        for param in self.current_model.param_names:
            pval = self.current_model.params[param]
            minv, maxv = self.current_model.param_bounds[param]
            if not minv or minv == -numpy.inf:
                minv = 0
            if not maxv or maxv == numpy.inf:
                maxv = pval * 2
            self.view.paramWidgets[param].setRange(minv=minv, maxv=maxv)
            self.view.paramWidgets[param].setValue(pval)

    def get_model_params(self):
        for param in self.current_model.params:
            pval = self.view.paramWidgets[param].getValue()
            self.current_model.params[param] = float(pval)

        # The pressure range on which the model was built.
        self.current_model.pressure_range = self.limits

        # The loading range on which the model was built.
        loading = self.isotherm.loading(branch=self.branch)
        self.current_model.loading_range = [min(loading), max(loading)]

    def select_branch(self):
        self.branch = self.view.branchDropdown.currentText()
        self.view.isoGraph.branch = self.branch
        self.model_isotherm = None
        self.plot_results()

    def slider_reset(self):
        self.view.p_selector.setValues(self.limits, emit=False)
        self.view.isoGraph.draw_limits(self.limits[0], self.limits[1])

    def output_results(self):
        self.view.output.setText(self.output)
        self.output = ""

    def plot_results(self):
        self.view.isoGraph.model_isotherm = self.model_isotherm
        self.view.isoGraph.draw_isotherms(branch=self.branch)
