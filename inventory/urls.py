from django.urls import path
from .import category,dashboard,brand,measurement,products,supplier,restock,job,requisition,reports,utils,allocation,closingstock

app_name = 'inventory'

urlpatterns = [
    path('dashboard/',dashboard.InventoryDashboardView,name='dashboard'), 

    #category start
    path('categories/',category.category,name='category-list'),
    path('categories/add/',category.add_category,name='new-category'),
    path('categories/<str:category_id>/update/',category.edit_category,name='edit-category'),
    path('categories/<str:category_id>/delete/',category.delete_category,name='delete-category'),
    path('categories/upload/',category.category_upload,name='upload-category'),
    #categoryend

    #Brand Start
    path('brand/',brand.brand,name='brand-list'),
    path('brnad/add/',brand.add_brand,name='new-brand'),
    path('brand/<str:brand_id>/update/',brand.edit_brand,name='edit-brand'),
    path('brand/<str:brand_id>/delete/',brand.delete_brand,name='delete-brand'),
    path('brand/upload/',brand.brand_upload,name='upload-brand'),
    #Brand End

    #measure Start
    path('measurement/',measurement.measurement,name='measurement-list'),
    path('measurement/add/',measurement.add_measurement,name='new-measurement'),
    path('measurement/<str:measurement_id>/update/',measurement.edit_measurement,name='edit-measurement'),
    path('measurement/<str:measurement_id>/delete/',measurement.delete_measurement,name='delete-measurement'),
    path('measurement/upload/',measurement.measurement_upload,name='upload-measurement'),
    #Brand End

    #product Start
    path('product/',products.product,name='product-list'),
    path('product/add/',products.add_product,name='new-product'),
    path('product/<str:product_id>/update/',products.edit_product,name='edit-product'),
    path('product/<str:product_id>/delete/',products.delete_product,name='delete-product'),
    path('product/upload/',products.product_upload,name='upload-product'),
    path('product/<str:product_id>/view/',products.detail_product,name='view-product'),
    path('assets/avialable/',products.aviable_assets,name='aviable-assets'),
    path('products/closing_stock/',closingstock.closing_stock,name='closing-stock'),
    path('products/closing_stock/<str:closing_stock_id>/',closingstock.closingstock_product,name='closing-stock-products'),
    path('products/closing_stock/<str:closing_stock_product_id>/detail/',closingstock.closingstock_detail_product,name='closing-stock-products-detail'),
    path('product/close/stock/',closingstock.close_stock,name='close-stock'),
    #Product End

    #supplier Start
    path('supplier/',supplier.supplier,name='supplier-list'),
    path('supplier/add/',supplier.add_supplier,name='new-supplier'),
    path('supplier/<str:supplier_id>/products/',supplier.add_supplier_detail,name='supplier-products'),
    path('supplier/<str:supplier_id>/prodduct/remove/',supplier.delete_supplier_item,name='remove-product'),
    path('supplier/<str:supplier_id>/update/',supplier.edit_supplier,name='edit-supplier'),
    path('supplier/<str:supplier_id>/delete/',supplier.delete_supplier,name='delete-supplier'),
    path('supplier/upload/',supplier.supplier_upload,name='upload-supplier'),
    #supplier End

    #restock Start
    path('restock/',restock.restock,name='restock-list'),
    path('restock/add/',restock.add_restock,name='new-restock'),
    path('restock/<str:restock_id>/details/add/',restock.add_restock_detail,name='add-restock-details'),
    path('restock/<str:restock_id>/details/update/',restock.edit_restock_detail,name='edit-restock-details'),
    path('restock/<str:restock_id>/details/upload/',restock.restock_detail_upload,name='upload-restock-details-items'),
    path('restock/<str:restock_id>/details/delete/',restock.delete_restock_item,name='delete-restock-details-item'),
    path('restock/<str:restock_id>/update/',restock.edit_restock,name='edit-restock'),
    path('restock/<str:restock_id>/delete/',restock.delete_restock,name='delete-restock'),
    path('restock/<str:restock_id>/approve/',restock.approve_restock,name='approve-restock'),
    path('restock/<str:restock_id>/cancel/',restock.cancel_restock,name='cancel-restock'),
    path('restock/<str:restock_id>/reverse/',restock.reverse_restock,name='reverse-restock'),
   
    #restock End

    #certification Start
    path('job/',job.job_cert,name='job-list'),
    path('job/add/',job.add_job,name='new-job'),
    path('job/<str:job_id>/details/add/',job.add_job_detail,name='add-job-details'),
    path('job/<str:job_id>/details/update/',job.edit_job_detail,name='edit-job-details'),
    path('job/<str:job_id>/details/upload/',job.job_detail_upload,name='upload-job-details-items'),
    path('job/<str:job_id>/details/delete/',job.delete_job_item,name='delete-job-details-item'),
    path('job/<str:job_id>/update/',job.edit_job,name='edit-job'),
    path('job/<str:job_id>/delete/',job.delete_job,name='delete-job'),
    path('job/<str:job_id>/approve/',job.approve_job,name='approve-job'),
    path('job/<str:job_id>/cancel/',job.cancel_job,name='cancel-job'),
    path('job/<str:job_id>/reverse/',job.reverse_job,name='reverse-job'),
    path('job/loadproduct/',job.load_product,name='load-product'),
    #certification End

    # Requisition Start
    path('requisition/personnal/',requisition.personnalrequisition,name='personnal-requisition-list'),
    path('requisition/pending/',requisition.pendingrequisition,name='pending-requisition-list'),
    path('requisition/awaiting/capital/',requisition.awaitingcapitalrequisition,name='awaiting-capital-requisition-list'),
    path('requisition/awaiting/consumable/',requisition.awaitingconsumablerequisition,name='awaiting-consumable-requisition-list'),
    path('requisition/approved/',requisition.requisitionissue,name='approved-requisition-list'),

    path('requisition/add/',requisition.add_requisition,name='new-requisition'),
    path('requisition/<str:requisition_id>/details/add/',requisition.add_requisition_detail,name='add-requisition-details'),
    path('requisition/<str:requisition_id>/details/update/',requisition.edit_requisition_detail,name='edit-requisition-details'),
    path('requisition/<str:requisition_id>/details/delete/',requisition.delete_requisition_item,name='delete-requisition-details-item'),
    path('requisition/<str:requisition_id>/update/',requisition.edit_requisition,name='edit-requisition'),
    path('requisition/<str:requisition_id>/delete/',requisition.delete_reqisition,name='delete-requisition'),
    path('requisition/<str:requisition_id>/approve/',requisition.approve_requisition,name='approve-requisition'),
    path('requisition/<str:requisition_id>/approve/item/',requisition.approve_individual_items,name='approve-requisition-items'),
    path('requisition/<str:requisition_id>/cancel/item/',requisition.reject_individual_items,name='cancel-requisition-items'),
    path('requisition/<str:requisition_id>/approve/quantity/',requisition.approve_quantity,name='approve-requisition-quantity'),
    path('requisition/<str:requisition_id>/<str:detailbatch_id>/approve/quantity/',requisition.store_approve_quantity,name='store-approve-quantity'),
    path('requisition/<str:requisition_id>/cancel/',requisition.cancel_requisition,name='cancel-requisition'),
    path('requisition/<str:requisition_id>/reverse/',requisition.reverse_requisition,name='reverse-requisition'),
    path('requisition/<str:requisition_id>/send/',requisition.send_notification_reqisition,name='send-requisition'),
    path('requisition/<str:requisition_id>/list-inventory/',requisition.list_inventory,name='list-inventory'),
    path('requisition/<str:requisition_id>/issue/<str:asset_id>/item/',requisition.store_assets_issue,name='store-assets-issue'),
    
    # Requisition End

    #report Start
    path('reports/requisition/',reports.reportrequisition,name='report-requisition'),
    path('reports/requisition/devisional/statistics/',reports.regionrequisition,name='devisional-statistics'),
    path('reports/requisition/sub_devisional/statistics/',reports.districtrequisition,name='sub-devisional-statistics'),
    path('reports/product/low-stock/statistics/',reports.low_stock_alert,name='low-stock-alert'),
    path('reports/products/expired/',reports.expire_products,name='expire-products'),
    path('reports/products/<str:product_id>/forcast/',reports.forecast_view,name='product-forcast'),
    path('low-stock/',reports.check_product_stock,name='low-stock'),
    path('assets/assigned-assets/',reports.assigned_assets,name='assigned-assets'),
    path('assets/return/<str:assets_id>/asset/',reports.return_assets,name='return-assets'),
    #report End

    #allocation Start
    path('allocation/',allocation.allocation,name='allocation-list'),
    path('allocation/add/',allocation.add_allocation,name='new-allocation'),
    path('allocation/<str:allocation_id>/destination/',allocation.add_allocation_destination,name='add-allocation-destination'),
    path('allocation/<str:allocation_id>/destination/update/',allocation.edit_allocation_destination,name='edit-allocation-destination'),
    path('allocation/<str:allocation_id>/destination/item/delete/',allocation.delete_allocation_destination,name='delete-allocation-destination'),
    path('allocation/<str:allocation_id>/destination/release/',allocation.release_allocation_destination,name='release-allocation-destination'),
    path('allocation/<str:destination_id>/destination/product/add/',allocation.add_allocation_detail,name='add-destination-item'),
    path('allocation/<str:destination_id>/destination/product/upload/',allocation.allocation_detail_upload,name='allocation-detail-upload'),
    path('allocation/<str:destination_id>/destination/product/delete/',allocation.delete_destination_item,name='delete-destination-item'),
    path('allocation/<str:allocation_id>/destination/detail/',allocation.view_allocation_destination,name='view-allocation-destination'),
    path('allocation/<str:destination_id>/destination/detail/items/',allocation.view_allocation_detail,name='view-allocation-detail-items'),
    path('allocation/destination/detail/items/<str:item_id>/',allocation.allocation_list_inventory,name='allocation-list-inventory'),
    path('allocation/destination/detail/items/<str:item_id>/<str:detailbatch_id>/',allocation.store_allocation_approve_quantity,name='store-allocation-approve-quantity'),
    path('allocation/destination/detail/asset/<str:item_id>/<str:asset_id>/issue/',allocation.store_allocation_assets_issue,name='store-allocation-assets-issue'),
    
    #allocation End
    


]

