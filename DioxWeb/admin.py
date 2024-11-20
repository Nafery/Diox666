from django.contrib import admin
from .models import Residente, Rol, Empleado, Cuidado, Incidencia, Medicamento, ResidenteMedicamento, ResidenteEnfermedad, Enfermedad

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