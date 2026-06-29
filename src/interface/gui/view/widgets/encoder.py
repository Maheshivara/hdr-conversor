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
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from interface.gui.viewmodel.encoder import EncoderViewModel
from interface.gui.viewmodel.home_screen import HomeScreenViewModel
from shared.constants import AvailableInput


class Encoder(QWidget):
    def __init__(
        self, home_view_model: HomeScreenViewModel, view_model: EncoderViewModel
    ):
        super().__init__()
        self._view_model = view_model
        self._home_view = home_view_model

        self._home_view.changed_language.connect(self._retranslate)
        self._home_view.changed_theme.connect(self._retranslate)

        self._view_model.updated_encoder.connect(self._build_encoder_control)
        self._view_model.updated_encoder.connect(self._build_encoders_menu)

        self._build()

    def _build(self):
        self._layout = QVBoxLayout()
        self._encoders_btn = QPushButton()
        self._encoders_btn.setIcon(qta.icon("fa6s.code-compare"))
        self._encoders_btn.setText(self._home_view.t("ui.home.encoders.label"))

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
        current = self._view_model.get_current()
        if current is None:
            return
        available = self._view_model.get_available()

        for encoder in available:
            name = self._home_view.t(f"ui.home.encoders.{encoder.name}.name")
            action = self._encoders_menu_group.addAction(name)
            action.setCheckable(True)
            if encoder == current.type:
                action.setChecked(True)
            action.triggered.connect(
                lambda _, e=encoder: self._view_model.set_current(e)
            )
            self._encoders_menu.addAction(action)

    def _build_encoder_control(self):
        self._encoder_control_inputs.clear()

        current = self._view_model.get_current()
        if current is None:
            return

        name = self._home_view.t(f"ui.home.encoders.{current.type.name}.name")
        self._encoder_control_label.setText(name)
        inputs = current.inputs

        show = len(inputs) > 0
        self._encoder_control_inputs.setVisible(show)
        self._encoder_control_inputs.setDisabled(not show)

        for key, input in inputs.items():
            item = QListWidgetItem()
            type = input[0]
            value = input[1]
            match type:
                case AvailableInput.FLOAT:
                    input_widget = self._build_float(current.type.name, key, value)
                    item.setSizeHint(input_widget.sizeHint())
                    self._encoder_control_inputs.addItem(item)
                    self._encoder_control_inputs.setItemWidget(item, input_widget)

                case AvailableInput.INT:
                    input_widget = self._build_int(current.type.name, key, value)
                    item.setSizeHint(input_widget.sizeHint())
                    self._encoder_control_inputs.addItem(item)
                    self._encoder_control_inputs.setItemWidget(item, input_widget)

    def _build_float(self, effect_name: str, name: str, value: float | None) -> QWidget:
        label = QLabel()
        label.setText(self._home_view.t(f"ui.home.encoders.{effect_name}.{name}"))

        input = QDoubleSpinBox()
        input.setMaximum(1000)
        input.setMinimum(-1000)

        v = value
        if v is None:
            v = 0

        input.setValue(v)
        input.valueChanged.connect(
            lambda nv, key=name: self._view_model.update_param(key, nv)
        )

        widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(input)
        widget.setLayout(layout)
        return widget

    def _build_int(self, effect_name: str, name: str, value: int | None) -> QWidget:
        label = QLabel()
        label.setText(self._home_view.t(f"ui.home.encoders.{effect_name}.{name}"))

        input = QSpinBox()
        input.setMaximum(1000)
        input.setMinimum(-1000)
        v = value

        if v is None:
            v = 0

        input.setValue(v)
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
        self._encoders_btn.setText(self._home_view.t("ui.home.encoders.label"))
        self._build_encoders_menu()
        self._build_encoder_control()
