from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _('Warehouse manager')  # default: "Django Administration"
admin.site.index_title = _('Poseidon Warehouse manager')  # default: "Site administration"
admin.site.site_title = _('Poseidon Warehouse manager')  # default: "Django site admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('admin/', permanent=True)),
]
