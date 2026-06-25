from typing import Optional

import qtawesome as qta
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QPushButton,
    QWidget,
)

from interface.gui.viewmodel.effect_list import EffectListViewModel


class EffectList(QWidget):
    def __init__(
        self, view_model: EffectListViewModel, parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._view_model = view_model

        self._available = self._view_model.get_effects()

        self._view_model.changed_language.connect(self._retranslate)
        self._view_model.changed_theme.connect(self._retranslate)
        self._view_model.list_updated.connect(self._build_list_items)

        self._build()

    def _build(self):
        self._layout = QGridLayout()
        self._label = QLabel()
        self._label.setText(self._view_model.t("ui.home.effect_list.label"))
        self._list_widget = QListWidget(self)
        self._build_list_items()

        self._add_effect_btn = QPushButton()
        self._add_effect_btn.setIcon(qta.icon("fa5.plus-square"))
        self._add_effect_menu = QMenu()

        self._build_effect_menu()

        self._layout.addWidget(self._label, 0, 0, 1, 1)
        self._layout.addWidget(self._add_effect_btn, 0, 1, 1, 1)
        self._layout.addWidget(self._list_widget, 1, 0, 3, 2)
        self.setLayout(self._layout)

    def _build_effect_menu(self):
        self._add_effect_menu.clear()
        for effect in self._available:
            action = QAction(
                self._view_model.t(f"ui.home.effect_list.effect.{effect.name}"), self
            )
            action.triggered.connect(
                lambda _, ef=effect: self._view_model.add_effect(ef)
            )
            self._add_effect_menu.addAction(action)

        self._add_effect_btn.setMenu(self._add_effect_menu)

    def _build_list_items(self):
        self._list_widget.clear()
        current = self._view_model.get_current()

        for key, effect in current.items():
            item = QListWidgetItem()
            item_widget = QWidget()

            line_text = QLabel(
                self._view_model.t(
                    f"ui.home.effect_list.effect.{effect.get_type().name}"
                )
            )
            line_push_button = QPushButton()
            icon = qta.icon("fa6.trash-can")
            line_push_button.setIcon(icon)

            item_layout = QGridLayout()
            item_layout.addWidget(line_text, 0, 0, 1, 2)
            item_layout.addWidget(line_push_button, 0, 3, 1, 1)

            line_push_button.clicked.connect(
                lambda _, i=key: self._view_model.remove_effect(i)
            )
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self._list_widget.addItem(item)
            self._list_widget.setItemWidget(item, item_widget)

    def _retranslate(self):
        self._label.setText(self._view_model.t("ui.home.effect_list.label"))
        self._build_effect_menu()
        self._build_list_items()
