from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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
    habitacion = models.CharField(max_length=10)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = 1)
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

class Analgesico(Medicamento):
    tipo = models.CharField(max_length=100, choices=[('opioide', 'Opioide'), ('no_opioide', 'No Opioide')])

    def __str__(self):
        return f"Analgesico: {self.nombre}"

class Antidepresivo(Medicamento):
    clasificacion = models.CharField(max_length=100, choices=[('ISRS', 'Inhibidores selectivos de la recaptación de serotonina'),
                                                                ('IRSN', 'Inhibidores de la recaptación de serotonina y noradrenalina')])

    def __str__(self):
        return f"Antidepresivo: {self.nombre}"

class Antiinflamatorio(Medicamento):
    tipo = models.CharField(max_length=100, choices=[('esteroide', 'Esteroide'), ('no_esteroide', 'No Esteroide')])

    def __str__(self):
        return f"Antiinflamatorio: {self.nombre}"

class Antibiotico(Medicamento):
    clase = models.CharField(max_length=100, choices=[('penicilina', 'Penicilina'), 
                                                      ('cefalosporina', 'Cefalosporina'),
                                                      ('macrolidos', 'Macrólidos'),
                                                      ('quinolonas', 'Quinolonas')])
    
    def __str__(self):
        return f"Antibiótico: {self.nombre}"

class Antihipertensivo(Medicamento):
    clase = models.CharField(max_length=100, choices=[('IECA', 'Inhibidores de la Enzima Convertidora de Angiotensina'), 
                                                      ('ARA', 'Antagonistas de los Receptores de Angiotensina'),
                                                      ('diuretico', 'Diurético'),
                                                      ('beta_bloqueante', 'Beta-bloqueante')])
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Antihipertensivo: {self.nombre}"

class Antialergico(Medicamento):
    tipo = models.CharField(max_length=100, choices=[('antihistaminico', 'Antihistamínico'),
                                                     ('corticosteroide', 'Corticosteroide'),
                                                     ('leucotrieno', 'Antagonista de Leucotrienos')])
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Antialérgico: {self.nombre}"

class Ansiolitico(Medicamento):
    clasificacion = models.CharField(max_length=100, choices=[('benzodiazepinas', 'Benzodiazepinas'),
                                                              ('no_benzodiazepinas', 'No Benzodiazepinas')])
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Ansiolítico: {self.nombre}"

class Antidiabetico(Medicamento):
    tipo = models.CharField(max_length=100, choices=[('insulina', 'Insulina'),
                                                     ('biguanidas', 'Biguanidas'),
                                                     ('sulfonilureas', 'Sulfonilureas')])
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Antidiabético: {self.nombre}"

class Estimulante(Medicamento):
    clasificacion = models.CharField(max_length=100, choices=[('anfetamina', 'Anfetamina'),
                                                              ('metilfenidato', 'Metilfenidato')])
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Estimulante: {self.nombre}"

class Antipsicotico(Medicamento):
    tipo = models.CharField(max_length=100, choices=[('atipico', 'Atípico'),
                                                     ('tipico', 'Típico')])
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Antipsicótico: {self.nombre}"

class Laxante(Medicamento):
    tipo = models.CharField(max_length=100, choices=[('irritante', 'Irritante'),
                                                     ('formador_de_masa', 'Formador de Masa'),
                                                     ('lubricante', 'Lubricante')])
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Laxante: {self.nombre}"

class Vacuna(Medicamento):
    enfermedad_previene = models.CharField(max_length=100)
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Vacuna: {self.nombre}"

class Anticonceptivo(Medicamento):
    tipo = models.CharField(max_length=100, choices=[('oral', 'Oral'),
                                                     ('inyectable', 'Inyectable'),
                                                     ('implante', 'Implante'),
                                                     ('condon', 'Condón')])
    # Otros campos específicos pueden ser agregados si es necesario
    
    def __str__(self):
        return f"Anticonceptivo: {self.nombre}"


class Enfermedad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    cronica = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class ResidenteEnfermedad(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='enfermedades')
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
