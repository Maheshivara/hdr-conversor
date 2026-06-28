from enum import Enum, auto


class PipelineError(Enum):
    REMOVE_EFFECT_ERROR = auto()
    READ_IMAGE_ERROR = auto()
    INVALID_EFFECT = auto()
    COULD_NOT_SWAP_ERROR = auto()
    EFFECT_NOT_FOUND_ERROR = auto()
    EFFECT_INPUT_NOT_FOUND_ERROR = auto()
    INVALID_INPUT_VALUE_ERROR = auto()
    INVALID_ENCODER_ERROR = auto()
    FAIL_TO_WRITE_ERROR = auto()
