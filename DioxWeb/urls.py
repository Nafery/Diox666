from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.index, name='index'),
    path('residentes/', views.lista_residentes, name='residentes'),
    path('empleados/', views.lista_empleados, name='empleados'),
    path('residentes/<int:id>/', views.detalle_residente, name='detalle_residente'),
    path('residentes/eliminar/<int:pk>/', views.eliminar_residente, name='eliminar_residente'),
    path('crear_residente/', views.crear_residente, name='crear_residente'),
    path('empleados/<int:id>/', views.detalle_empleado, name='detalle_empleado'),
    path('enfermedades/', views.lista_enfermedades, name='lista_enfermedades'),
    path('login/', views.login_empleado, name='login_empleado'),
    path('registro/', views.registrar_empleado, name='registro_empleado'),
    path('logout/', LogoutView.as_view(next_page='login_empleado'), name='logout'),
    path('informes/medicamentos/', views.generar_informe_medicamentos, name='generar_informe_medicamentos'),
    path('informes/medicamentos/csv/', views.exportar_informe_medicamentos_csv, name='exportar_informe_medicamentos_csv'),
]