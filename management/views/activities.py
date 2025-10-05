from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from ..models import Activity, RecycledMaterial
from ..forms import ActivityForm, RecycledMaterialForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView, UpdateView


# Listar actividades
class ActivityListView(View, LoginRequiredMixin, UserPassesTestMixin):
    def get(self, request):
        activities = Activity.objects.all().order_by("-date")
        return render(request, "management/activities/activity_list.html", {
            "activities": activities
            })


class ActivityCreateView(View, LoginRequiredMixin, UserPassesTestMixin):
    
    
    def get(self, request):
        user = get_user_model()
        form = ActivityForm()
        return render(request, "management/activities/create_activity.html", {
            "form": form
            })

    def post(self, request):
        form = ActivityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("activity_list")
        return render(request, "management/activities/create_activity.html", {
            "form": form
            })
        
class ActivityDetailView(View, LoginRequiredMixin, UserPassesTestMixin):
    def get(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        materials = activity.materials.all()
        material_form = RecycledMaterialForm()
        return render(request, "management/activities/activity_detail.html", {
            "activity": activity,
            "materials": materials,
            "material_form": material_form
            })

    def post(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        material_form = RecycledMaterialForm(request.POST)
        if material_form.is_valid():
            recycled_material = material_form.save(commit=False)
            recycled_material.activity = activity
            recycled_material.save()
            return redirect("activity_detail", pk=pk)
        materials = activity.materials.all()
        return render(request, "management/activities/activity_detail.html", {
            "activity": activity,
            "materials": materials,
            "material_form": material_form
            })
    

class ActivityUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "management/activities/edit_activity.html"


    def test_func(self):
        return self.request.user.role in ["admin", "operator"]

    def get(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        form = ActivityForm(instance=activity)
        return render(request, self.template_name, {
            "form": form, 
            "activity": activity
            })

    def post(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect("activity_detail", pk=pk)
        return render(request, self.template_name, {
            "form": form, 
            "activity": activity
            })
    
class ActivityDeleteView(View):
    def get(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        return render(request, "management/activities/delete_activity.html", {
            "activity": activity
            })

    def post(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        activity.delete()
        return redirect("activity_list")    
    
    
class RecycledMaterialDeleteView(View):
    def post(self, request, activity_pk, material_pk):
        activity = get_object_or_404(Activity, pk=activity_pk)
        material = get_object_or_404(RecycledMaterial, pk=material_pk, activity=activity)
        material.delete()
        return redirect("activity_detail", pk=activity_pk)
    
