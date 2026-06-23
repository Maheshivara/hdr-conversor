from core.models.enum.effects import EffectType
from core.models.input import Input


class Workflow:
    def __init__(self, name: str, steps: list[tuple[EffectType, dict[str, Input]]]):
        self.steps = steps

    def add_step(self, step: tuple[EffectType, dict[str, Input]]):
        self.steps.append(step)

    def remove_step(self, step_idx: int):
        self.steps.pop(step_idx)
