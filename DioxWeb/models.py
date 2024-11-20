from django.db import models
from django.core.exceptions import ValidationError
import re
from django.utils import timezone

# Función para validar el RUT
def validar_rut(value):
    rut_pattern = re.compile(r'^\d{1,8}-[\dkK]$')
    if not rut_pattern.match(value):
        raise ValidationError('El RUT no tiene un formato válido (Ej: 12345678-9).')

class GeneroChoices(models.TextChoices):
    MASCULINO = 'M', 'Masculino'
    FEMENINO = 'F', 'Femenino'
    OTRO = 'O', 'Otro'

class Residente(models.Model):
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])  # RUT con validación
    nombre = models.CharField(max_length=100)
    ap_paterno = models.CharField(max_length=100)
    ap_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10, choices=GeneroChoices.choices)
    contacto_emergencia = models.CharField(max_length=100)
    telefono_emergencia = models.CharField(max_length=15)
    habitacion = models.CharField(max_length=10, unique=True)
    observaciones = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='residentes/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.ap_paterno} - Habitación {self.habitacion}"

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    nombre = models.CharField(max_length=100)
    ap_paterno = models.CharField(max_length=100)
    ap_materno = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    fecha_contratacion = models.DateField()
    direccion = models.CharField(max_length=200)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(upload_to='imagenes/empleados/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.ap_paterno} - {self.rol.nombre if self.rol else 'Sin Rol'}"

class Cuidado(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    descripcion = models.TextField()
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cuidado de {self.residente.nombre} por {self.empleado.nombre} ({self.fecha_creacion.date()})"

class Incidencia(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    descripcion = models.TextField()
    resuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"Incidencia de {self.residente.nombre} - {'Resuelta' if self.resuelto else 'Pendiente'}"

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    dosis_recomendada = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Enfermedad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    cronica = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class ResidenteEnfermedad(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    enfermedad = models.ForeignKey(Enfermedad, on_delete=models.CASCADE)
    fecha_diagnostico = models.DateField()
    tratamiento = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.residente.nombre} - {self.enfermedad.nombre}"

class ResidenteMedicamento(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    dosis = models.CharField(max_length=50)
    frecuencia = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['residente', 'medicamento', 'fecha_inicio'], name='unique_residente_medicamento')
        ]

    def __str__(self):
        return f"{self.residente.nombre} - {self.medicamento.nombre}"
