import base64
import binascii
from io import BytesIO

import cairosvg
import cv2
import numpy as np
import qrcode
from qrcode.image.svg import SvgImage
from qreader import QReader


class QReaderSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = QReader()

        return cls._instance


class QRService:

    @staticmethod
    def base64_to_cv2(image_data_url: str):
        try:
            header, payload = image_data_url.split(",")
        except AttributeError:
            raise ValueError("Invalid input data")

        image_data = base64.b64decode(payload, validate=True)

        if header.startswith("data:image/svg+xml"):
            image_data = cairosvg.svg2png(
                bytestring=image_data,
                background_color="white"
            )
        elif not header.startswith("data:image/png"):
            raise ValueError("Invalid input data")

        np_arr = np.frombuffer(image_data, np.uint8)
        cv2_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if cv2_img is None:
            raise ValueError("Unsupported or corrupted image")

        return cv2_img

    @staticmethod
    def decode_cv2(img: np.ndarray) -> str | None:
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)
        return data if data else None

    @staticmethod
    def decode_qreader(img: np.ndarray) -> str | None:
        qreader = QReaderSingleton()
        data = qreader.detect_and_decode(image=img)
        return data if data else None

    @classmethod
    def decode_best(cls, image_data_url: str) -> tuple[str,str] | None:
        """
        Method converts input base64 string into CV2 image and tries to decode with OpenCV at first and then with QReader.
        It returns a tuple (decoded_data: str, decoding_method: str) or None if data not found.
        """
        cv2_img = cls.base64_to_cv2(image_data_url)
        decoded_data = cls.decode_cv2(cv2_img)
        if decoded_data is not None:
            return decoded_data, "CV2"
        decoded_data = cls.decode_qreader(cv2_img)
        if decoded_data is not None:
            return decoded_data, "QReader"
        return None

    @staticmethod
    def get_qrcode_svg(text: str) -> str:
        """Returns base64 string of the generated .svg image"""
        factory = SvgImage
        img = qrcode.make(text ,image_factory=factory, box_size=30)
        stream = BytesIO()
        img.save(stream)
        base64_image = base64.b64encode(stream.getvalue()).decode()
        return "data:image/svg+xml;utf8;base64," + base64_image