from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    orden = models.IntegerField(default=0)
    puntos = models.IntegerField(default=100)
    icono = models.CharField(max_length=50, default='bi-journal-text') # Clase de icono de Bootstrap
    video = models.FileField(upload_to='cursos/videos/', null=True, blank=True)

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.titulo

class ProgresoCurso(models.Model):
    STATUS_CHOICES = [
        ('bloqueado', 'Bloqueado'),
        ('disponible', 'Disponible'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresos')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bloqueado')
    porcentaje = models.IntegerField(default=0)
    ultima_pagina = models.IntegerField(default=0)
    fecha_completado = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('usuario', 'curso')
        verbose_name_plural = "Progresos de Cursos"

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo} ({self.estado})"

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    empresa = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='empleados_asociados')
    curp = models.CharField(max_length=18, unique=True, null=True, blank=True)
    rfc = models.CharField(max_length=13, unique=True, null=True, blank=True)
    nombre_empresa = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    notas = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.get_or_create(usuario=instance)

class ContenidoCurso(models.Model):
    curso = models.ForeignKey(Curso, related_name='contenidos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, blank=True)
    texto = models.TextField(blank=True, help_text="Contenido en texto o descripción de la imagen.")
    imagen = models.FileField(upload_to='cursos/slides/', null=True, blank=True)
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Contenidos de Curso"

    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo or 'Slide ' + str(self.orden)}"

class Pregunta(models.Model):
    curso = models.ForeignKey(Curso, related_name='preguntas', on_delete=models.CASCADE)
    texto = models.TextField()
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return f"{self.curso.titulo} - {self.texto[:50]}"

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Opciones"

    def __str__(self):
        return self.texto

class MaterialCurso(models.Model):
    curso = models.ForeignKey(Curso, related_name='materiales', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='cursos/materiales/')

    class Meta:
        verbose_name_plural = "Materiales de Curso"

    def __str__(self):
        return f"{self.curso.titulo} - {self.nombre}"

class AlertaSeguridad(models.Model):
    NIVEL_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES, default='media')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Alertas de Seguridad"
        ordering = ['-fecha']

    def __str__(self):
        return self.get_nivel_display() + " - " + self.titulo

class Simulacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='bi-shield-shaded')
    puntos = models.IntegerField(default=50)

    class Meta:
        verbose_name_plural = "Simulaciones"

    def __str__(self):
        return self.titulo

class DesafioSimulacion(models.Model):
    simulacion = models.ForeignKey(Simulacion, related_name='desafios', on_delete=models.CASCADE)
    imagen = models.FileField(upload_to='simulaciones/')
    texto_complementario = models.TextField(blank=True, help_text="Texto opcional para dar contexto al desafío.")
    es_peligro = models.BooleanField(default=False, help_text="¿Es una amenaza real?")
    explicacion = models.TextField(help_text="Explicación que se mostrará al usuario como feedback.")

    class Meta:
        verbose_name_plural = "Desafíos de Simulación"

class ProgresoSimulacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresos_simulaciones')
    simulacion = models.ForeignKey(Simulacion, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    puntaje = models.IntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'simulacion')
        verbose_name_plural = "Progresos de Simulaciones"

    def __str__(self):
        return f"{self.usuario.username} - {self.simulacion.titulo}"
