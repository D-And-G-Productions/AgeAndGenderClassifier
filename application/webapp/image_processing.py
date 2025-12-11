from io import BytesIO

import numpy as np
from PIL import Image


class ImageProcessing:
    @staticmethod
    async def imageBytesToArray(imageBytes):
        """
        Convert image bytes to expected numpy array for inference.
        """
        image = ImageProcessing._imageBytesTo128By128Image(imageBytes)
        array = ImageProcessing.imageToNumpyArray(image)
        return array

    @staticmethod
    def _imageBytesTo128By128Image(imgBytes):
        bytesIO = BytesIO(imgBytes)
        image = Image.open(bytesIO)
        return image.convert("RGB").resize((128, 128))

    @staticmethod
    def imageToNumpyArray(image):
        array = np.asarray(image, dtype=np.float32)
        array = ImageProcessing._normaliseRGB(array)
        array = ImageProcessing._addBatchDimension(array)
        return array

    @staticmethod
    def _normaliseRGB(array):
        return array / 255

    @staticmethod
    def _addBatchDimension(array):
        return array[None, ...]
