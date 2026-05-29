from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacidad/', views.privacidad, name='privacidad'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('empresa/', views.empresa_dashboard, name='empresa_dashboard'),
    path('empleado/', views.empleado_dashboard, name='empleado_dashboard'),
    path('cursos/', views.cursos, name='cursos'),
    path('diplomas/', views.diplomas, name='diplomas'),
    path('descargar-diploma/<int:curso_id>/', views.descargar_diploma, name='descargar_diploma'),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('lista-usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('gestionar-cursos/', views.gestionar_cursos, name='gestionar_cursos'),
    path('auditoria/', views.auditoria, name='auditoria'),
    path('crear-curso/', views.crear_curso, name='crear_curso'),
    path('editar-curso/<int:curso_id>/', views.editar_curso, name='editar_curso'),
    path('ver-curso/<int:curso_id>/', views.ver_curso, name='ver_curso'),
    path('eliminar-curso/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'),

    # Simulaciones
    path('simulaciones/', views.simulaciones, name='simulaciones'),
    path('ejecutar-simulacion/<int:sim_id>/', views.ejecutar_simulacion, name='ejecutar_simulacion'),
    path('gestionar-simulaciones/', views.gestionar_simulaciones, name='gestionar_simulaciones'),
    path('crear-simulacion/', views.crear_simulacion, name='crear_simulacion'),
    path('editar-simulacion/<int:sim_id>/', views.editar_simulacion, name='editar_simulacion'),
    path('eliminar-simulacion/<int:sim_id>/', views.eliminar_simulacion, name='eliminar_simulacion'),

    path('login/', auth_views.LoginView.as_view(template_name='principal/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('registro-empresa/', views.registro_empresa, name='registro_empresa'),
    path('confirmar-registro/<str:uidb64>/<str:token>/', views.confirmar_registro, name='confirmar_registro'),
    path('confirmar-empleado/<str:uidb64>/<str:token>/', views.confirmar_contrasena_empleado, name='confirmar_contrasena_empleado'),
    
    # API endpoints for JWT Secure Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
