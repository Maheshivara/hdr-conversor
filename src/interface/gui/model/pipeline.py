from typing import Any

from PySide6.QtCore import QObject, Signal

from application.usecases.pipeline import PipelineUseCase
from shared.constants import AvailableEffect, AvailableEncoders, AvailableOutputFormat


class PipelineModel(QObject):
    _pipeline = PipelineUseCase()

    effects_updated = Signal()
    encoder_updated = Signal()

    effect_update_error = Signal(str)
    encoder_update_error = Signal(str)

    pipeline_started = Signal()
    pipeline_processing = Signal(tuple[int, int])
    pipeline_error = Signal(str)
    pipeline_success = Signal()

    def __init__(self) -> None:
        super().__init__()

    def get_effects(self):
        return self._pipeline.get_effects()

    def add_effect(self, t: AvailableEffect):
        err = self._pipeline.add_effect(t)
        if err is not None:
            self.effect_update_error.emit(err.name)
            return

        self.effects_updated.emit()

    def remove_effect(self, idx: int):
        err = self._pipeline.remove_effect(idx)
        if err is not None:
            self.effect_update_error.emit(err.name)
            return

        self.effects_updated.emit()

    def set_encoder(self, ecd: AvailableEncoders):
        err = self._pipeline.set_encoder(ecd)

        if err is not None:
            self.encoder_update_error.emit(err.name)
            return

        self.encoder_updated.emit()

    def update_effect_input(self, idx: int, input: str, new_value: Any):
        err = self._pipeline.update_effect_input(idx, input, new_value)

        if err is not None:
            self.effect_update_error.emit(err.name)

        self.effects_updated.emit()

    def update_encoder_input(self, input: str, new_value: Any):
        err = self._pipeline.update_encoder_input(input, new_value)

        if err is not None:
            self.encoder_update_error.emit(err.name)

        self.encoder_update_error.emit()

    def get_encoder(self):
        return self._pipeline.get_encoder()

    def get_encoders(self):
        return self._pipeline.get_available_encoders()

    def get_available_effects(self):
        return self._pipeline.get_available_effects()

    def execute(
        self, image_paths: list[str], formats: list[AvailableOutputFormat], out_dir: str
    ):
        self.pipeline_started.emit()
        total = len(image_paths)
        for i, path in enumerate(image_paths):
            self.pipeline_processing.emit((i, total))
            err = self._pipeline.execute(path, formats, out_dir)
            if err is not None:
                self.pipeline_error.emit(err.name)

        self.pipeline_success.emit()
