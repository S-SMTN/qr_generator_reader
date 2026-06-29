from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from django.views.generic import TemplateView
import secrets

from Reader_app.services.qr_service import QRService


class QrCreateView(TemplateView):
    template_name = "qr_create.html"

    def get_context_data(self, **kwargs):
        context = super(QrCreateView, self).get_context_data(**kwargs)

        token = secrets.token_urlsafe(16)
        generated_qrcode = QRService.get_qrcode_svg(token)
        context.update({"qrcode":generated_qrcode})
        return context


class QrScanPostView(TemplateView):
    template_name = "qr_scan.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        image_data_url = request.POST.get("image")

        if not image_data_url:
            return HttpResponse("No image provided")

        try:
            data = QRService.decode_best(image_data_url)
        except ValueError as e:
            return HttpResponse(str(e))

        if not data:
            return HttpResponse("No QR code found!")

        return HttpResponse(f"QR-decoded data: {data[0]}, decoded with {data[1]}")


class QrLiveScanPageView(TemplateView):
    template_name = "qr_live_scan.html"


class QrScanLiveView(View):

    def post(self, request: HttpRequest) -> JsonResponse:
        image_data_url = request.POST.get("image")

        if not image_data_url:
            return JsonResponse({
                "success": False,
                "error": "No image provided"
            }, status=400)

        try:
            data = QRService.decode_best(image_data_url)
        except ValueError:
            return JsonResponse({
                "success": False,
                "found": False
            })

        if not data:
            return JsonResponse({
                "success": True,
                "found": False
            })

        return JsonResponse({
            "success": True,
            "found": True,
            "data": f"QR-decoded data: {data[0]}, decoded with {data[1]}"
        })
