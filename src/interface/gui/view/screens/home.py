from PySide6.QtGui import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
)

from interface.gui.model.effect_list import EffectListModel
from interface.gui.model.encoder import EncoderModel
from interface.gui.model.image_list import ImageListModel
from interface.gui.view.widgets.effect_list import EffectList
from interface.gui.view.widgets.encoder import Encoder
from interface.gui.view.widgets.image_list import ImageList
from interface.gui.viewmodel.effect_list import EffectListViewModel
from interface.gui.viewmodel.encoder import EncoderViewModel
from interface.gui.viewmodel.home_screen import HomeScreenViewModel
from interface.gui.viewmodel.image_list import ImageListViewModel


class HomeScreen(QWidget):
    def __init__(self, view_model: HomeScreenViewModel):
        super().__init__()
        self._view_model = view_model
        self._layout = QGridLayout()
        self._layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._layout.setHorizontalSpacing(10)
        self._layout.setContentsMargins(8, 8, 8, 8)

        image_list_widget_view_model = ImageListViewModel(
            self._view_model, ImageListModel()
        )
        self._image_list_widget = ImageList(image_list_widget_view_model, self)

        effect_list_view_model = EffectListViewModel(
            self._view_model, EffectListModel()
        )
        self._effect_list_widget = EffectList(effect_list_view_model, self)

        encoder_view_model = EncoderViewModel(
            self._view_model, effect_list_view_model, EncoderModel()
        )
        self._encoders = Encoder(encoder_view_model)

        self._layout.addWidget(self._image_list_widget, 0, 0, 5, 2)
        self._layout.addWidget(self._effect_list_widget, 0, 2, 5, 2)
        self._layout.addWidget(self._encoders, 6, 0, 1, 2)

        self._layout.setColumnStretch(0, 1)
        self._layout.setColumnStretch(2, 1)
        self._layout.setRowStretch(0, 1)

        self.setLayout(self._layout)
