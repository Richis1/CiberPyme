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
        # Note: Depending on template contents, we just check success
        self.assertContains(response, "Diploma")

class SecurityOWASPTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='securityuser', password='password123', first_name="<b>XSS_Test</b>")

    def test_csrf_protection_enforced(self):
        """Verify that POST requests fail without a CSRF token when checks are enforced"""
        client = Client(enforce_csrf_checks=True)
        # Try to post login without CSRF token
        response = client.post(reverse('login'), {'username': 'securityuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 403) # Forbidden due to lack of CSRF token

    def test_sql_injection_protection(self):
        """Verify Django ORM prevents SQL Injection through automatic parameterization"""
        sql_injection_payload = "' OR '1'='1"
        # Try to retrieve user with payload as username
        user_exists = User.objects.filter(username=sql_injection_payload).exists()
        self.assertFalse(user_exists)

    def test_xss_auto_escaping_in_templates(self):
        """Verify that HTML output is automatically escaped by Django templates to prevent XSS"""
        self.client.login(username='securityuser', password='password123')
        # Access a page where first_name is displayed. Let's assign user to group Empresas to see dashboard
        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name='Empresas')
        self.user.groups.add(group)
        
        response = self.client.get(reverse('empresa_dashboard'))
        self.assertEqual(response.status_code, 200)
        # The raw tag <b> should be escaped as &lt;b&gt; to prevent XSS execution
        self.assertContains(response, "&lt;b&gt;XSS_Test&lt;/b&gt;")
        self.assertNotContains(response, "<b>XSS_Test</b>")

    def test_curp_rfc_encryption_in_db(self):
        """Verify that CURP and RFC fields of Perfil are encrypted in DB and decrypted via properties"""
        from .models import Perfil
        perfil = self.user.perfil
        perfil.curp = "ABCD123456HDFRND01"
        perfil.rfc = "ABCD123456123"
        perfil.save()
        
        # Reload from database directly using values() to check the raw database content
        raw_db_values = Perfil.objects.filter(id=perfil.id).values('curp', 'rfc').first()
        
        # Verify that the database stores encrypted values (different from raw values)
        self.assertNotEqual(raw_db_values['curp'], "ABCD123456HDFRND01")
        self.assertNotEqual(raw_db_values['rfc'], "ABCD123456123")
        self.assertTrue(raw_db_values['curp'].startswith("gAAAAA"))
        self.assertTrue(raw_db_values['rfc'].startswith("gAAAAA"))
        
        # Reload instance and check decrypted properties
        perfil.refresh_from_db()
        self.assertEqual(perfil.curp_desencriptado, "ABCD123456HDFRND01")
        self.assertEqual(perfil.rfc_desencriptado, "ABCD123456123")


