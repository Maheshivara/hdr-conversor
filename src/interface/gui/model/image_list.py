from PySide6.QtCore import QObject, Signal

from interface.gui.model.image_list_manager import ImageListManager


class ImageListModel(QObject):
    list_updated = Signal()
    _list_manager = ImageListManager()

    def __init__(self) -> None:
        super().__init__()

    def remove_item(self, idx: int):
        result = self._list_manager.remove_image_path(idx)
        if result:
            self.list_updated.emit()

    def add_items(self, paths: list[str]):
        result = self._list_manager.add_image_paths(paths)
        if result > 0:
            self.list_updated.emit()

    def add_dir(self, dir: str):
        result = self._list_manager.add_images_dir(dir)
        if result > 0:
            self.list_updated.emit()

    def get_list(self) -> dict[int, str]:
        return self._list_manager.get_paths()

    def clear(self):
        self._list_manager.clear()
        self.list_updated.emit()
