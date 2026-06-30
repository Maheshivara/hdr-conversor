import time
from os import path

import cv2
from PIL import Image as PImage

from core.models.image import Image


class ImageWriter:
    def to_png(self, image: Image, out_dir: str) -> bool:
        out_path = path.join(out_dir, self._create_image_name(image.file_path, "png"))
        try:
            # Normalize float32 to uint8 (0-255 range)
            normalized = cv2.normalize(
                image.data, image.data, 0, 255, cv2.NORM_MINMAX
            ).astype("uint8")

            return cv2.imwrite(out_path, normalized, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        except Exception:
            return False

    def to_dds(self, image: Image, out_dir: str) -> bool:
        out_path = path.join(out_dir, self._create_image_name(image.file_path, "dds"))
        try:
            # Normalize to 0-255 for DDS
            normalized = cv2.normalize(
                image.data, image.data, 0, 255, cv2.NORM_MINMAX
            ).astype("uint8")

            p_img = PImage.fromarray(normalized)
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
