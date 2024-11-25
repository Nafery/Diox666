from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Residente, ResidenteEnfermedad, ResidenteMedicamento, Enfermedad, Medicamento, Empleado, Rol
from .validators import validar_rut
import datetime

class EmpleadoLoginForm(AuthenticationForm):
    username = forms.CharField(label="Correo Electrónico", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingresa tu correo',
    }))
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingresa tu contraseña',
    }))

class ResidenteForm(forms.ModelForm):
    class Meta:
        model = Residente
        fields = ['rut', 'nombre', 'ap_paterno', 'ap_materno', 'fecha_nacimiento', 'genero', 
                  'contacto_emergencia', 'telefono_emergencia', 'habitacion', 'observaciones', 'imagen']

    # Definir el widget para el campo de fecha de nacimiento
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date', 
            'class': 'form-control',  # Estilo de formulario Bootstrap
            'placeholder': 'Seleccionar fecha'
        }),
        initial=datetime.date.today
    )

    
class ResidenteEnfermedadForm(forms.ModelForm):
    class Meta:
        model = ResidenteEnfermedad
        fields = ['enfermedad', 'fecha_diagnostico', 'tratamiento']

class ResidenteMedicamentoForm(forms.ModelForm):
    class Meta:
        model = ResidenteMedicamento
        fields = ['medicamento', 'dosis', 'frecuencia', 'fecha_inicio', 'fecha_fin', 'observaciones']

class EmpleadoRegistroForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    
    class Meta:
        model = Empleado
        fields = [
            'rut', 'nombre', 'ap_paterno', 'ap_materno', 
            'email', 'telefono', 'fecha_contratacion', 
            'direccion', 'rol', 'imagen'
        ]
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data