from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Email',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
        }
        
        help_texts = {}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    

class ProfileForm(UserChangeForm):
    password = None  # Exclude the password field

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'phone', 'photo')
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Email',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'birth_date': 'Fecha de Nacimiento',
            
        }
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'birth_date', 'phone', 'photo']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'birth_date': 'Fecha de Nacimiento',
            'phone': 'Teléfono',
            'photo': 'Foto de Perfil',
        }
        

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'document_number', 'birth_date', 'terms_accepted']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'max': timezone.now().date()}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
        }
        
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone': 'Teléfono',
            'document_number': 'Número de Documento',
            'birth_date': 'Fecha de Nacimiento',
            'terms_accepted': 'Acepto los términos y condiciones',
        }
    def clean_terms_accepted(self):
        terms_accepted = self.cleaned_data.get('terms_accepted')
        if not terms_accepted:
            raise forms.ValidationError("Debes aceptar los términos y condiciones para continuar.")
        return terms_accepted
    
    

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'phone', 'email', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            
            

        }

class RoleAssignmentForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(), 
        label="Usuario", 
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    
    role = forms.ChoiceField(
        choices=get_user_model().ROLE_CHOICES, 
        label="Rol", 
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'role')
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Email',
            'password1': 'Contraseña',
            'password2': 'Confirmar Contraseña',
            'role': 'Rol',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user