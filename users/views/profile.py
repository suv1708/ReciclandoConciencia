from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from ..forms import CompleteProfileForm, EditProfileForm


class CompleteProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = CompleteProfileForm(instance=request.user)
        return render(request, "users/complete_profile.html", {
            "form": form
            })

    def post(self, request):
        form = CompleteProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")  
        return render(request, "users/complete_profile.html", {
            "form": form
            })


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "users/profile.html", {
            "user": request.user
            })


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditProfileForm(instance=request.user)
        return render(request, "users/edit_profile.html", {
            "form": form
            })

    def post(self, request):
        form = EditProfileForm(
            request.POST, 
            request.FILES, 
            instance=request.user
            )
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "users/edit_profile.html", {
            "form": form
        })


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "admin_dashboard.html"

    def test_func(self):
        return self.request.user.role == 'admin'
