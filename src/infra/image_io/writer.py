import time
from os import path

import cv2
import numpy as np
from PIL import Image as PImage

from core.models.image import Image


class ImageWriter:
    def to_png(self, image: Image, out_dir: str) -> bool:
        normalized_data = np.zeros_like(image.data)
        cv2.normalize(image.data, normalized_data, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        out_path = path.join(out_dir, self._create_image_name(image.file_path, "png"))

        return cv2.imwrite(out_path, normalized_data)

    def to_dds(self, image: Image, out_dir: str) -> bool:
        normalized_data = np.zeros_like(image.data)
        cv2.normalize(image.data, normalized_data, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

        out_path = path.join(out_dir, self._create_image_name(image.file_path, "dds"))
        try:
            p_img = PImage.fromarray(normalized_data)
            del normalized_data
            p_img.save(out_path, pixel_format="DXT5")

            return True

        except Exception:
            return False

    def _create_image_name(self, original_path: str, ext: str) -> str:
        base_name = path.basename(original_path)

        original_name = base_name.rsplit(".", 1)[0]
        timestamp = time.strftime("%Y%m%dT%H%M%S")
        new_name = f"{timestamp}_{original_name}.{ext}"

        return new_name
