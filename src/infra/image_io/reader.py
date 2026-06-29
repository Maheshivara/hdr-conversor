import cv2
from openexr_numpy import imread

from core.models.image import Image, ImageOriginalExtension


class ImageReader:
    def from_file(self, file_path: str) -> Image | None:
        file_ext = file_path.split(".")[-1].strip().lower()

        match file_ext:
            case "exr":
                return self._from_exr(file_path)
            case "hdr":
                return self._from_hdr(file_path)

        return None

    def _from_exr(self, image_path: str) -> Image | None:
        try:
            exr_image = imread(image_path)
            exr_image = exr_image.clip(0, None)

            image = Image(
                ImageOriginalExtension.EXR, data=exr_image, file_path=image_path
            )

            return image

        except Exception:
            return None

    def _from_hdr(self, image_path: str) -> Image | None:
        try:
            hdr_image = cv2.imread(image_path, cv2.IMREAD_ANYDEPTH | cv2.IMREAD_COLOR)
            if hdr_image is None:
                return None

            hdr_image = cv2.cvtColor(hdr_image, cv2.COLOR_BGR2RGB)
            hdr_image = hdr_image.clip(0, None)
            image = Image(
                ImageOriginalExtension.HDR, data=hdr_image, file_path=image_path
            )

            return image

        except Exception:
            return None
