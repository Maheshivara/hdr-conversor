from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
)


class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 900, 700)

        layout = QGridLayout()
        self.grid_layout = layout
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)
        layout.setHorizontalSpacing(10)
        layout.setContentsMargins(8, 8, 8, 8)
        self.setLayout(layout)
