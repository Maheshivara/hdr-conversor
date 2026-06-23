from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
)

from interface.gui.viewmodel.home_screen import HomeScreenViewModel


class HomeScreen(QWidget):
    def __init__(self, view_model: HomeScreenViewModel):
        super().__init__()
        self._view_model = view_model
        layout = QGridLayout()
        self.grid_layout = layout
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)
        layout.setHorizontalSpacing(10)
        layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(layout)
