from django.forms import inlineformset_factory
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Residente, Empleado, ResidenteEnfermedad, ResidenteMedicamento, Enfermedad, Medicamento, Incidencia
from .forms import ResidenteForm, ResidenteEnfermedadForm, ResidenteMedicamentoForm, EmpleadoLoginForm, EmpleadoRegistroForm
from django.contrib.auth.decorators import login_required
from .decorators import role_required

# Create your views here.

@login_required
def index(request):
    context = {}
    return render(request, 'pages/index.html', context)

@role_required(roles=["Cuidador", "Medico", "Enfermero", "Administrador"])
@login_required
def lista_residentes(request):
    residentes = Residente.objects.all()
    return render(request, 'pages/lista_residentes.html', {'residentes': residentes})

@role_required(roles=["Administrador"])
@login_required
def eliminar_residente(request, pk):
    # Verificar que la solicitud sea POST
    if request.method == "POST":
        try:
            # Obtener el residente o lanzar 404 si no existe
            residente = get_object_or_404(Residente, pk=pk)
            # Eliminar el residente
            residente.delete()
            # Mostrar mensaje de éxito
            messages.success(request, f"Residente {residente.nombre} {residente.ap_paterno} eliminado con éxito.")
        except Exception as e:
            # Manejar posibles errores de eliminación
            messages.error(request, f"Hubo un error al intentar eliminar el residente: {e}")
    else:
        # Redirigir si el método no es POST
        messages.warning(request, "Acción no permitida. Solo se permiten solicitudes POST para eliminar residentes.")
    
    # Redirigir a la lista de residentes
    return redirect('residentes')

@role_required(roles=["Administrador"])
@login_required
def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'pages/lista_empleados.html', {'empleados': empleados})

@role_required(roles=["Administrador", "Cuidador", "Medico", "Enfermero"])
@login_required
def detalle_residente(request, id):
    # Obtener el residente
    residente = get_object_or_404(Residente, id=id)

    # Obtener las enfermedades, medicamentos e incidencias actuales del residente
    enfermedades = ResidenteEnfermedad.objects.filter(residente=residente)
    medicamentos = ResidenteMedicamento.objects.filter(residente=residente)
    incidencias = Incidencia.objects.filter(residente=residente)
    
    # Enfermedades no asignadas al residente
    enfermedades_disponibles = Enfermedad.objects.exclude(
        id__in=enfermedades.values_list('enfermedad_id', flat=True)
    )
    
    # Medicamentos no asignados al residente
    medicamentos_disponibles = Medicamento.objects.exclude(
        id__in=medicamentos.values_list('medicamento_id', flat=True)
    )

    # Manejar formulario para agregar enfermedades
    if request.method == "POST" and "agregar_enfermedad" in request.POST:
        enfermedad_id = request.POST.get("enfermedad")
        fecha_diagnostico = request.POST.get("fecha_diagnostico")
        tratamiento = request.POST.get("tratamiento")
        
        if enfermedad_id:
            enfermedad = get_object_or_404(Enfermedad, id=enfermedad_id)
            ResidenteEnfermedad.objects.create(
                residente=residente,
                enfermedad=enfermedad,
                fecha_diagnostico=fecha_diagnostico,
                tratamiento=tratamiento,
            )
            return redirect("detalle_residente", id=id)
    
    # Manejar formulario para agregar medicamentos
    if request.method == "POST" and "agregar_medicamento" in request.POST:
        medicamento_id = request.POST.get("medicamento")
        dosis = request.POST.get("dosis")
        frecuencia = request.POST.get("frecuencia")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        observaciones = request.POST.get("observaciones")
        
        if medicamento_id:
            medicamento = get_object_or_404(Medicamento, id=medicamento_id)
            ResidenteMedicamento.objects.create(
                residente=residente,
                medicamento=medicamento,
                dosis=dosis,
                frecuencia=frecuencia,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                observaciones=observaciones,
            )
            return redirect("detalle_residente", id=id)

    # Manejar formulario para agregar incidencias
    if request.method == "POST" and "agregar_incidencia" in request.POST:
        descripcion = request.POST.get("descripcion")
        
        if descripcion:
            Incidencia.objects.create(
                residente=residente,
                descripcion=descripcion,
                resuelto=False,  # Marcar como no resuelta por defecto
            )
            return redirect("detalle_residente", id=id)

    # Marcar una incidencia como resuelta
    if request.method == "POST" and "marcar_resuelto" in request.POST:
        incidencia_id = request.POST.get("incidencia_id")
        
        if incidencia_id:
            incidencia = get_object_or_404(Incidencia, id=incidencia_id)
            incidencia.resuelto = True
            incidencia.save()
            return redirect("detalle_residente", id=id)
    
    # Formulario para editar los datos del residente
    if request.method == "POST" and "editar_residente" in request.POST:
        form = ResidenteForm(request.POST, request.FILES, instance=residente)
        if form.is_valid():
            form.save()
            return redirect("detalle_residente", id=id)
    else:
        form = ResidenteForm(instance=residente)

    return render(request, 'pages/detalle_residente.html', {
        'residente': residente,
        'enfermedades': enfermedades,
        'medicamentos': medicamentos,
        'incidencias': incidencias,
        'enfermedades_disponibles': enfermedades_disponibles,
        'medicamentos_disponibles': medicamentos_disponibles,
        'form': form,  # Pasar el formulario para edición
    })


@role_required(roles=["Administrador"])
@login_required
def detalle_empleado(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    return render(request, 'pages/detalle_empleado.html', {'empleado': empleado})

@role_required(roles=["Administrador"])
@login_required
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
                return redirect('residentes')

    context = {
        'residente_form': residente_form,
        'enfermedad_formset': enfermedad_formset,
        'medicamento_formset': medicamento_formset,
    }
    return render(request, 'pages/crear_residente.html', context)

@role_required(roles=["Administrador"])
@login_required
def lista_enfermedades(request):
    enfermedades = Enfermedad.objects.all()
    return render(request, 'pages/lista_enfermedades.html', {'enfermedades': enfermedades})


def login_empleado(request):
    if request.method == 'POST':
        form = EmpleadoLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = EmpleadoLoginForm()
    return render(request, 'pages/login_empleado.html', {'form': form})

@role_required(roles=["Administrador"])
@login_required
def registrar_empleado(request):
    if request.method == "POST":
        form = EmpleadoRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear el usuario
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            # Crear el empleado asociado al usuario
            empleado = form.save(commit=False)
            empleado.user = user
            empleado.save()

            messages.success(request, "Empleado registrado exitosamente.")
    else:
        form = EmpleadoRegistroForm()
    
    return render(request, 'pages/registro_empleado.html', {'form': form})