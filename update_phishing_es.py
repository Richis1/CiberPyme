import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from principal.models import Simulacion, DesafioSimulacion

SVG_PHISHING = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500">
  <rect width="800" height="500" fill="#f0f2f5"/>
  <rect width="800" height="60" fill="#ffffff" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))"/>
  <text x="20" y="40" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#1a73e8">Correo Corporativo</text>
  <rect x="50" y="90" width="700" height="380" rx="10" fill="#ffffff" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.1))"/>
  <text x="80" y="140" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="#d93025">ACCIÓN REQUERIDA: Verificación de Seguridad</text>
  <text x="80" y="170" font-family="Arial, sans-serif" font-size="14" fill="#5f6368">De: soporte@seguridad-servidor.com</text>
  <text x="80" y="190" font-family="Arial, sans-serif" font-size="14" fill="#5f6368">Para: empleado@cyberpyme.com</text>
  <text x="80" y="240" font-family="Arial, sans-serif" font-size="16" fill="#202124">Estimado usuario,</text>
  <text x="80" y="270" font-family="Arial, sans-serif" font-size="16" fill="#202124">Hemos detectado actividad inusual en su cuenta de correo institucional.</text>
  <text x="80" y="300" font-family="Arial, sans-serif" font-size="16" fill="#202124">Si no verifica su identidad en las próximas 2 horas, su acceso será suspendido.</text>
  <rect x="80" y="330" width="200" height="40" rx="5" fill="#1a73e8"/>
  <text x="105" y="355" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="#ffffff">VERIFICAR CUENTA</text>
  <text x="80" y="400" font-family="Arial, sans-serif" font-size="14" fill="#5f6368">El equipo de Seguridad IT</text>
</svg>"""

SVG_TEAMS = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500">
  <rect width="800" height="500" fill="#f5f5f5"/>
  <rect x="150" y="50" width="500" height="400" rx="8" fill="#ffffff" filter="drop-shadow(0 4px 8px rgba(0,0,0,0.1))"/>
  <rect x="150" y="50" width="500" height="60" fill="#464eb8" rx="8"/>
  <circle cx="180" cy="80" r="15" fill="#ffffff"/>
  <text x="171" y="86" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="bold" fill="#464eb8">CM</text>
  <text x="210" y="85" font-family="Segoe UI, Arial, sans-serif" font-size="18" font-weight="bold" fill="#ffffff">Carlos Mendoza (Contabilidad)</text>
  <text x="350" y="140" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#888888">Hoy, 09:15 AM</text>
  <rect x="170" y="160" width="410" height="50" rx="10" fill="#e8ebfa"/>
  <text x="190" y="190" font-family="Segoe UI, Arial, sans-serif" font-size="15" fill="#333333">¡Hola! ¿Cómo vas con el reporte de fin de mes para el cliente?</text>
  <rect x="170" y="380" width="460" height="40" rx="20" fill="#f0f0f0"/>
  <text x="190" y="405" font-family="Segoe UI, Arial, sans-serif" font-size="14" fill="#888888">Escribe un mensaje...</text>
</svg>"""

def run():
    try:
        sim = Simulacion.objects.get(titulo__icontains="Phishing")
    except Simulacion.DoesNotExist:
        print("La simulación de Phishing no existe.")
        return

    desafios = sim.desafios.all().order_by('id')
    if len(desafios) == 2:
        # Update 1
        d1 = desafios[0]
        if d1.imagen:
            d1.imagen.delete(save=False)
        d1.imagen.save('phishing_alert_es.svg', ContentFile(SVG_PHISHING.encode('utf-8')), save=True)
        
        # Update 2
        d2 = desafios[1]
        if d2.imagen:
            d2.imagen.delete(save=False)
        d2.imagen.save('teams_chat_es.svg', ContentFile(SVG_TEAMS.encode('utf-8')), save=True)
        
        print("¡Imágenes de Phishing actualizadas a español correctamente con formato SVG!")
    else:
        print(f"Esperaba 2 desafíos pero encontré {len(desafios)}.")

if __name__ == '__main__':
    run()
