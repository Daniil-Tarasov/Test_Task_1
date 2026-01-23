from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from electronics.models import ElectronicsNetwork
from electronics.serializers import (
    ElectronicsNetworkCreateSerializer,
    ElectronicsNetworkSerializer,
    ElectronicsNetworkUpdateSerializer,
)


class ElectronicsNetworkCreateAPIView(generics.CreateAPIView):
    serializer_class = ElectronicsNetworkCreateSerializer


class ElectronicsNetworkListAPIView(generics.ListAPIView):
    queryset = ElectronicsNetwork.objects.all()
    serializer_class = ElectronicsNetworkSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["contacts__country"]
    ordering_fields = ["contacts__country"]


class ElectronicsNetworkRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ElectronicsNetwork.objects.all()
    serializer_class = ElectronicsNetworkSerializer


class ElectronicsNetworkUpdateAPIView(generics.UpdateAPIView):
    queryset = ElectronicsNetwork.objects.all()
    serializer_class = ElectronicsNetworkUpdateSerializer


class ElectronicsNetworkDestroyAPIView(generics.DestroyAPIView):
    queryset = ElectronicsNetwork.objects.all()
