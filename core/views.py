from django.http import Http404
from django.shortcuts import render, get_object_or_404


from core.models import WarehouseArchive, Company


# Create your views here.

def create_receipt(request, pk):
    if not request.user.is_staff and not request.user.is_superuser:
        raise Http404
    archive: WarehouseArchive = get_object_or_404(WarehouseArchive, pk=pk)
    company: Company = Company.objects.first()
    data = {
        "archive": {
            "uuid": archive.invoice_number,
            "recorder": archive.recorder_user.get_full_name(),
            "description": archive.description,
            "total_price": archive.total_price,
            'created_at': archive.created_at,
        },
        "items": [

        ]
    }

    if company:
        data['company'] = {
            'name': company.name,
            'phone': company.phone,
            'address': company.address,
        }

    for i in archive.archiveitem_set.all():
        data['items'].append({
            'name': i.warehouse_item.product.name,
            'amount': i.amount,
            'fee': i.warehouse_item.product.price,
            'unit': i.warehouse_item.product.unit.name,
            'price': i.warehouse_item.product.price * i.amount,
            'warehouse': i.warehouse_item.warehouse.name
        })

    return render(request=request, template_name='receipt.html', context={'data': data})
