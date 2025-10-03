from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from ..models import Activity, RecycledMaterial
from ..forms import ActivityForm, RecycledMaterialForm

# Listar actividades

class ActivityListView(View):
    def get(self, request):
        activities = Activity.objects.all().order_by("-date")
        return render(request, "management/activities/activity_list.html", {
            "activities": activities
            })


class ActivityCreateView(View):
    def get(self, request):
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