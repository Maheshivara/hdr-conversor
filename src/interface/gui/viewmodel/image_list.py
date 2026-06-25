from typing import Optional

from PySide6.QtCore import QObject, Signal

from interface.gui.model.image_list import ImageListModel
from interface.gui.viewmodel.home_screen import HomeScreenViewModel


class ImageListViewModel(QObject):
    changed_theme = Signal()
    changed_language = Signal()
    list_updated = Signal()

    def __init__(
        self,
        home_view_model: HomeScreenViewModel,
        list_model: ImageListModel,
        parent: Optional[QObject] = None,
    ) -> None:
        super().__init__(parent)
        self._model = list_model
        self._home_view_model = home_view_model

        self._home_view_model.changed_language.connect(self.changed_language)
        self._home_view_model.changed_theme.connect(self.changed_theme)
        self._model.list_updated.connect(self.list_updated)

    def get_list(self) -> dict[int, str]:
        return self._model.get_list()

    def remove_element(self, idx: int):
        self._model.remove_item(idx)

    def add_images(self, paths: list[str]):
        self._model.add_items(paths)

    def add_dir(self, dir: str):
        self._model.add_dir(dir)

    def clear_list(self):
        self._model.clear()

    def t(self, key: str) -> str:
        return self._home_view_model.t(key)
