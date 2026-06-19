from django.urls import path

from Reader_app.views import (
    QrCreateView,
    QrScanPostView,
    QrLiveScanPageView,
    QrScanLiveView
)

app_name = "Reader_app"

urlpatterns = [
    path("", QrCreateView.as_view(), name="qrcreate"),
    path("qrcode-scan-post", QrScanPostView.as_view(), name="qrread"),
    path("qrcode-scan-live/", QrLiveScanPageView.as_view(), name="qrlivepage"),
    path("api/scan-live/", QrScanLiveView.as_view(), name="qrliveapi"),
]
