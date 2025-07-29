from django.core.exceptions import ValidationError
from django.db import models


class Contact(models.Model):
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=60, verbose_name="Страна")
    city = models.CharField(max_length=170, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=5, verbose_name="Номер дома")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.email


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название продукта")
    model = models.CharField(max_length=200, verbose_name="Модель")
    released_at = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class ElectronicsNetwork(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    contacts = models.ManyToManyField(Contact, verbose_name="Контакты")
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="electronics_network",
        verbose_name="Поставщик",
    )
    debt_to_supplier = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Задолженность")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    @property
    def hierarchy_level(self):
        level = 0
        network = self
        while network.supplier:
            network = network.supplier
            level += 1
        return level

    def clean(self):
        super().clean()
        if self.supplier and self.supplier == self:
            raise ValidationError({"supplier": "Поставщик не может быть самим собой."})

        visited = set()
        supplier = self.supplier
        while supplier:
            if supplier == self:
                raise ValidationError({"supplier": "Обнаружен цикл в цепочке поставщиков."})
            if supplier.id in visited:
                break
            visited.add(supplier.id)
            supplier = supplier.supplier

    def __str__(self):
        return self.name
