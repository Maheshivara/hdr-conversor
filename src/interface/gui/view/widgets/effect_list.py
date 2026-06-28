from typing import Optional

import qtawesome as qta
from PySide6.QtGui import QAction, Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QWidget,
)

from interface.gui.view.widgets.effect import Effect
from interface.gui.viewmodel.effect_list import EffectListViewModel
from interface.gui.viewmodel.home_screen import HomeScreenViewModel


class EffectList(QWidget):
    def __init__(
        self,
        home_view_model: HomeScreenViewModel,
        view_model: EffectListViewModel,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._view_model = view_model
        self._home_view_model = home_view_model

        self._available = self._view_model.get_effects()

        self._home_view_model.changed_language.connect(self._retranslate)
        self._home_view_model.changed_theme.connect(self._retranslate)
        self._view_model.list_updated.connect(self._build_list_items)

        self._build()

    def _build(self):
        self._layout = QGridLayout()
        self._label = QLabel()
        self._label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self._label.setText(self._home_view_model.t("ui.home.effect_list.label"))
        self._list_widget = QListWidget(self)
        self._build_list_items()

        self._add_effect_btn = QPushButton()
        self._add_effect_btn.setIcon(qta.icon("fa5.plus-square"))
        self._add_effect_btn.setText(self._home_view_model.t("ui.home.effect_list.add"))
        self._add_effect_menu = QMenu()
        self._add_effect_btn.setMenu(self._add_effect_menu)

        self._build_effect_menu()

        self._layout.addWidget(self._label, 0, 0, 1, 2)
        self._layout.addWidget(self._list_widget, 1, 0, 9, 2)
        self._layout.addWidget(self._add_effect_btn, 10, 0, 1, 2)
        self.setLayout(self._layout)

    def _build_effect_menu(self):
        self._add_effect_menu.clear()
        for effect in self._available:
            action = QAction(
                self._home_view_model.t(
                    f"ui.home.effect_list.effect.{effect.name}.name"
                ),
                self,
            )
            action.triggered.connect(
                lambda _, ef=effect: self._view_model.add_effect(ef)
            )
            self._add_effect_menu.addAction(action)

    def _build_list_items(self):
        self._list_widget.clear()
        current = self._view_model.get_current()[0]

        for key, effect in current.items():
            name = self._home_view_model.t(
                f"ui.home.effect_list.effect.{effect.type.name}.name"
            )
            effect_item = QListWidgetItem()
            effect_widget = Effect(
                name,
                key,
                effect,
                self._home_view_model,
                self._view_model.update_effect_param,
                self._view_model.remove_effect,
            )

            effect_item.setSizeHint(effect_widget.sizeHint())
            self._list_widget.addItem(effect_item)
            self._list_widget.setItemWidget(effect_item, effect_widget)

    def _retranslate(self):
        self._label.setText(self._home_view_model.t("ui.home.effect_list.label"))
        self._add_effect_btn.setText(self._home_view_model.t("ui.home.effect_list.add"))
        self._build_effect_menu()
        self._build_list_items()
