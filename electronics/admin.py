from django import forms
from django.contrib import admin

from electronics.models import Contact, ElectronicsNetwork, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt_to_supplier=0)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "email")
    search_fields = ("email", "country", "city")
    list_filter = ("country", "city")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model")
    search_fields = ("name", "model")


class ElectronicsNetworkAdminForm(forms.ModelForm):
    class Meta:
        model = ElectronicsNetwork
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["supplier"].queryset = ElectronicsNetwork.objects.exclude(pk=self.instance.pk)
        else:
            self.fields["supplier"].queryset = ElectronicsNetwork.objects.all()


@admin.register(ElectronicsNetwork)
class ElectronicsNetworkAdmin(admin.ModelAdmin):
    form = ElectronicsNetworkAdminForm
    list_display = ("id", "name", "hierarchy_level")
    search_fields = ("name",)
    list_filter = ("contacts__city",)
    actions = [clear_debt]
    readonly_fields = ("created_at",)
    list_select_related = ("supplier",)

    def get_contact_city(self, obj):
        return obj.contacts.city if obj.contacts else "-"

    get_contact_city.short_description = "Город"
