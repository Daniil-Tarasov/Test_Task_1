from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from electronics.models import Contact, ElectronicsNetwork, Product
from users.models import User


class ElectronicsNetworkModelTest(TestCase):

    def setUp(self):
        self.network_0 = ElectronicsNetwork.objects.create(name="Завод", debt_to_supplier=0)
        self.network_1 = ElectronicsNetwork.objects.create(
            name="Первый уровень", debt_to_supplier=0, supplier=self.network_0
        )
        self.network_2 = ElectronicsNetwork.objects.create(
            name="Второй уровень", debt_to_supplier=0, supplier=self.network_1
        )

    def test_hierarchy_level_property(self):
        self.assertEqual(self.network_0.hierarchy_level, 0)
        self.assertEqual(self.network_1.hierarchy_level, 1)
        self.assertEqual(self.network_2.hierarchy_level, 2)

    def test_supplier_cannot_be_self(self):
        self.network_0.supplier = self.network_0
        with self.assertRaises(ValidationError) as cm:
            self.network_0.clean()
        self.assertIn("Поставщик не может быть самим собой", cm.exception.message_dict["supplier"][0])

    def test_cycle_detection(self):
        self.network_0.supplier = self.network_2
        self.network_0.save()
        with self.assertRaises(ValidationError) as cm:
            self.network_1.supplier = self.network_0
            self.network_1.clean()
        self.assertIn("Обнаружен цикл в цепочке поставщиков", cm.exception.message_dict["supplier"][0])

    def test_valid_structure_does_not_raise(self):
        try:
            self.network_2.clean()
        except ValidationError:
            self.fail("clean() вызвал ValidationError для валидной структуры")


class ElectronicsNetworkAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="test")
        self.contact = Contact.objects.create(
            email="contact@example.com", country="Россия", city="Москва", street="Ленина", house_number="10"
        )
        self.product = Product.objects.create(name="Smartphone", model="X100", released_at="2023-01-01")

        self.network = ElectronicsNetwork.objects.create(name="Test Network", debt_to_supplier=0)
        self.network.contacts.add(self.contact)
        self.network.products.add(self.product)

        self.client.force_authenticate(user=self.user)

    def test_list_networks(self):
        url = reverse("electronics:electronicsnetwork-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_network(self):
        url = reverse("electronics:electronicsnetwork-detail", args=[self.network.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.network.name)

    def test_create_network(self):
        url = reverse("electronics:electronicsnetwork-create")
        data = {
            "name": "New Network",
            "debt_to_supplier": "1000.00",
            "contacts": [self.contact.id],
            "products": [self.product.id],
            "supplier": None,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_update_network(self):
        url = reverse("electronics:electronicsnetwork-update", args=[self.network.id])
        data = {
            "name": "Updated Network",
            "debt_to_supplier": "2000.00",
            "contacts": [self.contact.id],
            "products": [self.product.id],
            "supplier": None,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Network")

    def test_partial_update_network(self):
        url = reverse("electronics:electronicsnetwork-update", args=[self.network.id])
        data = {"name": "Test Update"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Update")

    def test_delete_network(self):
        url = reverse("electronics:electronicsnetwork-destroy", args=[self.network.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ElectronicsNetwork.objects.filter(id=self.network.id).exists())
