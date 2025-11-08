# HDR Converter

## Description
This is a basic application that uses the libraries [OpenCV](https://pypi.org/project/opencv-python/) and [OpenEXR](https://pypi.org/project/OpenEXR/) to convert HDR images (`.hdr` and `.exr`) to RGBM, following the steps described [here](https://graphicrants.blogspot.com/2009/04/rgbm-color-encoding.html) by Brian Karis.

The application was developed as part of the *Digital Processing of Images and Signals* course during the 2025.2 term at the *Instituto Federal de Alagoas (IFAL) - Campus Arapiraca*, taught by Professor **Edvonaldo Horácio dos Santos, M.Sc.**

The group of contributors:
- [Humberto Augusto](https://github.com/Humberto0003)
- [José Bezerra](https://github.com/JBPinheiro86)
- [Luis Gabriel](https://github.com/Maheshivara)
- [Wallace Souza](https://github.com/RochaSWallace)

## How to Run
> [!IMPORTANT]  
> This project uses [uv](https://docs.astral.sh/uv/) as its package manager. All steps described below assume that you have it installed and configured.

> [!IMPORTANT]  
> You will also need Python version **3.14** (or later). You can install it with the command:
> ```sh
> uv python install 3.14
> ```

1. Clone this repository to your desired location.  
2. Inside the cloned repository directory, synchronize the project dependencies with:
    ```sh
    uv sync
    ```
3. Start the UI with:
    ```sh
    uv run src/main.py
    ```
