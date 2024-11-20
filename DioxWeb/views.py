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
    enfermedades = ResidenteEnfermedad.objects.filter(residente=residente)
    medicamentos = ResidenteMedicamento.objects.filter(residente=residente)
    return render(request, 'pages/detalle_residente.html', {
        'residente': residente,
        'enfermedades': enfermedades,
        'medicamentos': medicamentos,
    })

def detalle_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    return render(request, 'pages/detalle_empleado.html', {'empleado': empleado})

def crear_residente(request):
    # Formulario principal para Residente
    residente_form = ResidenteForm(request.POST or None, request.FILES or None)

    # Crear formsets
    ResidenteEnfermedadFormSet = inlineformset_factory(
        Residente, ResidenteEnfermedad, form=ResidenteEnfermedadForm, extra=1, can_delete=True
    )
    ResidenteMedicamentoFormSet = inlineformset_factory(
        Residente, ResidenteMedicamento, form=ResidenteMedicamentoForm, extra=1, can_delete=True
    )

    enfermedad_formset = ResidenteEnfermedadFormSet(request.POST or None, instance=None)
    medicamento_formset = ResidenteMedicamentoFormSet(request.POST or None, instance=None)

    if request.method == 'POST':
        if residente_form.is_valid():
            # Guardar el residente
            residente = residente_form.save(commit=False)
            residente.save()

            # Asociar el residente al formset
            enfermedad_formset = ResidenteEnfermedadFormSet(request.POST, instance=residente)
            medicamento_formset = ResidenteMedicamentoFormSet(request.POST, instance=residente)

            if enfermedad_formset.is_valid() and medicamento_formset.is_valid():
                # Guardar enfermedades y medicamentos relacionados
                enfermedad_formset.save()
                medicamento_formset.save()

                # Redirigir tras el éxito
                return redirect('residentes')  # Cambia 'residentes' a la URL correcta

    context = {
        'residente_form': residente_form,
        'enfermedad_formset': enfermedad_formset,
        'medicamento_formset': medicamento_formset,
    }
    return render(request, 'pages/crear_residente.html', context)