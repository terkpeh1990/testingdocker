from django.urls import path
from .import classification,accountingrecognition,ipsascategory,location,sourceoffunding,gfscategory,subcategory,methodofacquisition,assets

app_name = 'fixedassets'

urlpatterns = [
    #Classification Start
    path('classification/',classification.classification,name='classification-list'),
    path('classification/add/',classification.add_classification,name='new-classification'),
    path('classification/<str:classification_id>/update/',classification.edit_classification,name='edit-classification'),
    path('classification/<str:classification_id>/delete/',classification.delete_classification,name='delete-classification'),
    path('classification/upload/',classification.classification_upload,name='upload-classification'),
    #Classification End

    #Accounting Recognition Start
    path('accountingrecognition/',accountingrecognition.recognition,name='recognition-list'),
    path('accountingrecognition/add/',accountingrecognition.add_recognition,name='new-recognition'),
    path('accountingrecognition/<str:recognition_id>/update/',accountingrecognition.edit_recognition,name='edit-recognition'),
    path('accountingrecognition/<str:recognition_id>/delete/',accountingrecognition.delete_recognition,name='delete-recognition'),
    path('accountingrecognition/upload/',accountingrecognition.recognition_upload,name='upload-recognition'),
    #Accounting Recognition End

    #GFS Category Start
    path('gfscategory/',gfscategory.gfscategory,name='gfscategory-list'),
    path('gfscategory/add/',gfscategory.add_gfscategory,name='new-gfscategory'),
    path('gfscategory/<str:gfscategory_id>/update/',gfscategory.edit_gfscategory,name='edit-gfscategory'),
    path('gfscategory/<str:gfscategory_id>/delete/',gfscategory.delete_gfscategory,name='delete-gfscategory'),
    path('gfscategory/upload/',gfscategory.gfscategory_upload,name='upload-gfscategory'),
    #GFS Category End

    #Ipsas Category Start
    path('ipsascategory/',ipsascategory.ipsascategory,name='ipsascategory-list'),
    path('ipsascategory/add/',ipsascategory.add_ipsascategory,name='new-ipsascategory'),
    path('ipsascategory/<str:ipsascategory_id>/update/',ipsascategory.edit_ipsascategory,name='edit-ipsascategory'),
    path('ipsascategory/<str:ipsascategory_id>/delete/',ipsascategory.delete_ipsascategory,name='delete-ipsascategory'),
    path('ipsascategory/upload/',ipsascategory.ipsascategory_upload,name='upload-ipsascategory'),
    #Ipsas Category End

    #Location Start
    path('location/',location.location,name='location-list'),
    path('location/add/',location.add_location,name='new-location'),
    path('location/<str:location_id>/update/',location.edit_location,name='edit-location'),
    path('location/<str:location_id>/delete/',location.delete_location,name='delete-location'),
    path('location/upload/',location.location_upload,name='upload-location'),
    #Location End

    #Funding Start
    path('funding/',sourceoffunding.funding,name='funding-list'),
    path('funding/add/',sourceoffunding.add_funding,name='new-funding'),
    path('funding/<str:funding_id>/update/',sourceoffunding.edit_funding,name='edit-funding'),
    path('funding/<str:funding_id>/delete/',sourceoffunding.delete_funding,name='delete-funding'),
    path('funding/upload/',sourceoffunding.funding_upload,name='upload-funding'),
    #Funding End

    #Sub Category Start
    path('subcategory/',subcategory.subcategory,name='subcategory-list'),
    path('subcategory/add/',subcategory.add_subcategory,name='new-subcategory'),
    path('subcategory/<str:subcategory_id>/update/',subcategory.edit_subcategory,name='edit-subcategory'),
    path('subcategory/<str:subcategory_id>/delete/',subcategory.delete_subcategory,name='delete-subcategory'),
    path('subcategory/upload/',subcategory.subcategory_upload,name='upload-subcategory'),
    #Sub Category End

    #Method of Acquisition Start
    path('methodofacquisition/',methodofacquisition.methodofacquisition,name='methodofacquisition-list'),
    path('methodofacquisition/add/',methodofacquisition.add_methodofacquisition,name='new-methodofacquisition'),
    path('methodofacquisition/<str:methodofacquisition_id>/update/',methodofacquisition.edit_methodofacquisition,name='edit-methodofacquisition'),
    path('methodofacquisition/<str:methodofacquisition_id>/delete/',methodofacquisition.delete_methodofacquisition,name='delete-methodofacquisition'),
    path('methodofacquisition/upload/',methodofacquisition.methodofacquisition_upload,name='upload-methodofacquisition'),
    #Method of Acquisition End

    #Assets Start
    path('assets/',assets.assets,name='asset-list'),
    path('assets/selectclassification/',assets.add_selectclassification,name='select-classification'),
    path('assets/reportselect/',assets.report_selectclassification,name='report-selectclassification'),
    path('assets/reportselect/<str:assetclassification>/',assets.export_excel,name='export-excel'),
    path('assets/<str:formclassification>/add/',assets.add_assets,name='new-asset'),
    path('assets/load_subcategory/',assets.load_subcategory,name="load-subcategory"),
    path('assets/load_user/',assets.load_user,name="load_user"),
    path('assets/<str:asset_id>/update/',assets.edit_assets,name='edit-assets'),
    path('assets/<str:asset_id>/delete/',assets.delete_asset,name='delete-assets'),
    path('assets/<str:asset_id>/assign/',assets.assigned_assets,name='assigned-assets'),
    path('assets/<str:asset_id>/view_assets/',assets.view_assets,name='detail-assets'),
    path('assets/<str:assign_id>/return/',assets.return_assets,name='returned-assets'),
    path('assets/depreciation/',assets.depreciation,name='depreciation-list'),
    path('assets/depreciation/new/',assets.run_depreciation,name='new-depreciation'),
    path('assets/depreciaition/<depreciation_id>',assets.view_depreciation,name='detail-depreciation'),
    path('assets/duereevaluation',assets.reevaluation,name='reevaluation-list'),
    path('assets/<str:asset_id>/evaluate/',assets.reevaluate_asset,name='reevaluate-asset'),
    path('assets/disposal/',assets.disposal,name='disposal-list'),
    path('assets/<str:asset_id>/disposal/',assets.disposal_asset,name='dispose-asset'),
    path('assets/dashboard/',assets.assetdashboard,name='assetdashboard'),


    
    # path('methodofacquisition/<str:methodofacquisition_id>/delete/',methodofacquisition.delete_methodofacquisition,name='delete-methodofacquisition'),
    # path('methodofacquisition/upload/',methodofacquisition.methodofacquisition_upload,name='upload-methodofacquisition'),
    #MAssets End
]



