from django.urls import path
from .import purchase_order

app_name = 'purchaseorder'

urlpatterns = [
    path('purchase_requisition/',purchase_order.purchase_requisition,name='purchase-requisition-list'),
    path('purchase_requisition/create/<str:document_product_id>/',purchase_order.create_purchase_order,name='new-purchase-requisition'),
    path('add_purchase_requisition/<str:purchase_requisition_id>/update/',purchase_order.add_purchase_requisition,name='update-purchase-requisition'),
    path('purchase_requisition/<str:purchase_requisition_id>/Detail/',purchase_order.view_purchase_requisition,name='purchase-requisition-detail'),
    path('approve_purchase_requisition/<str:purchase_requisition_id>/approve/',purchase_order.approve_purchase_requisition,name='approve-purchase-requisition'),
    path('cancel_purchase_requisition/<str:purchase_requisition_id>/cancel/',purchase_order.cancel_purchase_requisition,name='cancel-purchase-requisition'),
    path('complete_supplier_selection/<str:purchase_requisition_id>/confirm/',purchase_order.complete_supplier_selection,name='complete-supplier-selection'),
    path('add_quotation_requisition/<str:quotation_id>/quotation/',purchase_order.add_quotation_requisition,name='quotation-form'),
    path('approve_quotation_requisition/<str:quotation_id>/approve/',purchase_order.approve_quotation_requisition,name='approve-quotation'),
    path('reject_quotation_requisition/<str:quotation_id>/reject/',purchase_order.reject_quotation_requisition,name='reject-quotation'),

    path('lpo/<str:purchase_requisition_id>/new/',purchase_order.create_lpo,name='new-lpo'),
    path('lpo/<str:lpo_id>/detail/',purchase_order.view_lpo,name='detail-lpo'),
    path('lpo/<str:lpo_id>/approve/',purchase_order.approve_lpo,name='approve-lpo'),
    path('lpo/<str:lpo_id>/cancel/',purchase_order.cancel_lpo,name='cancel-lpo'),
    path('lpo/',purchase_order.lpo,name='lpo'),


]


