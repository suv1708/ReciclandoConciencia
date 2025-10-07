from .models import Activity, RecycledMaterial
from django import forms
from .models import *
from django.contrib.auth import get_user_model


class AdminReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'status', 'assigned_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].queryset = (
            get_user_model().objects.exclude(role="citizen")
        )
        
        
class UserReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description']


class UserReportEditForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  
        super().__init__(*args, **kwargs)

        if user and user.role == "citizen":
            self.fields["status"].disabled = True


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["title", "description", "activity_type",
                  "date", "location", "participants_count"]
        labels = {
            "title": "Título",
            "description": "Descripción",
            "activity_type": "Tipo de Actividad",
            "date": "Fecha",
            "location": "Ubicación",
            "participants_count": "Número de Participantes",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 4}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "participants_count": forms.NumberInput(attrs={"min": 0}),
        }


class RecycledMaterialForm(forms.ModelForm):
    class Meta:
        model = RecycledMaterial
        fields = ["material_type", "quantity_kg"]


