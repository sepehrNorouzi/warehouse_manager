from django.contrib import admin

from core.models import Category, Product, Warehouse, WarehouseItem, WarehouseArchive, ArchiveItem, Unit, Company


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
