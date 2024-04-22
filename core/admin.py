from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from core.models import Category, Product, Warehouse, WarehouseItem, WarehouseArchive, ArchiveItem, Unit, Company


@admin.action(description=_("Invoice"))
def get_invoice(model_admin, request, queryset):
    if len(queryset) != 1:
        messages.error(request, _("Please select just one."))

    else:
        return redirect('receipt', pk=queryset.first().id)


@admin.register(Company)
class CompanyModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


@admin.register(Unit)
class UnitModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ArchiveItem)
class WarehouseArchiveItemModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'created_at', ]
    list_filter = ['category', ]
    search_fields = ['name', ]


class WarehouseItemInlineAdmin(admin.TabularInline):
    model = WarehouseItem
    extra = 1


@admin.register(Warehouse)
class WarehouseModelAdmin(admin.ModelAdmin):
    inlines = [WarehouseItemInlineAdmin, ]
    list_display = ['name', ]


class ArchiveItemInlineModelAdmin(admin.TabularInline):
    model = ArchiveItem
    extra = 1


@admin.register(WarehouseArchive)
class WarehouseArchiveModelAdmin(admin.ModelAdmin):
    inlines = [ArchiveItemInlineModelAdmin, ]
    actions = [get_invoice, ]
    readonly_fields = ['invoice_number', ]
    search_fields = ['invoice_number', ]

    list_display = ['recorder_user', 'invoice_number', ]
    list_filter = ['recorder_user', ]
