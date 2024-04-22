from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models, IntegrityError
from django.utils.translation import gettext_lazy as _

from core.validator import mobile_regex


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now=True, verbose_name=_("Created at"))

    class Meta:
        abstract = True


class Unit(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Unit name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Company name'))
    phone = models.CharField(max_length=100, verbose_name=_('Company phone'), validators=[mobile_regex], null=True,
                             blank=True)
    address = models.TextField(null=True, blank=True, verbose_name=_("Company address"), )

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")


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

    unit = models.ForeignKey(to=Unit, on_delete=models.CASCADE, verbose_name=_("Unit"), help_text=_("Price per unit."))

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
    recorder_user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name=_("Recorder User"))
    description = models.TextField(null=True, blank=True, verbose_name=_("Archive description"))

    def __str__(self):
        return f'{self.recorder_user.username} - {self.uuid}'

    @property
    def total_price(self):
        s = 0

        for i in self.archiveitem_set.all():
            s += i.amount * i.warehouse_item.product.price

        return s

    class Meta:
        verbose_name = _("Warehouse Archive")
        verbose_name_plural = _("Warehouse Archives")


class ArchiveItem(models.Model):
    warehouse_item = models.ForeignKey(to=WarehouseItem, on_delete=models.CASCADE, verbose_name=_("Item"))
    amount = models.PositiveIntegerField(verbose_name=_("Amount"))
    archive = models.ForeignKey(to=WarehouseArchive, on_delete=models.CASCADE, verbose_name=_("Archive"))

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.amount > self.warehouse_item.amount:
            raise IntegrityError(
                _(f"Not enough {self.warehouse_item.product.name} in the {self.warehouse_item.warehouse.name}"))

        self.warehouse_item.amount -= self.amount
        self.warehouse_item.save()

        super(ArchiveItem, self).save(force_insert, force_update, using, update_fields, )

    class Meta:
        verbose_name = _("Archive Item")
        verbose_name_plural = _("Archive Items")

    def __str__(self):
        return f'{self.warehouse_item.warehouse.name} - {self.warehouse_item.product.name} - {self.amount}'
