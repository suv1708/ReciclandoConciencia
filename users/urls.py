from django.urls import path
from .views.auth import *
from django.contrib.auth.views import LogoutView
from .views.profile import *
from .views.adminv import *


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete_profile'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('role-assignment/', RoleAssignmentView.as_view(), name='role_assig'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
]
