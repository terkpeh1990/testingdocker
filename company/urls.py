from django.urls import path
from django.views.generic import TemplateView
from . import devision,sub_devision,approvals



app_name = 'company'

urlpatterns = [
 #Devison start
    path('devision/',devision.devision,name='devision-list'),
    path('devision/status/pending/',devision.pending_devision,name='pending-devision-list'),
    path('devision/<str:devision_id>/update/',devision.edit_devision,name='edit-devision'),
    path('devision/new/',devision.add_devision,name='new-devision'),
    path('devision/<str:devision_id>/delete/',devision.delete_devision,name='delete-devision'),
    path('division/upload/',devision.uploads_devision,name='uploads-devision'),
    path('devision/<str:devision_id>/detail/',devision.devision_detail,name='detail-devision'),
    path('devision/<str:devision_id>/status/',devision.change_devision_status,name='devision-status'),
    path('devision/tag_devision/<str:devision_id>/',devision.tag_devision,name='tag-devision'),
    #region end

    #sub devision start
    path('subdivison/',sub_devision.sub_devision,name='sub_division-list'),
    path('subdivision/<str:subdivision_id>/update/',sub_devision.edit_sub_devison,name='edit-sub-devison'),
    path('subdivision/new/',sub_devision.add_sub_devison,name='new-sub_devision'),
    path('subdivision/<str:subdivision_id>/delete/',sub_devision.delete_sub_devision,name='delete-sub_devision'),
    path('subdivision/upload/',sub_devision.uploads_sub_devision,name='uploads-sub_division'),
    #sub devision end

    # Approval start
    path('approval/',approvals.approval,name='approval-list'),
    path('approval/<str:approval_id>/update/',approvals.edit_approval,name='edit-approval'),
    path('approval/new/',approvals.add_approval,name='new-approval'),
    path('approval/<str:approval_id>/delete/',approvals.delete_approval,name='delete-approval'),
    path('approval/upload/',approvals.uploads_approval,name='uploads-approval'),
    
    #Approval end
]