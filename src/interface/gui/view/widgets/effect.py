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

from application.dto.effects import EffectDTO
from interface.gui.viewmodel.home_screen import HomeScreenViewModel
from shared.constants import AvailableInput


class Effect(QWidget):
    def __init__(
        self,
        name: str,
        idx: int,
        effect: EffectDTO,
        home_view_model: HomeScreenViewModel,
        on_param_update: Callable[[int, str, Any], None],
        on_remove_effect: Callable[[int], None],
    ):
        super().__init__()
        self._home_view = home_view_model
        self._name = name
        self._type = effect.type
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
        for key, param in self._effect.inputs.items():
            type = param[0]
            value = param[1]
            match type:
                case AvailableInput.INT:
                    self._build_int(key, value)
                case AvailableInput.FLOAT:
                    self._build_float(key, value)

        self._params_widget.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

    def _build_float(self, key: str, value: float | None):
        item = QListWidgetItem()
        item_widget = QWidget()

        text = QLabel(
            self._home_view.t(
                f"ui.home.effect_list.effect.{self._type.name}.inputs.{key}"
            )
        )

        spin_box = QDoubleSpinBox()
        v = value
        if v is None:
            v = 0

        spin_box.setMaximum(1000)
        spin_box.setMinimum(-1000)
        spin_box.setValue(v)
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

    def _build_int(self, key: str, value: int | None):
        item = QListWidgetItem()
        item_widget = QWidget()

        text = QLabel(
            self._home_view.t(
                f"ui.home.effect_list.effect.{self._type.name}.inputs.{key}"
            )
        )

        spin_box = QSpinBox()
        v = value
        if v is None:
            v = 0

        spin_box.setMaximum(1000)
        spin_box.setMinimum(-1000)
        spin_box.setValue(v)
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
