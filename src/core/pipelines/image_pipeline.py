from core.filters.image_filter import ImageFilter
from core.models.image import Image


class ImagePipeline:
    def __init__(self):
        self._stages: dict[int, ImageFilter] = {}

    def add_stage(self, stage: ImageFilter):
        index = len(self._stages)
        self._stages[index] = stage

    def get_stage(self, idx: int) -> ImageFilter | None:
        return self._stages.get(idx)

    def get_all_stages(self) -> dict[int, ImageFilter]:
        return self._stages

    def remove_stage(self, idx: int):
        stage = self._stages.get(idx)
        if stage is None:
            return

        self._stages.pop(idx)

    def move_stage(self, init_idx: int, target_idx: int):
        if init_idx == target_idx:
            return

        if init_idx not in self._stages:
            return

        ordered_keys = sorted(self._stages.keys())
        stages = [self._stages[k] for k in ordered_keys]

        try:
            source_pos = ordered_keys.index(init_idx)
        except ValueError:
            return

        n = len(stages)
        if target_idx in ordered_keys:
            target_pos = ordered_keys.index(target_idx)
        else:
            if target_idx < 0:
                target_pos = 0
            elif target_idx >= n:
                target_pos = n
            else:
                target_pos = target_idx

        stage = stages.pop(source_pos)

        if source_pos < target_pos:
            target_pos -= 1

        stages.insert(target_pos, stage)

        self._stages.clear()
        for i, s in enumerate(stages):
            self._stages[i] = s

    def swap_stages(self, idx_1: int, idx_2: int):
        stage_one = self._stages.get(idx_1)
        stage_two = self._stages.get(idx_2)

        if stage_one is None or stage_two is None:
            return
        self._stages[idx_1] = stage_two
        self._stages[idx_2] = stage_one

    def run(self, image: Image) -> Image:
        ordered_index = sorted(self._stages.keys())

        result = image
        for i in ordered_index:
            filter = self._stages.get(i)
            if filter:
                result = filter.apply(result)

        return result
