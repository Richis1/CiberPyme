from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Curso, ProgresoCurso, Pregunta, Opcion

class CursoExamenTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testemployee', password='testpassword')
        self.client = Client()
        self.client.login(username='testemployee', password='testpassword')
        
        # Create course
        self.curso = Curso.objects.create(
            titulo="Test Phishing",
            descripcion="Curso de prueba",
            orden=1,
            puntos=100
        )
        
        # Create progress (state: en_curso, ultima_pagina: 5)
        self.progreso = ProgresoCurso.objects.create(
            usuario=self.user,
            curso=self.curso,
            estado='en_curso',
            porcentaje=50,
            ultima_pagina=5
        )
        
        # Create 10 questions to easily calculate percentages
        self.preguntas = []
        for i in range(10):
            p = Pregunta.objects.create(curso=self.curso, texto=f"Pregunta {i}", orden=i)
            # 1 correct option, 1 incorrect
            o_correcta = Opcion.objects.create(pregunta=p, texto="Correcta", es_correcta=True)
            o_incorrecta = Opcion.objects.create(pregunta=p, texto="Incorrecta", es_correcta=False)
            self.preguntas.append((p, o_correcta, o_incorrecta))

    def test_exam_pass_marks_completed(self):
        # POST with 8 correct answers (80% score) and 2 incorrect answers
        post_data = {}
        for i, (p, o_correcta, o_incorrecta) in enumerate(self.preguntas):
            if i < 8:
                post_data[f"pregunta_{p.id}"] = o_correcta.id
            else:
                post_data[f"pregunta_{p.id}"] = o_incorrecta.id
                
        response = self.client.post(reverse('ver_curso', args=[self.curso.id]), post_data)
        
        # Verify redirect to course view with score in URL
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"?puntuacion=80", response.url)
        
        # Verify progress is updated to completed
        self.progreso.refresh_from_db()
        self.assertEqual(self.progreso.estado, 'completado')
        self.assertEqual(self.progreso.porcentaje, 100)
        self.assertIsNotNone(self.progreso.fecha_completado)

    def test_exam_fail_resets_progress(self):
        # POST with 5 correct answers (50% score) and 5 incorrect answers
        post_data = {}
        for i, (p, o_correcta, o_incorrecta) in enumerate(self.preguntas):
            if i < 5:
                post_data[f"pregunta_{p.id}"] = o_correcta.id
            else:
                post_data[f"pregunta_{p.id}"] = o_incorrecta.id
                
        response = self.client.post(reverse('ver_curso', args=[self.curso.id]), post_data)
        
        # Verify redirect to course view with score in URL
        self.assertEqual(response.status_code, 302)
        self.assertIn(f"?puntuacion=50", response.url)
        
        # Verify progress is reset: state=en_curso, porcentaje=0, ultima_pagina=0
        self.progreso.refresh_from_db()
        self.assertEqual(self.progreso.estado, 'en_curso')
        self.assertEqual(self.progreso.porcentaje, 0)
        self.assertEqual(self.progreso.ultima_pagina, 0)

    def test_descargar_diploma_renders(self):
        # Mark course as completed
        self.progreso.estado = 'completado'
        self.progreso.save()
        
        response = self.client.get(reverse('descargar_diploma', args=[self.curso.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Julio Cesar Gonzalez Rosado")
        self.assertContains(response, "firma_julio")
