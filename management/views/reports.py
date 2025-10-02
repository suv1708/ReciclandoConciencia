from ..models import *
from ..forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model



class UserReportListView(LoginRequiredMixin, View):

        def get(self, request):
            user = get_user_model()
            reports = Report.objects.filter(
                **{
                    'reporter' if request.user.role == 'citizen' 
                    else 'assigned_to': request.user
                    })

            
            return render(request, "management/reports/user_reports.html", {
                "reports": reports
                })


class CreateReportView(CreateView):
    model = Report
    form_class = UserReportForm
    success_url = reverse_lazy("user_report_list")
    

    
    def get(self, request):
        form = self.form_class()
        return render(request, "management/reports/create_report.html", {
            "form": form
            })
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return render(request, "management/reports/create_report.html", {
            "form": form
            })
        
    def form_valid(self, form):
        form.instance.reporter = self.request.user
        return super().form_valid(form)
        
    
class EditReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        report = get_object_or_404(Report, pk=self.kwargs['pk'])
        return self.request.user == report.reporter or self.request.user.role == 'operator'

    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        form = UserReportEditForm(
            instance=report, user=request.user)
        return render(request, "management/reports/edit_report.html", {
            "form": form,
            "report": report
        })

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        form = UserReportEditForm(
            request.POST, instance=report, user=request.user)
        if form.is_valid():
            if request.user.role == "citizen":
                form.instance.status = report.status
            form.save()
            return redirect("user_report_list")
        return render(request, "management/reports/edit_report.html", {
            "form": form,
            "report": report
        })


class DeleteReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        report.delete()
        return redirect("user_report_list")
