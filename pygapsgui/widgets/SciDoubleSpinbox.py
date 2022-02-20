"""Scientific spin box
Adapted from https://gist.github.com/jdreaver/0be2e44981159d0854f5
"""

import re

import numpy as np
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

# Regular expression to find floats. Match groups are the whole string, the
# whole coefficient, the decimal part of the coefficient, and the exponent
# part.
_float_re = re.compile(r'(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)')


def valid_float_string(string):
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False


class FloatValidator(QG.QValidator):
    def validate(self, string, position):
        if valid_float_string(string):
            return self.State.Acceptable
        if string == "" or string[position - 1] in 'e.-+':
            return self.State.Intermediate
        return self.State.Invalid

    def fixup(self, text):
        match = _float_re.search(text)
        return match.groups()[0] if match else ""


class ScientificDoubleSpinBox(QW.QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimum(-np.inf)
        self.setMaximum(np.inf)
        self.validator = FloatValidator()
        self.setDecimals(1000)
        self.setAlignment(QC.Qt.AlignCenter)

    def validate(self, text, position):
        return self.validator.validate(text, position)

    def fixup(self, text):
        return self.validator.fixup(text)

    def valueFromText(self, text):
        return float(text)

    def textFromValue(self, value):
        return format_float(value)

    def stepBy(self, steps):
        text = self.cleanText()
        groups = _float_re.search(text).groups()
        decimal = float(groups[1])
        decimal += steps
        new_string = f"{decimal:g}" + (groups[3] if groups[3] else "")
        self.lineEdit().setText(new_string)


class SciFloatSpinDelegate(QW.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        """Give an instance of the SciDoubleSpinbox"""
        return ScientificDoubleSpinBox(parent)

    def setEditorData(self, editor: QW.QWidget, index: QC.QModelIndex) -> None:
        """Ensure that the SciDoubleSpinbox data is set correctly."""
        editor.setValue(index.data())

    def displayText(self, value, locale):
        return format_float(value)


class SciFloatDelegate(QW.QStyledItemDelegate):
    def displayText(self, value, locale):
        return format_float(value)


def format_float(value):
    """Modified form of the 'g' format specifier."""
    if type(value) == str:
        return value
    string = f"{value:.5g}".replace("e+", "e")
    string = re.sub("e(-?)0*(\d+)", r"e\1\2", string)
    return string
