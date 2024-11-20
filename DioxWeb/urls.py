from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('residentes/', views.lista_residentes, name='residentes'),
    path('empleados/', views.lista_empleados, name='empleados'),
    path('residentes/<int:id>/', views.detalle_residente, name='detalle_residente'),
    path('crear_residente/', views.crear_residente, name='crear_residente'),
    path('empleados/<int:id>/', views.detalle_empleado, name='detalle_empleado'),
]