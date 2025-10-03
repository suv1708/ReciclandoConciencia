from django.urls import path
from .views.activities import *

app_name = "activities"

urlpatterns = [
    path("", ActivityListView.as_view(), name="activity_list"),
    path("create/", ActivityCreateView.as_view(), name="activity_create"),
]