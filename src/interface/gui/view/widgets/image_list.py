from typing import Optional

import qtawesome as qta
from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QWidget,
)

from interface.gui.viewmodel.image_list import ImageListViewModel
from shared.constants import ImageConfig


class ImageList(QWidget):
    def __init__(
        self, view_model: ImageListViewModel, parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._view_model = view_model

        self._view_model.changed_language.connect(self._retranslate)
        self._view_model.changed_theme.connect(self._retranslate)
        self._view_model.list_updated.connect(self._build_list_items)
        allowed_files: list[str] = []
        for ext in ImageConfig.VALID_EXTENSIONS:
            allowed_files.append(f"*{ext}")
        self._file_selector = " ".join(allowed_files)
        self._build()

    def _build(self):
        self._layout = QGridLayout()

        self._label = QLabel()
        self._label.setText(self._view_model.t("ui.home.path_list.label"))
        self._list_widget = QListWidget(self)
        self._build_list_items()

        self._add_images_btn = QPushButton()
        self._add_images_btn.setText(self._view_model.t("ui.home.path_list.add_images"))
        self._add_images_btn.setIcon(qta.icon("fa6.images"))
        self._add_images_btn.clicked.connect(self._add_images_clicked)

        self._add_images_dir_btn = QPushButton()
        self._add_images_dir_btn.setText(
            self._view_model.t("ui.home.path_list.add_dir")
        )
        self._add_images_dir_btn.setIcon(qta.icon("fa6.folder-closed"))
        self._add_images_dir_btn.clicked.connect(self._add_dir_clicked)

        self._layout.addWidget(self._label, 0, 0, 1, 2)
        self._layout.addWidget(self._list_widget, 1, 0, 9, 2)
        self._layout.addWidget(self._add_images_btn, 10, 0, 1, 1)
        self._layout.addWidget(self._add_images_dir_btn, 10, 1, 1, 1)
        self.setLayout(self._layout)

    def _build_list_items(self):
        list = self._view_model.get_list()
        self._list_widget.clear()
        for idx, path in list.items():
            item = QListWidgetItem()
            item_widget = QWidget()

            line_text = QLabel(self._transform_path(path))
            line_push_button = QPushButton()
            icon = qta.icon("fa6.trash-can")
            line_push_button.setIcon(icon)

            item_layout = QHBoxLayout()
            item_layout.addWidget(line_text)
            item_layout.addWidget(line_push_button)

            line_push_button.clicked.connect(
                lambda _, i=idx: self._view_model.remove_element(i)
            )
            item_widget.setLayout(item_layout)
            item.setSizeHint(item_widget.sizeHint())
            self._list_widget.addItem(item)
            self._list_widget.setItemWidget(item, item_widget)

    def _transform_path(self, path: str) -> str:
        if len(path) <= 50:
            return path

        return f"...{path[-47:]}"

    def _add_images_clicked(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle(self._view_model.t("ui.home.path_list.add_image_dialog"))
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter(
            f"{self._view_model.t('ui.home.path_list.image_files')} {self._file_selector}"
        )
        if dialog.exec():
            selected_files = dialog.selectedFiles()
            self._view_model.add_images(selected_files)

    def _add_dir_clicked(self):
        dialog = QFileDialog(self)
        dialog.setWindowTitle(self._view_model.t("ui.home.path_list.add_dir_dialog"))
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setNameFilter(f"{self._view_model.t('ui.home.path_list.image_dir')}")
        directory = dialog.getExistingDirectory()
        if directory:
            self._view_model.add_dir(directory)

    def _retranslate(self):
        self._label.setText(self._view_model.t("ui.home.path_list.label"))
        self._add_images_dir_btn.setText(
            self._view_model.t("ui.home.path_list.add_dir")
        )
        self._add_images_btn.setText(self._view_model.t("ui.home.path_list.add_images"))
