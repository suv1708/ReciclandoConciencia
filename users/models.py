from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    document_number = models.CharField(
        "Número de Documento", max_length=20, unique=True)
    phone = models.CharField("Teléfono", max_length=15, blank=True, null=True)
    birth_date = models.DateField("Fecha de Nacimiento", blank=True, null=True)
    photo = models.ImageField(
        "Foto de Perfil", upload_to="profile_photos/", blank=True, null=True, default="static/users/images/default_profile.jpg")
    terms_accepted = models.BooleanField("Términos Aceptados", default=False)

    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("citizen", "Ciudadano"),
        ("operator", "Operador"),
    ]
    role = models.CharField("Rol", max_length=20,
                            choices=ROLE_CHOICES, default="citizen")

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
