import base64
from io import BytesIO
import cv2

from django.http import HttpResponse
from django.views.generic import TemplateView
import secrets
import qrcode
from qrcode.image.svg import SvgImage
import numpy as np


class QrCreateView(TemplateView):
    template_name = "qr_create.html"

    def get_context_data(self, **kwargs):
        context = super(QrCreateView, self).get_context_data(**kwargs)

        token = secrets.token_urlsafe(16)
        generated_qrcode = self.get_qrcode_svg(token)
        context.update({"qrcode":generated_qrcode})
        return context

    @staticmethod
    def get_qrcode_svg(text: str) -> str:
        factory = SvgImage
        img = qrcode.make(text ,image_factory=factory, box_size=30)
        stream = BytesIO()
        img.save(stream)
        base64_image = base64.b64encode(stream.getvalue()).decode()
        return "data:image/svg+xml;utf8;base64," + base64_image


class QrRead(TemplateView):
    template_name = "qr_scan.html"

    def post(self, request):
        image_data_url = request.POST.get("image")

        if not image_data_url:
            return HttpResponse("No image provided")

        image_data = base64.b64decode(image_data_url.split(",")[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        data = self.qrcode_reader(img)

        if not data:
            return HttpResponse("No QR code found!")

        return HttpResponse(data)

    @staticmethod
    def qrcode_reader(img):
        detector = cv2.QRCodeDetector()

        data, points, _ = detector.detectAndDecode(img)

        if data:
            return data

        return False
