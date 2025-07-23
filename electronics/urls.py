from django.urls import path

from electronics.apps import ElectronicsConfig
from electronics.views import (
    ElectronicsNetworkCreateAPIView,
    ElectronicsNetworkDestroyAPIView,
    ElectronicsNetworkListAPIView,
    ElectronicsNetworkRetrieveAPIView,
    ElectronicsNetworkUpdateAPIView,
)

app_name = ElectronicsConfig.name

urlpatterns = [
    path(
        "electronicsnetwork/create/",
        ElectronicsNetworkCreateAPIView.as_view(),
        name="electronicsnetwork-create",
    ),
    path(
        "electronicsnetwork/",
        ElectronicsNetworkListAPIView.as_view(),
        name="electronicsnetwork-list",
    ),
    path(
        "electronicsnetwork/<int:pk>/",
        ElectronicsNetworkRetrieveAPIView.as_view(),
        name="electronicsnetwork-detail",
    ),
    path(
        "electronicsnetwork/<int:pk>/update/",
        ElectronicsNetworkUpdateAPIView.as_view(),
        name="electronicsnetwork-update",
    ),
    path(
        "electronicsnetwork/<int:pk>/destroy/",
        ElectronicsNetworkDestroyAPIView.as_view(),
        name="electronicsnetwork-destroy",
    ),
]
