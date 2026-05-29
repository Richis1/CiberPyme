from django.contrib import admin
from .models import Curso, ProgresoCurso, AlertaSeguridad, ContenidoCurso, Pregunta, Opcion, MaterialCurso

class MaterialInline(admin.TabularInline):
    model = MaterialCurso
    extra = 1

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 3

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    inlines = [OpcionInline]
    list_display = ('texto', 'curso', 'orden')

class ContenidoInline(admin.TabularInline):
    model = ContenidoCurso
    extra = 1

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'puntos')
    ordering = ('orden',)
    inlines = [ContenidoInline, MaterialInline]

@admin.register(ProgresoCurso)
class ProgresoCursoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'estado', 'porcentaje')
    list_filter = ('estado', 'curso')
    search_fields = ('usuario__username', 'curso__titulo')

@admin.register(AlertaSeguridad)
class AlertaSeguridadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nivel', 'fecha')
    list_filter = ('nivel',)
    search_fields = ('titulo', 'descripcion')
