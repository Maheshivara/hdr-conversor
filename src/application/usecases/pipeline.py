from typing import Any

from application.dto.effects import EffectDTO
from application.dto.encoder import EncoderDTO
from application.errors.pipeline import PipelineError
from core.encoders.rgbm import RGBMEncoder
from core.filters.blacklevel_filter import BlackLevelFilter
from core.filters.exposure_filter import ExposureFilter
from core.filters.gamma_filter import GammaFilter
from core.filters.saturation_filter import SaturationFilter
from core.models.image import Image
from core.pipelines.image_pipeline import ImagePipeline
from infra.image_io.reader import ImageReader
from infra.image_io.writer import ImageWriter
from shared.constants import AvailableEffect, AvailableEncoders, AvailableOutputFormat


class PipelineUseCase:
    def __init__(self) -> None:
        self._pipeline = ImagePipeline()
        self._reader = ImageReader()
        self._writer = ImageWriter()
        self._encoder = RGBMEncoder()
        self._output_fmts: set[AvailableOutputFormat] = set()

    def add_fmt(self, new: AvailableOutputFormat):
        self._output_fmts.add(new)

    def remove_fmt(self, to_remove: AvailableOutputFormat):
        self._output_fmts.discard(to_remove)

    def toggle_fmt(self, fmt: AvailableOutputFormat):
        if fmt in self._output_fmts:
            self.remove_fmt(fmt)
        else:
            self.add_fmt(fmt)

    def get_output_fmt(self) -> list[AvailableOutputFormat]:
        return list(self._output_fmts)

    def get_available_fmt(self) -> list[AvailableOutputFormat]:
        return [AvailableOutputFormat.DDS, AvailableOutputFormat.PNG]

    def set_encoder(self, encoder: AvailableEncoders) -> PipelineError | None:
        e = None
        match encoder:
            # case AvailableEncoders.RGBE:
            #   e = DefaultEncoder()
            # case AvailableEncoders.LOG_LUV:
            #    e = DefaultEncoder()
            case AvailableEncoders.RGBM:
                e = RGBMEncoder()
        if e is None:
            return PipelineError.INVALID_ENCODER_ERROR

        self._encoder = e
        return None

    def get_available_encoders(self) -> list[AvailableEncoders]:
        return [
            # AvailableEncoders.RGBE,
            # AvailableEncoders.LOG_LUV,
            AvailableEncoders.RGBM,
        ]

    def get_available_effects(self) -> list[AvailableEffect]:
        return [
            AvailableEffect.BLACK_LEVEL,
            AvailableEffect.EXPOSURE,
            AvailableEffect.GAMMA,
            AvailableEffect.SATURATION,
        ]

    def add_effect(self, t: AvailableEffect) -> PipelineError | None:
        f = None
        match t:
            case AvailableEffect.BLACK_LEVEL:
                f = BlackLevelFilter()
            case AvailableEffect.SATURATION:
                f = SaturationFilter()
            case AvailableEffect.GAMMA:
                f = GammaFilter()
            case AvailableEffect.EXPOSURE:
                f = ExposureFilter()

        if f is None:
            return PipelineError.EFFECT_NOT_FOUND_ERROR

        self._pipeline.add_stage(f)

        return None

    def remove_effect(self, idx: int) -> PipelineError | None:
        removed = self._pipeline.remove_stage(idx)

        if not removed:
            return PipelineError.REMOVE_EFFECT_ERROR

        return None

    def get_effects(self) -> tuple[dict[int, EffectDTO], PipelineError | None]:
        effects = self._pipeline.get_all_stages()

        dtos: dict[int, EffectDTO] = dict()

        for k, f in effects.items():
            dto = EffectDTO.from_filter(f)
            if dto is None:
                return (dict(), PipelineError.INVALID_EFFECT)
            dtos[k] = dto
        return (dtos, None)

    def move_effect(self, idx: int, new_pos: int):
        self.move_effect(idx, new_pos)

    def swap_effects(self, idx_1: int, idx_2: int) -> PipelineError | None:
        swapped = self._pipeline.swap_stages(idx_1, idx_2)

        if not swapped:
            return PipelineError.COULD_NOT_SWAP_ERROR

        return None

    def update_effect_input(
        self, idx: int, input: str, new_value: Any
    ) -> PipelineError | None:
        effects = self._pipeline.get_all_stages()

        effect = effects.get(idx, None)
        if effect is None:
            return PipelineError.EFFECT_NOT_FOUND_ERROR

        inputs = effect.get_params()
        i = inputs.get(input, None)
        if i is None:
            return PipelineError.EFFECT_INPUT_NOT_FOUND_ERROR

        updated = i.update_value(new_value)
        if not updated:
            return PipelineError.INVALID_INPUT_VALUE_ERROR

    def execute(self, image_path: str, output_dir: str) -> PipelineError | None:
        if len(self._output_fmts) < 1:
            return PipelineError.NEED_OUTPUT_FORMAT_ERROR

        image = self._reader.from_file(image_path)
        if image is None:
            return PipelineError.READ_IMAGE_ERROR

        res = self._pipeline.run(image)

        res = self._encoder.encode(res)

        for fmt in self._output_fmts:
            written = self._write_image(res, fmt, output_dir)

            if not written:
                return PipelineError.FAIL_TO_WRITE_ERROR

        return None

    def _write_image(
        self, img: Image, fmt: AvailableOutputFormat, out_dir: str
    ) -> bool:
        written = False
        match fmt:
            case AvailableOutputFormat.PNG:
                written = self._writer.to_png(img, out_dir)
            case AvailableOutputFormat.DDS:
                written = self._writer.to_dds(img, out_dir)

        return written

    def get_encoder(self) -> EncoderDTO | None:
        return EncoderDTO.from_encoder(self._encoder)

    def update_encoder_input(self, input: str, new_value: Any) -> PipelineError | None:
        updated = self._encoder.update_input_value(input, new_value)

        if not updated:
            return PipelineError.INVALID_INPUT_VALUE_ERROR

        return None
