from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .models import Residente, Empleado, ResidenteEnfermedad, ResidenteMedicamento
from .forms import ResidenteForm, ResidenteEnfermedadForm, ResidenteMedicamentoForm

# Create your views here.

def index(request):
    context = {}
    return render(request, 'pages/index.html', context)

def lista_residentes(request):
    residentes = Residente.objects.all()
    return render(request, 'pages/lista_residentes.html', {'residentes': residentes})

def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'pages/lista_empleados.html', {'empleados': empleados})

def detalle_residente(request, id):
    residente = get_object_or_404(Residente, id=id)
    return render(request, 'pages/detalle_residente.html', {'residente': residente})

def detalle_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    return render(request, 'pages/detalle_empleado.html', {'empleado': empleado})

def crear_residente(request):
    # Formulario principal para Residente
    residente_form = ResidenteForm(request.POST or None, request.FILES or None)

    # Inicializamos los formsets en caso de que se necesiten
    enfermedad_formset = None
    medicamento_formset = None

    if request.method == 'POST':
        if residente_form.is_valid():
            # Guardar el residente
            residente = residente_form.save()

            # Verificar si el residente tiene enfermedades
            if residente_form.cleaned_data['tiene_enfermedades']:
                ResidenteEnfermedadFormSet = inlineformset_factory(
                    Residente, ResidenteEnfermedad, form=ResidenteEnfermedadForm, extra=1, can_delete=True
                )
                enfermedad_formset = ResidenteEnfermedadFormSet(request.POST, instance=residente)

            # Verificar si el residente consume medicamentos
            if residente_form.cleaned_data['consume_medicamentos']:
                ResidenteMedicamentoFormSet = inlineformset_factory(
                    Residente, ResidenteMedicamento, form=ResidenteMedicamentoForm, extra=1, can_delete=True
                )
                medicamento_formset = ResidenteMedicamentoFormSet(request.POST, instance=residente)

            # Si los formsets son válidos, guardamos las enfermedades y medicamentos
            if (enfermedad_formset is None or enfermedad_formset.is_valid()) and (medicamento_formset is None or medicamento_formset.is_valid()):
                # Guardar las enfermedades relacionadas
                if enfermedad_formset:
                    enfermedades = enfermedad_formset.save(commit=False)
                    for enfermedad in enfermedades:
                        enfermedad.residente = residente  # Asociar al residente
                        enfermedad.save()
                    for enfermedad in enfermedad_formset.deleted_objects:
                        enfermedad.delete()

                # Guardar los medicamentos relacionados
                if medicamento_formset:
                    medicamentos = medicamento_formset.save(commit=False)
                    for medicamento in medicamentos:
                        medicamento.residente = residente  # Asociar al residente
                        medicamento.save()
                    for medicamento in medicamento_formset.deleted_objects:
                        medicamento.delete()

                # Redirigir tras el éxito
                return redirect('residentes')  # Asegúrate de que esta URL existe

    context = {
        'residente_form': residente_form,
        'enfermedad_formset': enfermedad_formset,
        'medicamento_formset': medicamento_formset,
    }
    return render(request, 'pages/crear_residente.html', context)