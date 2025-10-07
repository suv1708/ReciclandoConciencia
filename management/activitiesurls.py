from django.urls import path
from .views.activities import *


urlpatterns = [
    path("", ActivityListView.as_view(), name="activity_list"),
    path("create/", ActivityCreateView.as_view(), name="activity_create"),
    path("<int:pk>/", ActivityDetailView.as_view(), name="activity_detail"),
    path("<int:pk>/edit/", ActivityUpdateView.as_view(), name="activity_edit"),
    path("<int:pk>/delete/", ActivityDeleteView.as_view(), name="activity_delete"),
]