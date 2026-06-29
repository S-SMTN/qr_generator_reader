import base64
import binascii
from io import BytesIO

import cv2
import numpy as np
import qrcode
from qrcode.image.svg import SvgImage
from qreader import QReader


class QRService:

    @staticmethod
    def base64_to_cv2(image_data_url: str):
        try:
            image_data = base64.b64decode(image_data_url.split(",")[1])
        except (IndexError, binascii.Error):
            raise ValueError("Invalid input data")
        np_arr = np.frombuffer(image_data, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    @staticmethod
    def decode_cv2(img: np.ndarray) -> str | None:
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)
        return data + " decoded with CV2" if data else None

    @staticmethod
    def decode_qreader(img: np.ndarray) -> str | None:
        qreader = QReader()
        result = qreader.detect_and_decode(image=img)
        return result + " decoded with QReader" if result else None

    @classmethod
    def decode_best(cls, image_data_url: str) -> str | None:
        img = cls.base64_to_cv2(image_data_url)
        return (
            cls.decode_cv2(img)
            or cls.decode_qreader(img)
        )

    @staticmethod
    def get_qrcode_svg(text: str) -> str:
        factory = SvgImage
        img = qrcode.make(text ,image_factory=factory, box_size=30)
        stream = BytesIO()
        img.save(stream)
        base64_image = base64.b64encode(stream.getvalue()).decode()
        return "data:image/svg+xml;utf8;base64," + base64_image