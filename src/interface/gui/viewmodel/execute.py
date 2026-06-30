from PySide6.QtCore import QObject, Signal

from interface.gui.model.image_list import ImageListModel
from interface.gui.model.pipeline import PipelineModel
from shared.constants import AvailableOutputFormat


class ExecuteViewModel(QObject):
    encoding_started = Signal()
    encoding_success = Signal()
    encoding_error = Signal(str)
    encoding_processing = Signal(tuple)

    updated_fmt = Signal()

    def __init__(self, pipeline_model: PipelineModel, image_list_model: ImageListModel):
        super().__init__()
        self._pipeline = pipeline_model
        self._image_list = image_list_model

        self._pipeline.pipeline_processing.connect(self.encoding_processing)
        self._pipeline.pipeline_started.connect(self.encoding_started)
        self._pipeline.pipeline_error.connect(self.encoding_error)
        self._pipeline.pipeline_success.connect(self.encoding_success)
        self._pipeline.fmt_updated.connect(self.updated_fmt)

    def run(self, output_dir: str):
        paths = list(self._image_list.get_list().values())
        self._pipeline.execute(paths, output_dir)

    def toggle_fmt(self, fmt: AvailableOutputFormat):
        self._pipeline.toggle_fmt(fmt)

    def get_available_fmt(self):
        return self._pipeline.get_available_fmt()

    def get_current_fmt(self):
        return self._pipeline.get_fmt()
