import os

from shared.constants import ImageConfig


class ImageListManager:
    _selected_images_paths: dict[int, str] = dict()
    _image_config = ImageConfig()

    def add_images_dir(self, d: str) -> int:
        if not os.path.exists(d) or not os.path.isdir(d):
            return 0
        files = os.listdir(d)
        count = 0
        for file in files:
            file_path = os.path.join(d, file)
            if self.add_image_path(file_path):
                count += 1

        return count

    def add_image_paths(self, paths: list[str]) -> int:
        count = 0
        for p in paths:
            if self.add_image_path(p):
                count += 1

        return count

    def add_image_path(self, p: str) -> bool:
        if not self._image_config.is_valid_path(p):
            return False

        if p in self._selected_images_paths.values():
            return False

        idx = len(self._selected_images_paths)
        self._selected_images_paths[idx] = p
        return True

    def remove_image_path(self, idx: int) -> bool:
        path = self._selected_images_paths.pop(idx, None)
        if path is None:
            return False

        return True

    def get_paths(self) -> dict[int, str]:
        return self._selected_images_paths

    def clear(self):
        self._selected_images_paths.clear()
