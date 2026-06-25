from typing import Any, Callable

import qtawesome as qta
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QDoubleSpinBox,
    QGridLayout,
    QLayout,
    QSpinBox,
)
from qtpy.QtWidgets import (
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.filters.image_filter import ImageFilter
from core.models.input import FloatInput, IntegerInput


class Effect(QWidget):
    def __init__(
        self,
        name: str,
        idx: int,
        effect: ImageFilter,
        on_param_update: Callable[[int, str, Any], None],
        on_remove_effect: Callable[[int], None],
    ):
        super().__init__()
        self._name = name
        self._idx = idx
        self._effect = effect
        self._on_param_update = on_param_update
        self._on_remove_effect = on_remove_effect

        self._build()

    def _build(self):
        self._layout = QGridLayout()
        self._label = QLabel()
        self._label.setText(self._name)

        self._btn = QPushButton()
        icon = qta.icon("fa6.trash-can")
        self._btn.setIcon(icon)
        self._btn.clicked.connect(lambda _, i=self._idx: self._on_remove_effect(i))

        self._params_widget = QListWidget()
        self._build_params()

        self._layout.addWidget(self._label, 0, 0, 1, 3)
        self._layout.addWidget(self._btn, 0, 4, 1, 1)
        self._layout.addWidget(self._params_widget, 1, 0, 5, 4)
        self.setLayout(self._layout)

    def _build_params(self):
        self._params_widget.clear()
        for key, param in self._effect.get_params().items():
            if isinstance(param, FloatInput):
                self._build_float(key, param)
                continue
            if isinstance(param, IntegerInput):
                self._build_int(key, param)
        self._params_widget.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

    def _build_float(self, key: str, param: FloatInput):
        item = QListWidgetItem()
        item_widget = QWidget()

        text = QLabel(param.get_display_name())

        spin_box = QDoubleSpinBox()
        value = param.get_value()
        if value is None:
            value = 0

        spin_box.setMaximum(1000)
        spin_box.setMinimum(-1000)
        spin_box.setValue(value)
        spin_box.valueChanged.connect(
            lambda nv, k=key, i=self._idx: self._on_param_update(i, k, nv)
        )
        item_layout = QVBoxLayout()
        item_layout.addWidget(text)
        item_layout.addWidget(spin_box)

        item_widget.setLayout(item_layout)
        item.setSizeHint(item_widget.sizeHint())
        self._params_widget.addItem(item)
        self._params_widget.setItemWidget(item, item_widget)

    def _build_int(self, key: str, param: IntegerInput):
        item = QListWidgetItem()
        item_widget = QWidget()

        text = QLabel(param.get_display_name())

        spin_box = QSpinBox()
        value = param.get_value()
        if value is None:
            value = 0

        spin_box.setMaximum(1000)
        spin_box.setMinimum(-1000)
        spin_box.setValue(value)
        spin_box.valueChanged.connect(
            lambda nv, k=key, i=self._idx: self._on_param_update(i, k, nv)
        )
        item_layout = QVBoxLayout()
        item_layout.addWidget(text)
        item_layout.addWidget(spin_box)
        item_layout.setSizeConstraints(
            QLayout.SizeConstraint.SetMaximumSize, QLayout.SizeConstraint.SetMinimumSize
        )
        item_widget.setLayout(item_layout)
        item.setSizeHint(item_widget.sizeHint())
        self._params_widget.addItem(item)
        self._params_widget.setItemWidget(item, item_widget)
