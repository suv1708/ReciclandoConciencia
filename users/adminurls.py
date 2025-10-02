from django.urls import path
from .views.auth import *
from django.contrib.auth.views import LogoutView
from .views.profile import *
from .views.adminv import *

urlpatterns = [

    path('user-list/', ListUsersView.as_view(), name='user_list'),
    path('reports/', ReportsView.as_view(), name='report_list'),
    path('user-edit/<int:pk>/', AdminUserEditView.as_view(), name='admin_user_edit'),
    path('user-delete/<int:pk>/', AdminUserDeleteView.as_view(), name='admin_user_delete'),
    path('report/edit/<int:pk>/', AdminReportEditView.as_view(), name='admin_edit_report'),
    path('report/delete/<int:pk>/', AdminReportDeleteView.as_view(), name='admin_delete_report'),
    
]
