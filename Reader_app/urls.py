from django.urls import path

from Reader_app.views import QrCreateView, QrRead

app_name = "Reader_app"

urlpatterns = [
    path("", QrCreateView.as_view(), name="qrcreate"),
    path("qrcode-read", QrRead.as_view(), name="qrread"),
]
