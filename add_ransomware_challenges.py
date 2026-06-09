import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from principal.models import Simulacion, DesafioSimulacion

SVG_USB = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" style="background:#e8ecef; font-family:'Segoe UI', sans-serif;">
  <rect width="800" height="500" fill="#e8ecef"/>
  <rect x="100" y="80" width="600" height="340" rx="20" fill="#fafafa" stroke="#d0d0d0" stroke-width="2"/>
  <text x="140" y="130" font-size="24" font-weight="bold" fill="#2c3e50">Estacionamiento de la Empresa</text>
  <text x="140" y="165" font-size="15" fill="#7f8c8d">Vas de camino a tu oficina por la mañana y encuentras este dispositivo en el suelo.</text>
  
  <g transform="translate(100, 30)">
    <rect x="250" y="180" width="220" height="100" rx="12" fill="#1e272c" filter="drop-shadow(0 8px 12px rgba(0,0,0,0.35))"/>
    <rect x="470" y="200" width="50" height="60" fill="#b0bec5" rx="3"/>
    <rect x="490" y="212" width="15" height="8" fill="#cfd8dc"/>
    <rect x="490" y="238" width="15" height="8" fill="#cfd8dc"/>
    <circle cx="280" cy="230" r="12" fill="#e8ecef"/>
    <rect x="310" y="195" width="130" height="70" fill="#ffffff" rx="4"/>
    <text x="320" y="235" font-size="13" font-weight="bold" fill="#d32f2f">CONFIDENCIAL</text>
    <text x="320" y="253" font-size="11" font-weight="bold" fill="#37474f">NOMINAS_2026.xlsx</text>
  </g>
</svg>"""

SVG_EXCEL = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" style="background:#f3f2f1; font-family:'Segoe UI', sans-serif;">
  <rect width="800" height="500" fill="#f3f2f1"/>
  <rect width="800" height="40" fill="#107c41"/>
  <text x="20" y="26" fill="#ffffff" font-size="16" font-weight="bold">Microsoft Excel - Factura_Pendiente.xlsm</text>
  
  <rect y="40" width="800" height="45" fill="#fff2cc" stroke="#f0d38a" stroke-width="1"/>
  <circle cx="25" cy="62" r="10" fill="#d83b01"/>
  <text x="22" y="67" fill="#ffffff" font-size="13" font-weight="bold">!</text>
  <text x="50" y="66" fill="#323130" font-size="13" font-weight="bold">ADVERTENCIA DE SEGURIDAD</text>
  <text x="235" y="66" fill="#323130" font-size="13">Las macros se han deshabilitado de forma automática.</text>
  <rect x="640" y="48" width="140" height="28" fill="#ffffff" stroke="#8a8886" stroke-width="1" rx="2"/>
  <text x="655" y="66" fill="#323130" font-size="12" font-weight="bold">Habilitar contenido</text>
  
  <rect x="15" y="100" width="770" height="380" fill="#ffffff" stroke="#d2d2d2" stroke-width="1"/>
  <line x1="15" y1="130" x2="785" y2="130" stroke="#e0e0e0"/>
  <line x1="15" y1="160" x2="785" y2="160" stroke="#e0e0e0"/>
  <line x1="15" y1="190" x2="785" y2="190" stroke="#e0e0e0"/>
  <line x1="85" y1="100" x2="85" y2="480" stroke="#e0e0e0"/>
  <line x1="220" y1="100" x2="220" y2="480" stroke="#e0e0e0"/>
  
  <rect x="30" y="145" width="740" height="320" fill="rgba(255,255,255,0.92)" rx="6" stroke="#c8c6c4" stroke-dasharray="5,5"/>
  <text x="400" y="240" font-size="20" font-weight="bold" fill="#323130" text-anchor="middle">⚠️ VISTA PREVIA PROTEGIDA</text>
  <text x="400" y="275" font-size="14" fill="#605e5c" text-anchor="middle">Para poder visualizar y descargar los datos de esta factura,</text>
  <text x="400" y="295" font-size="14" fill="#605e5c" text-anchor="middle">es necesario que haga clic en "Habilitar contenido" en la barra amarilla superior.</text>
</svg>"""

