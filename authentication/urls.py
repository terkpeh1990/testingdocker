from django.urls import path
from django.views.generic import TemplateView
from . import auth,grades



app_name = 'authentication'

urlpatterns = [
    path('login/',auth.login_view,name='login'),
    path('user/',auth.users,name='user-list'),
    path('user/<str:user_id>/update/',auth.edit_user,name='edit-user'),
    path('user/<str:user_id>/self_update/',auth.user_edit_user,name='self-edit-user'),
    path('user/new/',auth.add_user,name='new-user'),
    path('user/<str:user_id>/delete/',auth.delete_user,name='delete-user'),
    path('user/<str:user_id>/detail/',auth.detail_user,name='detail-user'),
    path('user/<str:user_id>/change/',auth.change_userstatus,name='user-status'),
    path('user/<str:user_id>/reset-password/',auth.reset_password,name='reset-password'),
    path('user/upload/',auth.uploads_users,name='uploads-user'),
    path('user/load_district/',auth.load_district,name="load-district"),
    path('user/change_password/',auth.change_password,name='change-password'),
    path('logout/',auth.logout_request,name='log-out'),
    

    #group start
    path('groups/',auth.usergroups,name='group-list'),
    path('group/<str:group_id>/update/',auth.edit_usergroups,name='edit-group'),
    path('group/new/',auth.add_usergroups,name='new-group'),
    path('group/<str:group_id>/delete/',auth.delete_usergroups,name='delete-group'),
    path('group/<str:group_id>/detail/',auth.detail_usergroups,name='detail-group'),
    #group end

    #grade start
    path('grade/',grades.grade,name='grade-list'),
    path('grade/<str:grade_id>/update/',grades.edit_grade,name='edit-grade'),
    path('grade/new/',grades.add_grade,name='new-grade'),
    path('grade/<str:grade_id>/delete/',grades.delete_grade,name='delete-grade'),
    path('grade/upload/',grades.uploads,name='uploads-grade'),
    #grade end

   
]

