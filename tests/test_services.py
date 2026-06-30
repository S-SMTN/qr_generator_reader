from Reader_app.services.qr_service import QReaderSingleton, QRService

from unittest import TestCase


QREADER_BASE = QReaderSingleton()


class QReaderSingletonTest(TestCase):
    def test_QReaderSingleton_is_singleton(self):
        qreader_second = QReaderSingleton()
        self.assertEqual(id(QREADER_BASE), id(qreader_second))
        self.assertTrue(QREADER_BASE is qreader_second)


class QRServiceTest(TestCase):
    def setUp(self):
        self.data = "test data to decode and encode"
        self.base64_image = QRService.get_qrcode_svg(self.data)
        self.cv2_img = QRService.base64_to_cv2(self.base64_image)

    def test_generate_and_decode_in_full(self):
        decoded = QRService.decode_best(self.base64_image)

        self.assertEqual(self.data, decoded[0])

    def test_get_qrcode_svg_returns_base64_str(self):
        self.assertTrue(self.base64_image.startswith("data:image/svg+xml;utf8;base64,"))
        self.assertEqual(len(self.base64_image.split(",")), 2)

    def test_decode_cv2_decodes(self):
        decoded = QRService.decode_cv2(self.cv2_img)

        self.assertEqual(self.data, decoded)

    def test_decode_qreader_decodes(self):
        decoded = QRService.decode_qreader(self.cv2_img)

        self.assertEqual(self.data, decoded)

    def test_base64_to_cv2_raises_errors(self):
        with self.assertRaises(ValueError):
            QRService.base64_to_cv2(123)

        with self.assertRaises(ValueError):
            QRService.base64_to_cv2("FOO,")

        with self.assertRaises(ValueError):
            QRService.base64_to_cv2("data:image/png;base64,@@@")

