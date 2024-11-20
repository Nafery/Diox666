from django import forms
from .models import Residente, ResidenteEnfermedad, ResidenteMedicamento, Enfermedad, Medicamento

class ResidenteForm(forms.ModelForm):
    tiene_enfermedades = forms.BooleanField(required=False, label="¿Tiene enfermedades?", initial=False)
    consume_medicamentos = forms.BooleanField(required=False, label="¿Consume medicamentos?", initial=False)

    class Meta:
        model = Residente
        fields = ['rut', 'nombre', 'ap_paterno', 'ap_materno', 'fecha_nacimiento', 'genero', 
                  'contacto_emergencia', 'telefono_emergencia', 'habitacion', 'observaciones', 'imagen']
    
class ResidenteEnfermedadForm(forms.ModelForm):
    class Meta:
        model = ResidenteEnfermedad
        fields = ['enfermedad', 'fecha_diagnostico', 'tratamiento']

class ResidenteMedicamentoForm(forms.ModelForm):
    class Meta:
        model = ResidenteMedicamento
        fields = ['medicamento', 'dosis', 'frecuencia', 'fecha_inicio', 'fecha_fin', 'observaciones']
