from django.urls import path
from .views.reports import *

urlpatterns = [
    path('', UserReportListView.as_view(), name='user_report_list'),
    path('create/', CreateReportView.as_view(), name='create_report'),
    path('edit/<int:pk>/', EditReportView.as_view(), name='edit_report'),
    path('delete/<int:pk>/', DeleteReportView.as_view(), name='delete_report'),
    
]