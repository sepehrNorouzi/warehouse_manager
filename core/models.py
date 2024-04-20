from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True, verbose_name=_("Created at"))

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Category name"))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name=_("Product Name"), )
    description = models.TextField(null=True, blank=True, verbose_name=_('Product description'))

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=_("Product category"))

    price = models.PositiveIntegerField(default=0, verbose_name=_("Price"))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return f'{self.name} - {self.category.__str__()} - {self.price}'


class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Warehouse Name"), )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Warehouse')
        verbose_name_plural = _('Warehouses')


class WarehouseItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    amount = models.PositiveIntegerField(default=0, verbose_name=_("Product amount"))
    warehouse = models.ForeignKey(to=Warehouse, on_delete=models.CASCADE, verbose_name=_('Warehouse'))

    class Meta:
        verbose_name = _('Warehouse Item')
        verbose_name_plural = _('Warehouse Items')

    def __str__(self):
        return f'{self.warehouse.__str__()} - {self.product.name}'


class WarehouseArchive(BaseModel):
    uuid = models.UUIDField(verbose_name=_("UUID"), editable=False, default=uuid4)
    item = models.ForeignKey(to=WarehouseItem, verbose_name=_("Item"), on_delete=models.RESTRICT)
    amount = models.PositiveIntegerField(default=1, verbose_name=_("Item amount"))

