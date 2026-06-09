from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import os
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .models import (
    Curso, ProgresoCurso, Perfil, ContenidoCurso, 
    Pregunta, Opcion, MaterialCurso, AlertaSeguridad,
    Simulacion, DesafioSimulacion, ProgresoSimulacion
)

def eliminar_archivo_fisico(archivo):
    if archivo and hasattr(archivo, 'path') and os.path.isfile(archivo.path):
        try:
            os.remove(archivo.path)
        except Exception as e:
            print(f"Error borrando archivo: {e}")

def custom_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'principal/landing.html')
        
    if request.user.is_staff:
        return redirect('admin_dashboard')
    if request.user.groups.filter(name='Empresas').exists():
        return redirect('empresa_dashboard')
    if request.user.groups.filter(name='Empleados').exists():
        return redirect('empleado_dashboard')
        
    return render(request, 'principal/landing.html')

def privacidad(request):
    return render(request, 'principal/privacidad.html')

def cursos(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    from .models import Curso
    cursos = Curso.objects.all().order_by('orden')
    return render(request, 'principal/cursos.html', {'cursos': cursos})

@login_required
def diplomas(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
        
    from .models import ProgresoCurso
    
  
    if request.user.groups.filter(name='Empresas').exists():
        from django.contrib.auth.models import User
        # Obtener 'completado' solo para empleados de esta empresa
        progresos = ProgresoCurso.objects.filter(
            usuario__perfil__empresa=request.user, 
            estado='completado'
        ).select_related('curso', 'usuario')
        context = {'is_company': True, 'progresos': progresos}
        return render(request, 'principal/diplomas.html', context)
    
    # Si es un empleado
    progresos = ProgresoCurso.objects.filter(usuario=request.user, estado='completado').select_related('curso')
    context = {
        'is_company': False,
        'progresos': progresos
    }
    return render(request, 'principal/diplomas.html', context)

@login_required
def descargar_diploma(request, curso_id):
    from .models import Curso, ProgresoCurso
    import datetime
    
    curso = get_object_or_404(Curso, id=curso_id)
    usuario_id = request.GET.get('usuario_id')
    
    if usuario_id:
        target_user = get_object_or_404(User, id=usuario_id)
        # Validar permisos
        tiene_permiso = request.user.is_staff
        if not tiene_permiso and request.user.groups.filter(name='Empresas').exists():
            try:
                tiene_permiso = (target_user.perfil.empresa == request.user)
            except Exception:
                tiene_permiso = False
        if not tiene_permiso:
            tiene_permiso = (request.user == target_user)
            
        if not tiene_permiso:
            messages.error(request, 'No tienes permiso para ver este diploma.')
            return redirect('home')
    else:
        target_user = request.user

    progreso = get_object_or_404(ProgresoCurso, usuario=target_user, curso=curso)
    if progreso.estado != 'completado' and not request.user.is_staff:
        messages.error(request, 'El usuario aún no ha completado este curso.')
        return redirect('home')
    
    # Usar la fecha de finalización del progreso (fecha_completado)
    fecha_diploma = progreso.fecha_completado if progreso.fecha_completado else datetime.datetime.now()
    
    context = {
        'curso': curso,
        'user': target_user,
        'fecha_hoy': fecha_diploma
    }
    return render(request, 'principal/diploma_formato.html', context)

@staff_member_required
def admin_dashboard(request):
    from .models import AlertaSeguridad
    alertas = AlertaSeguridad.objects.all()
    return render(request, 'principal/admin_dashboard.html', {'alertas': alertas})

@login_required
def empresa_dashboard(request):
    from django.contrib.auth.models import Group
    from .models import Curso, ProgresoCurso, Perfil
    
    if not request.user.groups.filter(name='Empresas').exists() and not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        # Alta de empleado y hasheo 
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El CURP ya está registrado.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
        else:
            # SEGURIDAD: Cifra la contraseña del empleado con PBKDF2-SHA256 al crear el usuario
            user = User.objects.create_user(username, email, password)
            user.is_active = True  # Activo inmediatamente ya que tiene contraseña establecida
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            # Vincular a esta empresa y guardar CURP
            perfil, _ = Perfil.objects.get_or_create(usuario=user)
            perfil.empresa = request.user
            perfil.curp = username  # El usuario es el CURP
            perfil.save()
            
            group, _ = Group.objects.get_or_create(name='Empleados')
            user.groups.add(group)
            
            # Crear progreso de cursos base para el nuevo empleado
            cursos = Curso.objects.all()
            for curso in cursos:
                estado = 'en_curso' if curso.orden == 1 else 'bloqueado'
                ProgresoCurso.objects.get_or_create(
                    usuario=user,
                    curso=curso,
                    defaults={'estado': estado, 'porcentaje': 0}
                )
            
            # Enviar Correo de Credenciales (Formato Premium HTML)
            try:
                login_url = f"{request.scheme}://{request.get_host()}/login/"
                context_email = {
                    'first_name': first_name,
                    'username': username,
                    'password': password,
                    'login_url': login_url
                }
                
                html_message = render_to_string('emails/credenciales.html', context_email)
                plain_message = strip_tags(html_message)
                
                asunto = 'Bienvenido a CyberPyme - Tus Credenciales de Acceso'
                
                send_mail(
                    asunto,
                    plain_message,
                    None, # Usa DEFAULT_FROM_EMAIL
                    [email],
                    html_message=html_message
                )
                messages.success(request, f'Empleado "{first_name}" dado de alta. Se ha enviado un correo con sus credenciales.')
            except Exception as e:
                print(f"Error enviando correo: {e}")
                messages.warning(request, f'Empleado creado, pero hubo un detalle al enviar el correo con las credenciales.')
 
            return redirect('empresa_dashboard')

    # Filtrar empleados por empresa (multi-tenancy)
    if request.user.is_staff:
        # El personal del staff ve todos los empleados
        empleados = User.objects.filter(groups__name='Empleados').prefetch_related('progresos', 'progresos__curso')
    else:
        # Las empresas solo ven a sus propios empleados
        empleados = User.objects.filter(perfil__empresa=request.user).prefetch_related('progresos', 'progresos__curso')
    
    total_empleados = empleados.count()
    completados = 0
    total_progresos = 0
    total_simulaciones = 0
    empleados_stats = []
    
    for emp in empleados:
        progs = emp.progresos.all()
        emp_total = progs.count()
        emp_completados = sum(1 for p in progs if p.estado == 'completado')
        emp_percent = (emp_completados * 100 // emp_total) if emp_total > 0 else 0
        
        total_simulaciones += progs.filter(porcentaje__gt=0).count()
        
        empleados_stats.append({
            'empleado': emp,
            'porcentaje': emp_percent,
            'progresos': progs
        })
        
        completados += emp_completados
        total_progresos += emp_total
        
    avg_capacitacion = (completados * 100 // total_progresos) if total_progresos > 0 else 0
    
    # Calcular Nivel de Riesgo
    if avg_capacitacion >= 80:
        riesgo_global = "Bajo"
        riesgo_color = "success"
    elif avg_capacitacion >= 50:
        riesgo_global = "Medio"
        riesgo_color = "warning"
    else:
        riesgo_global = "Alto"
        riesgo_color = "danger"
    
    context = {
        'total_empleados': total_empleados,
        'avg_capacitacion': avg_capacitacion,
        'total_simulaciones': total_simulaciones,
        'riesgo_global': riesgo_global,
        'riesgo_color': riesgo_color,
        'empleados_stats': empleados_stats,
    }
    
    return render(request, 'principal/empresa_dashboard.html', context)

@login_required
def empleado_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    if request.user.groups.filter(name='Empresas').exists():
        return redirect('empresa_dashboard')
        
    from .models import Curso, ProgresoCurso, AlertaSeguridad
    from django.contrib.auth.models import User
    
    # Asegurar que existan cursos base
    if not Curso.objects.exists():
        Curso.objects.create(titulo="Phishing 101", descripcion="Identificación de correos maliciosos", orden=1, puntos=100, icono='bi-shield-check')
        Curso.objects.create(titulo="Buenas Prácticas de Contraseñas", descripcion="Seguridad en accesos", orden=2, puntos=150, icono='bi-key')
        Curso.objects.create(titulo="Ransomware Básico", descripcion="Prevención de secuestro de datos", orden=3, puntos=200, icono='bi-unlock')

    # Asegurar que el usuario tenga registros de progreso
    cursos = Curso.objects.all()
    for curso in cursos:
        # Todos inician en 0% por defecto según petición del usuario
        estado = 'en_curso' if curso.orden == 1 else 'bloqueado'
        
        ProgresoCurso.objects.get_or_create(
            usuario=request.user, 
            curso=curso,
            defaults={'estado': estado, 'porcentaje': 0}
        )

    progresos = ProgresoCurso.objects.filter(usuario=request.user).select_related('curso').order_by('curso__orden')
    alertas = AlertaSeguridad.objects.all()[:5]
    
    # Calcular nivel y puntos
    completados = sum(1 for p in progresos if p.estado == 'completado')
    mis_puntos = sum(p.curso.puntos for p in progresos if p.estado == 'completado')
    total_cursos = cursos.count()
    
    if total_cursos > 0:
        nivel_seguridad = min(int((completados / total_cursos) * 10) + 1, 10)
    else:
        nivel_seguridad = 1
        
    # Calcular ranking de la empresa
    ranking = []
    try:
        empresa = request.user.perfil.empresa
        if empresa:
            compañeros = User.objects.filter(perfil__empresa=empresa).prefetch_related('progresos', 'progresos__curso')
        else:
            compañeros = User.objects.filter(id=request.user.id).prefetch_related('progresos', 'progresos__curso')
    except Exception:
        compañeros = User.objects.filter(id=request.user.id).prefetch_related('progresos', 'progresos__curso')
        
    for comp in compañeros:
        pts = sum(p.curso.puntos for p in comp.progresos.all() if p.estado == 'completado')
        ranking.append({
            'empleado': comp,
            'puntos': pts,
            'is_me': comp == request.user
        })
        
    ranking.sort(key=lambda x: x['puntos'], reverse=True)
    ranking = ranking[:5]
    
    context = {
        'progresos': progresos,
        'mis_puntos': mis_puntos,
        'nivel_seguridad': nivel_seguridad,
        'ranking': ranking,
        'alertas': alertas,
    }
    return render(request, 'principal/empleado_dashboard.html', context)
@staff_member_required
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        role = request.POST.get('role')
        curp = request.POST.get('curp')

        if role == 'empleado' and curp:
            username = curp

        if User.objects.filter(username=username).exists():
            messages.error(request, f'El {"CURP" if role=="empleado" else "Nombre de Usuario"} ya está registrado.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
        else:
            if role == 'empleado':
                # Crear inactivo y generar contraseña temporal aleatoria
                temp_password = User.objects.make_random_password()
                # SEGURIDAD: Cifra la contraseña temporal con PBKDF2-SHA256 al crear el usuario
                user = User.objects.create_user(username, email, temp_password)
                user.is_active = False
            elif role == 'admin':
                if not request.user.is_superuser:
                    messages.error(request, 'Solo el adminMaster puede crear otros administradores.')
                    return redirect('admin_dashboard')
                # SEGURIDAD: Cifra la contraseña del administrador con PBKDF2-SHA256 al crear el usuario
                user = User.objects.create_user(username, email, password)
                user.is_staff = True
                user.is_active = True
            else:
                # SEGURIDAD: Cifra la contraseña de la empresa/staff con PBKDF2-SHA256 al crear el usuario
                user = User.objects.create_user(username, email, password)
                
            user.first_name = first_name
            user.last_name = last_name if role not in ('empleado', 'admin') else ''
            user.save()
            
            if role == 'empleado':
                if curp:
                    user.perfil.curp = curp
                empresa_id = request.POST.get('empresa')
                if empresa_id:
                    try:
                        empresa_user = User.objects.get(id=empresa_id, groups__name='Empresas')
                        user.perfil.empresa = empresa_user
                    except User.DoesNotExist:
                        pass
                user.perfil.save()

            from django.contrib.auth.models import Group
            if role == 'empleado':
                group, _ = Group.objects.get_or_create(name='Empleados')
                user.groups.add(group)
            elif role == 'empresa':
                group, _ = Group.objects.get_or_create(name='Empresas')
                user.groups.add(group)
            
            # Enviar Correo (Formato Premium HTML)
            try:
                if role == 'empleado':
                    # SEGURIDAD: Genera un token firmado criptográficamente con HMAC-SHA256
                    token = default_token_generator.make_token(user)
                    # SEGURIDAD: Codifica el ID del usuario en Base64 seguro para URL
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    activacion_url = f"{request.scheme}://{request.get_host()}/confirmar-empleado/{uid}/{token}/"
                    
                    context_email = {
                        'first_name': first_name,
                        'username': username,
                        'activacion_url': activacion_url
                    }
                    html_message = render_to_string('emails/confirmar_contrasena_empleado.html', context_email)
                    asunto = 'Confirma tu Cuenta y Establece tu Contraseña - CyberPyme'
                    success_msg = f'Empleado "{first_name}" creado correctamente y notificado para establecer su contraseña.'
                else:
                    login_url = f"{request.scheme}://{request.get_host()}/login/"
                    context_email = {
                        'first_name': first_name,
                        'username': username,
                        'password': password,
                        'login_url': login_url
                    }
                    html_message = render_to_string('emails/credenciales.html', context_email)
                    asunto = 'Bienvenido a CyberPyme - Tus Credenciales de Acceso'
                    if role == 'admin':
                        success_msg = f'Administrador "{first_name}" creado correctamente y notificado por correo.'
                    else:
                        success_msg = f'Empresa "{first_name}" creada correctamente y notificada por correo.'
                
                plain_message = strip_tags(html_message)
                send_mail(
                    asunto,
                    plain_message,
                    None, # Usa DEFAULT_FROM_EMAIL
                    [email],
                    html_message=html_message
                )
                messages.success(request, success_msg)
            except Exception as e:
                print(f"Error enviando correo: {e}")
                messages.warning(request, f'El usuario fue creado correctamente, pero hubo un detalle al enviar el correo de notificación.')

            return redirect('admin_dashboard')

    empresas = User.objects.filter(groups__name='Empresas').order_by('first_name', 'username')
    return render(request, 'principal/crear_usuario.html', {'empresas': empresas})

@staff_member_required
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'principal/lista_usuarios.html', {'usuarios': usuarios})

@staff_member_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        
        # Los administradores no se pueden desactivar
        if user.is_staff or user.is_superuser:
            user.is_active = True
        else:
            user.is_active = request.POST.get('is_active') == 'on'
        
        # Si se ingresó una nueva contraseña, actualizarla (excepto para administradores)
        if password:
            if user.is_staff or user.is_superuser:
                messages.error(request, 'No está permitido cambiar la contraseña de un administrador desde aquí.')
            else:
                user.set_password(password)
            
        user.save()
        messages.success(request, f'Usuario "{user.username}" actualizado correctamente.')
    return redirect('lista_usuarios')

@staff_member_required
def eliminar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    username = user.username
    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
    elif not user.is_staff and not user.is_superuser:
        messages.error(request, 'No está permitido eliminar a este usuario (empresa/empleado), solo puedes desactivarlo.')
    else:
        user.delete()
        messages.success(request, f'Usuario "{username}" eliminado correctamente.')
    return redirect('lista_usuarios')

@staff_member_required
def toggle_usuario_activo(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.error(request, 'No puedes desactivar tu propio usuario.')
    elif user.is_staff or user.is_superuser:
        messages.error(request, 'Los administradores no se pueden desactivar.')
    else:
        user.is_active = not user.is_active
        user.save()
        estado = "activado" if user.is_active else "desactivado"
        messages.success(request, f'Usuario "{user.username}" {estado} correctamente.')
    return redirect('lista_usuarios')

@staff_member_required
def gestionar_cursos(request):
    from .models import Curso
    cursos = Curso.objects.all().order_by('orden')
    return render(request, 'principal/gestionar_cursos.html', {'cursos': cursos})

@staff_member_required
def crear_curso(request):
    from .models import Curso, ProgresoCurso
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        orden = request.POST.get('orden')
        puntos = request.POST.get('puntos')
        icono = request.POST.get('icono', 'bi-journal-text')
        
        video = request.FILES.get('video')
        
        curso = Curso.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            orden=orden,
            puntos=puntos,
            icono=icono,
            video=video
        )
        
        # Crear progreso para todos los usuarios existentes
        usuarios = User.objects.all()
        for usuario in usuarios:
            # Si no es staff ni empresa (es decir, es empleado)
            if not usuario.is_staff and not usuario.groups.filter(name='Empresas').exists():
                estado = 'en_curso' if str(orden) == '1' else 'bloqueado'
                ProgresoCurso.objects.get_or_create(
                    usuario=usuario,
                    curso=curso,
                    defaults={'estado': estado, 'porcentaje': 0}
                )
        
        messages.success(request, f'Curso "{titulo}" creado correctamente.')
        return redirect('gestionar_cursos')
    
    return render(request, 'principal/crear_curso.html')

@staff_member_required
def editar_curso(request, curso_id):
    from .models import Curso, ContenidoCurso, Pregunta, Opcion
    try:
        curso = Curso.objects.get(id=curso_id)
    except Curso.DoesNotExist:
        messages.error(request, 'El curso no existe.')
        return redirect('gestionar_cursos')

    if request.method == 'POST':
        # Datos básicos
        curso.titulo = request.POST.get('titulo')
        curso.descripcion = request.POST.get('descripcion')
        curso.orden = request.POST.get('orden')
        curso.puntos = request.POST.get('puntos')
        curso.icono = request.POST.get('icono')
        if 'video' in request.FILES:
            if curso.video:
                eliminar_archivo_fisico(curso.video)
            curso.video = request.FILES['video']
        curso.save()

        # --- Manejo de Diapositivas (Carrusel) ---
        ids_slide = request.POST.getlist('slide_id[]')
        titulos_slide = request.POST.getlist('slide_titulo[]')
        textos_slide = request.POST.getlist('slide_texto[]')
        indices_slide = request.POST.getlist('slide_form_index[]')
        
        # Obtener IDs de slides que se mantienen
        slides_actuales_ids = [s_id for s_id in ids_slide if s_id]
        
        # Borrar slides físicos que ya no están
        slides_a_borrar = curso.contenidos.exclude(id__in=slides_actuales_ids)
        for s in slides_a_borrar:
            eliminar_archivo_fisico(s.imagen)
        slides_a_borrar.delete()
        
        for i in range(len(titulos_slide)):
            slide_id = ids_slide[i] if i < len(ids_slide) else None
            form_idx = indices_slide[i] if i < len(indices_slide) else i
            titulo = titulos_slide[i]
            texto = textos_slide[i]
            
            if slide_id:
                # Actualizar existente
                try:
                    slide = ContenidoCurso.objects.get(id=slide_id)
                    slide.titulo = titulo
                    slide.texto = texto
                    slide.orden = i
                except ContenidoCurso.DoesNotExist:
                    continue
            else:
                # Crear nueva
                slide = ContenidoCurso.objects.create(
                    curso=curso,
                    titulo=titulo,
                    texto=texto,
                    orden=i
                )
            
            img_key = f'slide_imagen_{form_idx}'
            if img_key in request.FILES:
                if slide.imagen:
                    eliminar_archivo_fisico(slide.imagen)
                slide.imagen = request.FILES[img_key]
            
            slide.save()

        # --- Manejo de Materiales (Archivos) ---
        ids_material_mantener = request.POST.getlist('material_id[]')
        materiales_a_borrar = curso.materiales.exclude(id__in=ids_material_mantener)
        for m in materiales_a_borrar:
            eliminar_archivo_fisico(m.archivo)
        materiales_a_borrar.delete()

        nombres_material_nuevo = request.POST.getlist('material_nombre_nuevo[]')
        indices_material = request.POST.getlist('material_form_index[]')
        
        if nombres_material_nuevo:
            from .models import MaterialCurso
            for i in range(len(nombres_material_nuevo)):
                form_idx = indices_material[i] if i < len(indices_material) else i
                file_key = f'material_archivo_{form_idx}'
                if file_key in request.FILES:
                    MaterialCurso.objects.create(
                        curso=curso,
                        nombre=nombres_material_nuevo[i],
                        archivo=request.FILES[file_key]
                    )

        # --- Manejo de Preguntas ---
        textos_pregunta = request.POST.getlist('pregunta_texto[]')
        indices_pregunta = request.POST.getlist('question_form_index[]')
        
        # Siempre borramos y recreamos ( 
        # pero la lógica actual es borrar todo), pero ahora lo hacemos incluso si la lista está vacía
        curso.preguntas.all().delete()
        
        if textos_pregunta:
            for i in range(len(textos_pregunta)):
                p_texto = textos_pregunta[i]
                if not p_texto: continue
                
                form_idx = indices_pregunta[i] if i < len(indices_pregunta) else i
                pregunta = Pregunta.objects.create(curso=curso, texto=p_texto, orden=i)
                
                opciones_texto = request.POST.getlist(f'opcion_texto_{form_idx}[]')
                correctas = request.POST.getlist(f'opcion_correcta_{form_idx}[]')
                
                for j in range(len(opciones_texto)):
                    if not opciones_texto[j]: continue
                    es_correcta = str(j) in correctas
                    Opcion.objects.create(
                        pregunta=pregunta,
                        texto=opciones_texto[j],
                        es_correcta=es_correcta
                    )

        messages.success(request, f'Curso "{curso.titulo}" actualizado correctamente.')
        return redirect('gestionar_cursos')

    context = {
        'curso': curso,
        'contenidos': curso.contenidos.all(),
        'materiales': curso.materiales.all(),
        'preguntas': curso.preguntas.all().prefetch_related('opciones'),
    }
    return render(request, 'principal/editar_curso.html', context)

@staff_member_required
def eliminar_curso(request, curso_id):
    try:
        curso = Curso.objects.get(id=curso_id)
        # Borrar archivos físicos
        if curso.video: eliminar_archivo_fisico(curso.video)
        for s in curso.contenidos.all(): eliminar_archivo_fisico(s.imagen)
        for m in curso.materiales.all(): eliminar_archivo_fisico(m.archivo)
        
        titulo = curso.titulo
        curso.delete()
        messages.success(request, f'Curso "{titulo}" eliminado correctamente.')
    except Curso.DoesNotExist:
        messages.error(request, 'El curso no existe.')
    
    return redirect('gestionar_cursos')

@login_required
def ver_curso(request, curso_id):
    from .models import Curso, ContenidoCurso, Pregunta, Opcion, ProgresoCurso
    try:
        curso = Curso.objects.get(id=curso_id)
    except Curso.DoesNotExist:
        messages.error(request, 'El curso no existe.')
        return redirect('home')

    is_readonly = request.user.is_staff or request.user.groups.filter(name='Empresas').exists()
    progreso = None
    if not is_readonly:
        progreso, _ = ProgresoCurso.objects.get_or_create(usuario=request.user, curso=curso)
        
        # Bloquear nuevos intentos si el curso ya fue aprobado
        if progreso.estado == 'completado':
            is_readonly = True
        
        # Guardar progreso parcial vía AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
            try:
                import json
                data = json.loads(request.body)
                slide_index = int(data.get('slide_index', 0))
                progreso.ultima_pagina = slide_index
                progreso.save()
                return JsonResponse({'status': 'success'})
            except:
                return JsonResponse({'status': 'error'}, status=400)
    
    if request.method == 'POST' and not is_readonly:
        preguntas = curso.preguntas.all()
        correctas = 0
        total = preguntas.count()
        
        for p in preguntas:
            respuesta_id = request.POST.get(f'pregunta_{p.id}')
            if respuesta_id:
                try:
                    opcion = Opcion.objects.get(id=respuesta_id, pregunta=p)
                    if opcion.es_correcta:
                        correctas += 1
                except Opcion.DoesNotExist:
                    pass
        
        from django.urls import reverse
        porcentaje_exito = (correctas / total * 100) if total > 0 else 100
        score = int(porcentaje_exito)
        if score >= 70:
            progreso.estado = 'completado'
            progreso.porcentaje = 100
            import datetime
            progreso.fecha_completado = datetime.datetime.now()
            progreso.save()
            messages.success(request, f'¡Felicidades! Completaste el curso "{curso.titulo}" con una puntuación de {score}/100.')
            return redirect(f"{reverse('ver_curso', args=[curso.id])}?puntuacion={score}")
        else:
            progreso.estado = 'en_curso'
            progreso.porcentaje = 0
            progreso.ultima_pagina = 0
            progreso.save()
            messages.error(request, f'No has alcanzado el puntaje mínimo de 70/100. Puntuación obtenida: {score}/100. Debes volver a iniciar el curso.')
            return redirect(f"{reverse('ver_curso', args=[curso.id])}?puntuacion={score}")

    context = {
        'curso': curso,
        'contenidos': curso.contenidos.all(),
        'materiales': curso.materiales.all(),
        'preguntas': curso.preguntas.all().prefetch_related('opciones'),
        'progreso': progreso,
        'ultima_pagina': progreso.ultima_pagina if progreso else 0
    }
    return render(request, 'principal/ver_curso.html', context)

@staff_member_required
def auditoria(request):
    from django.contrib.auth.models import User
    from .models import Curso, ProgresoCurso, Perfil
    
    # Obtener todos los empleados con sus progresos y perfiles
    empleados = User.objects.filter(groups__name='Empleados').prefetch_related(
        'progresos', 'progresos__curso', 'perfil__empresa'
    ).order_by('perfil__empresa__username', 'username')
    
    cursos = Curso.objects.all().order_by('orden')
    
    empleados_stats = []
    for emp in empleados:
        progs = emp.progresos.all()
        progs_dict = {p.curso_id: p for p in progs}
        
        cursos_estados = []
        completados = 0
        for c in cursos:
            p = progs_dict.get(c.id)
            estado = p.estado if p else 'bloqueado'
            estado_display = p.get_estado_display() if p else 'Bloqueado'
            if estado == 'completado':
                completados += 1
            cursos_estados.append({
                'titulo': c.titulo,
                'estado': estado,
                'estado_display': estado_display
            })
            
        total_cursos = cursos.count()
        porcentaje = (completados * 100 // total_cursos) if total_cursos > 0 else 0
        
        empleados_stats.append({
            'empleado': emp,
            'porcentaje': porcentaje,
            'completados': completados,
            'total': total_cursos,
            'cursos_estados': cursos_estados,
            'empresa': emp.perfil.empresa if hasattr(emp, 'perfil') and emp.perfil.empresa else None
        })
    
    context = {
        'empleados_stats': empleados_stats,
        'cursos': cursos,
    }
    return render(request, 'principal/auditoria.html', context)

@login_required
def simulaciones(request):
    progresos = {p.simulacion_id: p for p in ProgresoSimulacion.objects.filter(usuario=request.user)}
    sims = Simulacion.objects.all()
    
    resultados = []
    for s in sims:
        prog = progresos.get(s.id)
        resultados.append({
            'sim': s,
            'completado': prog.completado if prog else False,
            'puntaje': prog.puntaje if prog else 0
        })
        
    return render(request, 'principal/simulaciones.html', {'simulaciones': resultados})

@login_required
def ejecutar_simulacion(request, sim_id):
    simulacion = get_object_or_404(Simulacion, id=sim_id)
    desafios = simulacion.desafios.all()
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            respuestas = data.get('respuestas', [])
            
            aciertos = 0
            total = desafios.count()
            
            for r in respuestas:
                d = DesafioSimulacion.objects.get(id=r['id'])
                if r['eleccion'] == d.es_peligro:
                    aciertos += 1
            
            puntos_finales = (aciertos * simulacion.puntos) // total if total > 0 else 0
            
            prog, _ = ProgresoSimulacion.objects.get_or_create(usuario=request.user, simulacion=simulacion)
            if prog.puntaje < puntos_finales:
                prog.puntaje = puntos_finales
            prog.completado = True
            prog.save()
            
            return JsonResponse({
                'status': 'success', 
                'puntos': puntos_finales, 
                'aciertos': aciertos, 
                'total': total
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return render(request, 'principal/ejecutar_simulacion.html', {
        'simulacion': simulacion,
        'desafios': desafios
    })

@staff_member_required
def gestionar_simulaciones(request):
    sims = Simulacion.objects.all().prefetch_related('desafios')
    return render(request, 'principal/gestionar_simulaciones.html', {'simulaciones': sims})

@staff_member_required
def crear_simulacion(request):
    return editar_simulacion(request, None)

@staff_member_required
def editar_simulacion(request, sim_id=None):
    from .models import Simulacion, DesafioSimulacion
    
    simulacion = None
    if sim_id:
        simulacion = get_object_or_404(Simulacion, id=sim_id)
        
    if request.method == 'POST':
        if not simulacion:
            simulacion = Simulacion.objects.create(
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion'),
                icono=request.POST.get('icono'),
                puntos=request.POST.get('puntos')
            )
        else:
            simulacion.titulo = request.POST.get('titulo')
            simulacion.descripcion = request.POST.get('descripcion')
            simulacion.icono = request.POST.get('icono')
            simulacion.puntos = request.POST.get('puntos')
            simulacion.save()
            
        # --- Desafíos ---
        ids_mantener = request.POST.getlist('desafio_id[]')
        # Limpiar vacíos
        ids_mantener_validos = [i for i in ids_mantener if i]
        
        # Eliminar desafíos físicos que ya no están
        desafios_a_borrar = simulacion.desafios.exclude(id__in=ids_mantener_validos)
        for d in desafios_a_borrar:
            eliminar_archivo_fisico(d.imagen)
        desafios_a_borrar.delete()
        
        contextos = request.POST.getlist('desafio_contexto[]')
        explicaciones = request.POST.getlist('desafio_explicacion[]')
        indices = request.POST.getlist('desafio_form_index[]')
        
        for i in range(len(contextos)):
            d_id = ids_mantener[i] if i < len(ids_mantener) else ""
            idx = indices[i]
            
            es_peligro = request.POST.get(f'desafio_es_peligro_{idx}') == 'on'
            
            if d_id:
                desafio = DesafioSimulacion.objects.get(id=d_id)
                desafio.texto_complementario = contextos[i]
                desafio.explicacion = explicaciones[i]
                desafio.es_peligro = es_peligro
            else:
                desafio = DesafioSimulacion(
                    simulacion=simulacion,
                    texto_complementario=contextos[i],
                    explicacion=explicaciones[i],
                    es_peligro=es_peligro
                )
            
            img_key = f'desafio_imagen_{idx}'
            if img_key in request.FILES:
                if desafio.id and desafio.imagen:
                    eliminar_archivo_fisico(desafio.imagen)
                desafio.imagen = request.FILES[img_key]
                
            desafio.save()
            
        messages.success(request, f'Simulación "{simulacion.titulo}" actualizada correctamente.')
        return redirect('gestionar_simulaciones')

    context = {
        'simulacion': simulacion,
        'desafios': simulacion.desafios.all() if simulacion else []
    }
    return render(request, 'principal/editar_simulacion.html', context)

@staff_member_required
def eliminar_simulacion(request, sim_id):
    sim = get_object_or_404(Simulacion, id=sim_id)
    titulo = sim.titulo
    # Borrar archivos de los desafíos
    for d in sim.desafios.all():
        eliminar_archivo_fisico(d.imagen)
    sim.delete()
    messages.success(request, f'Simulación "{titulo}" eliminada correctamente.')
    return redirect('gestionar_simulaciones')

def registro_empresa(request):
    if request.method == 'POST':
        nombre_empresa = request.POST.get('nombre_empresa')
        nombre_contacto = request.POST.get('nombre_contacto')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        rfc = request.POST.get('rfc')
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')
        
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Este nombre de usuario ya está en uso.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
        else:
            # Crear usuario inactivo (requiere confirmación por correo)
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False 
            user.first_name = nombre_contacto
            user.last_name = nombre_empresa
            user.save()
            
            # Guardar datos adicionales en el perfil
            user.perfil.nombre_empresa = nombre_empresa
            user.perfil.rfc = rfc
            user.perfil.telefono = telefono
            user.perfil.notas = mensaje
            user.perfil.save()
            
            # Asignar al grupo de Empresas
            from django.contrib.auth.models import Group
            group, _ = Group.objects.get_or_create(name='Empresas')
            user.groups.add(group)
            
            # Generar token de activación
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activacion_url = f"{request.scheme}://{request.get_host()}/confirmar-registro/{uid}/{token}/"
            
            # Enviar correo de confirmación
            try:
                context_email = {
                    'nombre_contacto': nombre_contacto,
                    'nombre_empresa': nombre_empresa,
                    'activacion_url': activacion_url
                }
                html_message = render_to_string('emails/confirmacion_registro.html', context_email)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    'Confirma tu cuenta - CyberPyme Yucatán',
                    plain_message,
                    None,
                    [email],
                    html_message=html_message
                )
                messages.success(request, '¡Registro exitoso! Te hemos enviado un correo de confirmación. Por favor revisa tu bandeja de entrada para activar tu cuenta.')
            except Exception as e:
                print(f"Error enviando correo: {e}")
                messages.warning(request, 'Tu cuenta fue creada, pero hubo un detalle al enviar el correo de activación. Contacta al soporte.')
            
            return redirect('login')
            
    return render(request, 'principal/registro_empresa.html')

def confirmar_registro(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, '¡Tu cuenta ha sido activada con éxito! Ya puedes iniciar sesión.')
        return redirect('login')
    else:
        messages.error(request, 'El enlace de confirmación es inválido o ha expirado.')
        return redirect('home')

def confirmar_contrasena_empleado(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if not password or not confirm_password:
                messages.error(request, 'Ambos campos de contraseña son obligatorios.')
            elif password != confirm_password:
                messages.error(request, 'Las contraseñas no coinciden.')
            elif len(password) < 8:
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            else:
                user.set_password(password)
                user.is_active = True
                user.save()
                messages.success(request, '¡Tu contraseña ha sido establecida con éxito! Ya puedes iniciar sesión.')
                return redirect('login')

        return render(request, 'principal/confirmar_contrasena_empleado.html', {'employee': user})
    else:
        messages.error(request, 'El enlace de confirmación es inválido o ha expirado.')
        return redirect('home')
