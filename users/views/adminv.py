from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import TemplateView
from ..models import CustomUser
from ..forms import *
from django.urls import reverse_lazy
from management.forms import *
from django.contrib import messages



class RoleAssignmentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'admin'

    def get(self, request):
        form = RoleAssignmentForm()
        users = CustomUser.objects.all()
        return render(request, "users/role_assignment.html", {
            "form": form, 
            "users": users
            })

    def post(self, request):
        form = RoleAssignmentForm(request.POST)
        users = CustomUser.objects.all()
        if form.is_valid():
            user = form.cleaned_data['user']
            role = form.cleaned_data['role']
            user.role = role
            user.save()
            return render(request, "users/role_assignment.html", {
                "form": RoleAssignmentForm(),
                "users": users,
                "success": f"Rol de {user.username} actualizado a {user.get_role_display()}"
            })
        return render(request, "users/role_assignment.html", {"form": form, "users": users})
    
    
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/admin_dashboard.html'

    def test_func(self):
        return self.request.user.role == 'admin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        return context
    
    
class ListUsersView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/user_list.html'

    def test_func(self):
        return self.request.user.role == 'admin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = CustomUser.objects.all()
        return context
    
    
class ReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/report_list.html'
    
    def test_func(self):
        return self.request.user.role == 'admin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from management.models import Report
        context['reports'] = Report.objects.all()
        return context
    
    
class ReportAssignmentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'admin'

    def get(self, request):
        from management.models import Report
        reports = Report.objects.filter(assigned_to__isnull=True)
        users = CustomUser.objects.filter(role='operator')
        return render(request, "users/assign_report.html", {
            "reports": reports, 
            "users": users
            })

    def post(self, request):
        from management.models import Report
        report_id = request.POST.get('report_id')
        user_id = request.POST.get('user_id')
        try:
            report = Report.objects.get(id=report_id)
            user = CustomUser.objects.get(id=user_id, role='operator')
            report.assigned_to = user
            report.save()
            message = f"Reporte {report.title} asignado a {user.username}"
        except Report.DoesNotExist:
            message = "Reporte no encontrado"
        except CustomUser.DoesNotExist:
            message = "Usuario no encontrado o no es operador"
        
        reports = Report.objects.filter(assigned_to__isnull=True)
        users = CustomUser.objects.filter(role='operator')
        return render(request, "users/assign_report.html", {
            "reports": reports,
            "users": users,
            "message": message
        })
    
    
class AdminUserEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'admin'

    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        form = RoleAssignmentForm(initial={'user': user, 'role': user.role})
        return render(request, "users/admin_user_edit.html", 
                {"form": form, 
                "user_obj": user
                })
        

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        form = RoleAssignmentForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            user.role = role
            user.save()
            messages.success(
                request, f"Rol de {user.username} actualizado a {user.get_role_display()}")
            return redirect("user_list")
        return render(request, "users/admin_user_edit.html", {
                "form": form,
                "user_obj": user
                })
    
    
class AdminUserDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    
    def test_func(self):
        return self.request.user.role == 'admin'

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        username = user.username
        user.delete()
        return render(request, "users/user_list.html", {
            "users": CustomUser.objects.all(),
            "success": f"Usuario {username} eliminado exitosamente."
        })
    
    
class AdminReportEditView(LoginRequiredMixin, UserPassesTestMixin, View):
    
    def test_func(self):
        return self.request.user.role == 'admin'

    def get(self, request, pk):
        from management.models import Report
        report = Report.objects.get(pk=pk)
        form = AdminReportForm(instance=report)
        return render(request, "users/admin_report_edit.html", {
                "form": form, 
                "report": report
                })
        
        

    def post(self, request, pk):
        from management.models import Report
        report = Report.objects.get(pk=pk)
        form = AdminReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            message = f"Reporte {report.title} actualizado exitosamente."
            return redirect("report_list")
            
        return render(request, "users/admin_report_edit.html", {
            "form": form, 
            "report": report
            })
    
    
class AdminReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'admin'

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        report.delete()
        return redirect("report_list")