SVG_DEFENDER = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500" style="background:#e6e6e6; font-family:'Segoe UI', sans-serif;">
  <rect width="800" height="500" fill="#e6e6e6"/>
  <rect x="50" y="50" width="700" height="400" rx="12" fill="#fafafa" stroke="#d0d0d0" stroke-width="2"/>
  <text x="90" y="110" font-size="22" font-weight="bold" fill="#202020">Notificación del Sistema de Seguridad</text>
  
  <rect x="410" y="290" width="320" height="140" rx="8" fill="#2b2b2b" filter="drop-shadow(0 6px 12px rgba(0,0,0,0.3))"/>
  <path d="M435 320 L448 312 L461 320 L461 336 Q448 348 435 352 Q422 348 409 336 Z" fill="#107c10"/>
  <path d="M425 330 L432 337 L447 322" stroke="#ffffff" stroke-width="3" fill="none"/>
  <text x="475" y="328" font-size="13" font-weight="bold" fill="#ffffff">Seguridad de Windows</text>
  <text x="475" y="348" font-size="12" font-weight="bold" fill="#a6e22e">Amenaza bloqueada y eliminada</text>
  <text x="425" y="380" font-size="11" fill="#e0e0e0">Antivirus de Windows Defender ha puesto en cuarentena</text>
  <text x="425" y="398" font-size="11" fill="#e0e0e0">el archivo sospechoso detectado.</text>
  <text x="425" y="415" font-size="10" fill="#aaaaaa">Archivo: C:\\Descargas\\update_patch.exe</text>
</svg>"""

def run():
    try:
        sim = Simulacion.objects.get(titulo__icontains="Ransomware")
    except Simulacion.DoesNotExist:
        print("La simulación de Ransomware no existe.")
        return

    sim.descripcion = "Aprende a identificar cómo se propaga el Ransomware y qué medidas preventivas tomar ante unidades extraíbles infectadas, macros maliciosas y software desconocido."
    sim.puntos = 250
    sim.save()

    desafios_nuevos = [
        {
            "svg": SVG_USB,
            "filename": "usb_drop_danger.svg",
            "contexto": "Encuentras esta memoria USB en el estacionamiento de la empresa con una etiqueta que dice 'CONFIDENCIAL NOMINAS 2026'. ¿Es seguro conectarla a tu computadora de la oficina?",
            "es_peligro": True,
            "explicacion": "¡Correcto! Esta es una técnica clásica de Ingeniería Social llamada 'USB Dropping'. Los atacantes dejan memorias USB infectadas con malware (como ransomware) en áreas comunes esperando que un empleado curioso las conecte."
        },
        {
            "svg": SVG_EXCEL,
            "filename": "excel_macro_danger.svg",
            "contexto": "Recibes una factura en formato Excel (.xlsm) y al abrirla se te solicita 'Habilitar contenido' (Macros) para ver los datos de la factura protegida.",
            "es_peligro": True,
            "explicacion": "¡Exacto! Habilitar macros en documentos descargados de fuentes externas o sospechosas es una vía muy común para ejecutar scripts automatizados que descargan e instalan ransomware de forma silenciosa."
        },
        {
            "svg": SVG_DEFENDER,
            "filename": "windows_defender_safe.svg",
            "contexto": "Tras intentar abrir un archivo sospechoso, te aparece esta notificación del antivirus integrado en tu sistema operativo.",
            "es_peligro": False,
            "explicacion": "Correcto. Esta notificación indica que tu sistema de seguridad (Windows Defender) funcionó correctamente detectando, deteniendo y eliminando la amenaza antes de que pudiera ejecutarse y encriptar tu información."
        }
    ]

    for data in desafios_nuevos:
        # Check if already exists to avoid duplicates
        d, created = DesafioSimulacion.objects.get_or_create(
            simulacion=sim,
            texto_complementario=data["contexto"],
            defaults={
                "es_peligro": data["es_peligro"],
                "explicacion": data["explicacion"]
            }
        )
        d.imagen.save(data["filename"], ContentFile(data["svg"].encode('utf-8')), save=True)
        print(f"Desafío agregado: {data['filename']} (Creado: {created})")

    print(f"¡Simulación de Ransomware actualizada con éxito! Ahora tiene {sim.desafios.count()} desafíos.")

if __name__ == '__main__':
    run()
