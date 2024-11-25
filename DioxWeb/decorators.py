# myapp/decorators.py
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Empleado

# Decorador para verificar el rol
def role_required(roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            # Verificar si el usuario está autenticado
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Acceso denegado: Inicie sesión.")
            
            # Verificar si el usuario es superusuario
            if request.user.is_superuser:
                # Si es superusuario, permitir acceso a todas las páginas
                return view_func(request, *args, **kwargs)
            
            # Obtener el rol del empleado
            try:
                empleado = request.user.empleado
                if empleado.rol.nombre in roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("Acceso denegado: No tiene permiso para ver esta página.")
            except Empleado.DoesNotExist:
                return HttpResponseForbidden("Acceso denegado: No es un empleado registrado.")
        return _wrapped_view
    return decorator
