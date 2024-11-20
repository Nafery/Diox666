from django.contrib import admin
from .models import Residente, Rol, Empleado, Cuidado, Incidencia, Medicamento, ResidenteMedicamento, ResidenteEnfermedad, Enfermedad, Analgesico, Antidepresivo, Antiinflamatorio, Antibiotico, Antihipertensivo, Antialergico, Ansiolitico, Antidiabetico, Estimulante, Antipsicotico, Laxante, Vacuna, Anticonceptivo

# Register your models here.

admin.site.register(Residente)
admin.site.register(Rol)
admin.site.register(Empleado)
admin.site.register(Cuidado)
admin.site.register(Incidencia)
admin.site.register(Medicamento)
admin.site.register(ResidenteMedicamento)
admin.site.register(ResidenteEnfermedad)
admin.site.register(Enfermedad)
admin.site.register(Analgesico)
admin.site.register(Antidepresivo)
admin.site.register(Antiinflamatorio)
admin.site.register(Antibiotico)
admin.site.register(Antihipertensivo)
admin.site.register(Antialergico)
admin.site.register(Ansiolitico)
admin.site.register(Antidiabetico)
admin.site.register(Estimulante)
admin.site.register(Antipsicotico)
admin.site.register(Laxante)
admin.site.register(Vacuna)
admin.site.register(Anticonceptivo)