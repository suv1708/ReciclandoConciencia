
from django.db import models
from django.conf import settings


class Project(models.Model):
    name = models.CharField("Nombre", max_length=200)
    description = models.TextField("Descripción")
    start_date = models.DateField("Fecha de inicio", blank=True, null=True)
    end_date = models.DateField("Fecha de fin", blank=True, null=True)
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects_responsible"
    )

    def __str__(self):
        return self.name


class Activity(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="activities")
    name = models.CharField("Nombre", max_length=200)
    description = models.TextField("Descripción", blank=True, null=True)
    execution_date = models.DateField(
        "Fecha de ejecución", blank=True, null=True)
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="activities_responsible"
    )

    def __str__(self):
        return f"{self.name} ({self.project.name})"


class Participation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    role = models.CharField("Rol en la actividad", max_length=100)

    def __str__(self):
        return f"{self.user.username} en {self.activity.name} como {self.role}"


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