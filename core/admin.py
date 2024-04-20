from django.contrib import admin

from core.models import Category, Product, Warehouse, WarehouseItem


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]


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
