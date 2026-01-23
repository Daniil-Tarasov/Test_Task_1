from rest_framework import serializers

from electronics.models import Contact, ElectronicsNetwork, Product


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ElectronicsNetworkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicsNetwork
        exclude = ("created_at",)


class ElectronicsNetworkSerializer(serializers.ModelSerializer):
    hierarchy_level = serializers.ReadOnlyField()
    contacts = ContactSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.HyperlinkedRelatedField(
        view_name="electronics:electronicsnetwork-detail",
        queryset=ElectronicsNetwork.objects.all(),
        allow_null=True,
    )

    class Meta:
        model = ElectronicsNetwork
        fields = "__all__"


class ElectronicsNetworkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectronicsNetwork
        fields = "__all__"
        read_only_fields = ("created_at", "debt_to_supplier")
