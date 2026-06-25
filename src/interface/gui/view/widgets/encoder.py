import qtawesome as qta
from PySide6.QtGui import QActionGroup
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.models.input import FloatInput
from interface.gui.viewmodel.encoder import EncoderViewModel


class Encoder(QWidget):
    def __init__(self, view_model: EncoderViewModel):
        super().__init__()
        self._view_model = view_model

        self._view_model.changed_language.connect(self._retranslate)
        self._view_model.changed_theme.connect(self._retranslate)

        self._build()

    def _build(self):
        self._layout = QVBoxLayout()
        self._encoders_btn = QPushButton()
        self._encoders_btn.setIcon(qta.icon("fa6s.code-compare"))
        self._encoders_btn.setText(self._view_model.t("ui.home.encoders.label"))

        self._encoders_menu = QMenu()
        self._encoders_menu_group = QActionGroup(self)
        self._encoders_menu_group.setExclusive(True)
        self._encoders_btn.setMenu(self._encoders_menu)

        self._build_encoders_menu()

        self._control_widget = QWidget()
        self._control_widget_layout = QVBoxLayout()
        self._encoder_control_label = QLabel()
        self._encoder_control_inputs = QListWidget()
        self._build_encoder_control()

        self._control_widget_layout.addWidget(self._encoder_control_label)
        self._control_widget_layout.addWidget(self._encoder_control_inputs)

        self._control_widget.setLayout(self._control_widget_layout)

        self._layout.addWidget(self._encoders_btn)
        self._layout.addWidget(self._control_widget)
        self.setLayout(self._layout)

    def _build_encoders_menu(self):
        self._encoders_menu.clear()
        self._current = self._view_model.get_current()
        available = self._view_model.get_available()

        for encoder in available:
            name = self._view_model.t(f"ui.home.encoders.names.{encoder}")
            action = self._encoders_menu_group.addAction(name)
            action.setCheckable(True)
            if encoder == self._current[0]:
                action.setChecked(True)
            action.triggered.connect(
                lambda _, e=encoder: self._view_model.set_current(e)
            )
            self._encoders_menu.addAction(action)

    def _build_encoder_control(self):
        self._encoder_control_inputs.clear()

        current = self._view_model.get_current()
        name = self._view_model.t(f"ui.home.encoders.names.{current[0]}")
        self._encoder_control_label.setText(name)
        inputs = current[1].get_inputs()

        show = len(inputs) > 0
        self._encoder_control_inputs.setVisible(show)
        self._encoder_control_inputs.setDisabled(not show)

        for key, input in inputs.items():
            item = QListWidgetItem()
            if isinstance(input, FloatInput):
                input_widget = self._build_float(key, input)
                item.setSizeHint(input_widget.sizeHint())
                self._encoder_control_inputs.addItem(item)
                self._encoder_control_inputs.setItemWidget(item, input_widget)

    def _build_float(self, name: str, i: FloatInput) -> QWidget:
        label = QLabel()
        label.setText(i.get_display_name())

        input = QDoubleSpinBox()
        input.setMaximum(1000)
        input.setMinimum(-1000)
        value = i.get_value()
        if value is None:
            value = 0
        input.setValue(value)
        input.valueChanged.connect(
            lambda nv, key=name: self._view_model.update_param(key, nv)
        )
        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(input)
        widget.setLayout(layout)
        return widget

    def _retranslate(self):
        self._encoders_btn.setText(self._view_model.t("ui.home.encoders.label"))
        self._build_encoders_menu()
        self._build_encoder_control()
