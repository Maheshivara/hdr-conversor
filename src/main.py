import os
import time

import numpy as np
import cv2 as cv
from wand.image import Image

from encoders.rgbm import RGBMEncoder
from readers.exr import EXRReader
from readers.hdr import HDRReader

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)

    hdr_reader = HDRReader()
    exr_reader = EXRReader()
    rgbm_encoder = RGBMEncoder(8.0)

    input_list = os.listdir(INPUT_DIR)
    filenames = [
        f
        for f in input_list
        if os.path.isfile(os.path.join(INPUT_DIR, f))
        and f.lower().endswith((".hdr", ".exr"))
    ]

    for filename in filenames:
        start_time = time.time()

        if filename.lower().endswith(".hdr"):
            filepath = os.path.join(INPUT_DIR, filename)
            data = hdr_reader.read(filepath)
            if data is None:
                print(f"Failed to read HDR image: {filepath}")
                continue

            rgbm_image = rgbm_encoder.from_hdr(data) * 255

            output_filename = f"{os.path.splitext(filename)[0]}_hdr_to_rgbm.png"
            output_filepath = os.path.join(OUTPUT_DIR, output_filename)
            cv.imwrite(output_filepath, (rgbm_image).astype(np.uint8))

            with Image(filename=output_filepath) as img:
                dds_filename = f"{os.path.splitext(filename)[0]}_hdr_to_rgbm.dds"
                dds_output_filepath = os.path.join(OUTPUT_DIR, dds_filename)
                img.compression = "dxt5"
                img.save(filename=dds_output_filepath)

        elif filename.lower().endswith(".exr"):

            filepath = os.path.join(INPUT_DIR, filename)
            data = exr_reader.read(filepath)
            if data is None:
                print(f"Failed to read EXR image: {filepath}")
                continue

            rgbm_image = rgbm_encoder.from_exr(data) * 255

            output_filename = f"{os.path.splitext(filename)[0]}_exr_to_rgbm.png"
            output_filepath = os.path.join(OUTPUT_DIR, output_filename)
            cv.imwrite(output_filepath, (rgbm_image).astype(np.uint8))

            with Image(filename=output_filepath) as img:
                dds_filename = f"{os.path.splitext(filename)[0]}_exr_to_rgbm.dds"
                dds_output_filepath = os.path.join(OUTPUT_DIR, dds_filename)
                img.compression = "dxt5"
                img.save(filename=dds_output_filepath)

        end_time = time.time()

        print(f"Processed {filename} in {end_time - start_time:.2f} seconds.")


if __name__ == "__main__":
    main()
