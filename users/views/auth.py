from django.views.generic import UpdateView
from django.contrib.auth import login

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from ..forms import LoginForm, RegistrationForm, EditProfileForm
from django.urls import reverse_lazy
from django.views.generic import  CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import *
from django.contrib.auth import get_user_model
from django.views import View


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('profile')



class UserRegisterView(CreateView):
    template_name = "users/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("complete_profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    


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
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, "users/edit_profile.html", {
            "form": form
            })


