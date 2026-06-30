import qtawesome as qta
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QWidget,
)

from interface.gui.viewmodel.execute import ExecuteViewModel
from interface.gui.viewmodel.home_screen import HomeScreenViewModel


class Execute(QWidget):
    def __init__(
        self, home_view_model: HomeScreenViewModel, view_model: ExecuteViewModel
    ):
        super().__init__()
        self._home_view = home_view_model
        self._model = view_model

        self._home_view.changed_language.connect(self._retranslate)
        self._home_view.changed_theme.connect(self._retranslate)

        self._model.updated_fmt.connect(self._build_output_options)
        self._model.encoding_error.connect(self._show_error_pop_up)
        self._model.encoding_success.connect(self._show_success_pop_up)

        self._build()

    def _build(self):
        self._layout = QGridLayout()
        self._output_options = QListWidget()
        self._build_output_options()

        self._run_btn = QPushButton()
        self._run_btn.setText(self._home_view.t("ui.home.execute.run"))
        self._run_btn.setIcon(qta.icon("mdi6.motion-play"))
        self._run_btn.clicked.connect(self._execute)

        self._layout.addWidget(self._output_options, 0, 0, 2, 1)
        self._layout.addWidget(self._run_btn, 0, 1, 1, 1)

        self.setLayout(self._layout)

    def _build_output_options(self):
        self._output_options.clear()

        options = self._model.get_available_fmt()
        current = self._model.get_current_fmt()

        for opt in options:
            item = QListWidgetItem()
            widget = QCheckBox()

            widget.setText(opt.name)
            widget.setChecked(opt in current)
            widget.checkStateChanged.connect(lambda _, o=opt: self._model.toggle_fmt(o))

            item.setSizeHint(widget.sizeHint())

            self._output_options.addItem(item)
            self._output_options.setItemWidget(item, widget)

    def _retranslate(self):
        self._run_btn.setText(self._home_view.t("ui.home.execute.run"))

    def _execute(self):
        if len(self._model.get_current_fmt()) < 1:
            self._show_error_pop_up("NEED_OUTPUT_FORMAT_ERROR")
            return
        dialog = QFileDialog(self)
        dialog.setWindowTitle(self._home_view.t("ui.home.execute.out_dir"))
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setNameFilter(f"{self._home_view.t('ui.home.execute.filter')}")
        directory = dialog.getExistingDirectory()
        if directory:
            self._model.run(directory)

    def _show_error_pop_up(self, err: str):
        err_msg = self._home_view.t(f"pipeline.errors.{err}")
        err_title = self._home_view.t("pipeline.errors.title")

        msg_box = QMessageBox()
        msg_box.setWindowTitle(err_title)
        msg_box.setText(err_msg)
        msg_box.exec()

    def _show_success_pop_up(self):
        msg = self._home_view.t("pipeline.success")
        title = self._home_view.t("pipeline.title")
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(msg)
        msg_box.exec()
