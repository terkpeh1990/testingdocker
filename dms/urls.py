from django.urls import path
from django.views.generic import TemplateView
from . import documents



app_name = 'dms'

urlpatterns = [
    #folder start
    path('filemanager/',documents.filemanager,name='filemanager-list'),
    path('filemanager/create-folder/',documents.add_folder,name='create-folder'),
    path('filemanager/folder/<str:folder_id>/pin_folder',documents.pin_folder,name='pin-folder'),
    path('filemanager/folder/<str:folder_id>/unpin_folder',documents.unpin_folder,name='unpin-folder'),
    path('filemanager/folder/<str:folder_id>/update/',documents.edit_folder,name='edit-folder'),
    path('filemanager/files/new/',documents.add_file,name='new-file'),
    path('filemanager/files/<str:file_id>/update/',documents.edit_file,name='edit-file'),
    
    path('filemanager/folder/<str:folder_id>/detail',documents.files,name='folder-detail'),
    path('filemanager/folder/file/<str:file_id>/generate/',documents.add_document_detail,name='add-document_detail'),
    path('filemanager/folder/file/<str:file_id>/edit/',documents.edit_document_detail,name='edit-document_detail'),
    path('filemanager/folder/document/paragraph/<str:item_id>/item/remove/',documents.remove_document_item,name='remove-document_item'),
    path('filemanager/folder/document/<str:document_id>/draft/',documents.save_as_draft,name='save-as_draft'),
    path('filemanager/folder/document/<str:document_id>/approve/',documents.sendpprove_document,name='sendpprove-document'),
    path('filemanager/files/<str:file_id>/currency/',documents.add_document_currency,name='add-document_currency'),
    path('filemanager/files/<str:file_id>/currency/edit/',documents.edit_document_currency,name='edit-document_currency'),
    path('filemanager/folder/<str:file_id>/dudget/',documents.add_document_budget,name='add-document_budget'),
    path('filemanager/folder/document/dudget/<str:item_id>/item/remove/',documents.remove_budget_item,name='remove-budget_item'),
    path('filemanager/folder/document/document/<str:document_id>/budget/attachment/detail/',documents.view_budget_attachment,name='view_budget_attachment'),
    # path('filemanager/folder/file/<str:file_id>/generate/',documents.add_document_detail,name='add-document_detail')
    path('filemanager/folder/document/document/<str:document_id>/attachement/',documents.add_attachment,name='add-attachment'),
    path('filemanager/folder/document/document/<str:item_id>/attachement/remove/',documents.remove_attachemnt,name='remove-attachemnt'),
    path('filemanager/folder/document/document/<str:document_id>/attachement/detail/',documents.view_attachment,name='view-attachment'),
    path('filemanager/folder/document/document/<str:document_id>/minute/',documents.add_munites,name='add-munites'),

    path('filemanager/folder/document/<str:document_id>/save/',documents.save_to_send,name='save-to-send'),
    path('filemanager/folder/document/<str:file_id>/detail/',documents.view_document_detail,name='view-document_detail'),
    path('filemanager/folder/document/<str:document_id>/return_or_cancel/',documents.return_document,name='return-document'),
    path('filemanager/folder/document/<str:file_id>/approved_amount/',documents.add_approved_amount,name='add-approved_amount'),
    path('filemanager/file/<str:file_id>/beneficiary/', documents.document_beneficiary_upload,name='document-beneficiary-upload'),
    path('filemanager/file/<str:file_id>/pull_low_stock/',documents.pull_low_stock_product,name='pull-product'),
    


    
    #Folder end
    
]