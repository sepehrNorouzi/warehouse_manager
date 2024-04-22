from django.shortcuts import render, get_object_or_404

from core.models import WarehouseArchive


# Create your views here.

def create_receipt(request, pk):
    archive: WarehouseArchive = get_object_or_404(WarehouseArchive, pk=pk)
    data = {
        "archive": {
            "uuid": archive.uuid,
            "recorder": archive.recorder_user,
            "description": archive.description,
            "total_price": archive.total_price,
            'created_at': archive.created_at,
        },
        "items": [

        ]
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
