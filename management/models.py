
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ("recoleccion", "Jornada de recolección"),
        ("taller", "Taller / Capacitación"),
        ("campaña", "Campaña de sensibilización"),
        ("otro", "Otro"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES, default="recoleccion")
    date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    participants_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.date}"


class RecycledMaterial(models.Model):
    MATERIAL_TYPES = [
        ("plastico", "Plástico"),
        ("vidrio", "Vidrio"),
        ("papel", "Papel / Cartón"),
        ("metal", "Metal"),
        ("organico", "Orgánico"),
        ("otro", "Otro"),
    ]

    activity = models.ForeignKey(
        Activity, related_name="materials", on_delete=models.CASCADE)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPES)
    quantity_kg = models.DecimalField(
        max_digits=6, decimal_places=2)  # hasta 9999.99 kg

    def __str__(self):
        return f"{self.material_type} - {self.quantity_kg} kg"


class Report(models.Model):
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports_made"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports_assigned"
        
        
    )
    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descripción")
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Fecha de actualización", auto_now=True)
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("in_progress", "En Progreso"),
        ("resolved", "Resuelto"),
    ]
    status = models.CharField(
        "Estado", max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"