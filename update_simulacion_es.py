import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from principal.models import Simulacion, DesafioSimulacion

SVG_PHISHING = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500">
  <rect width="800" height="500" fill="#f0f2f5"/>
  <rect width="800" height="60" fill="#ffffff" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.1))"/>
  <text x="20" y="40" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="#1a73e8">Correo</text>
  <rect x="50" y="90" width="700" height="380" rx="10" fill="#ffffff" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.1))"/>
  <text x="80" y="140" font-family="Arial, sans-serif" font-size="22" font-weight="bold" fill="#202124">URGENTE: Factura Vencida #99482</text>
  <text x="80" y="170" font-family="Arial, sans-serif" font-size="14" fill="#5f6368">De: administracion@empresa-pagos-seguros.com</text>
  <text x="80" y="190" font-family="Arial, sans-serif" font-size="14" fill="#5f6368">Para: ti</text>
  <text x="80" y="240" font-family="Arial, sans-serif" font-size="16" fill="#202124">Estimado cliente,</text>
  <text x="80" y="270" font-family="Arial, sans-serif" font-size="16" fill="#202124">Su cuenta sera suspendida en 24 HORAS si no paga la factura adjunta.</text>
  <text x="80" y="300" font-family="Arial, sans-serif" font-size="16" fill="#202124">Por favor descargue y abra el documento para ver los detalles.</text>
  <text x="80" y="330" font-family="Arial, sans-serif" font-size="16" fill="#202124">Saludos,</text>
  <text x="80" y="350" font-family="Arial, sans-serif" font-size="16" fill="#202124">El equipo de Cobranzas.</text>
  <rect x="80" y="380" width="300" height="60" rx="8" fill="#f8f9fa" stroke="#dadce0" stroke-width="1"/>
  <rect x="90" y="390" width="40" height="40" rx="4" fill="#ea4335"/>
  <text x="100" y="415" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="#ffffff">PDF</text>
  <text x="140" y="405" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#202124">factura_urgente.pdf.exe</text>
  <text x="140" y="425" font-family="Arial, sans-serif" font-size="12" fill="#5f6368">3.4 MB</text>
</svg>"""

SVG_SCAREWARE = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500">
  <rect width="800" height="500" fill="#202124"/>
  <rect x="50" y="50" width="700" height="400" rx="8" fill="#ffffff"/>
  <rect x="50" y="50" width="700" height="40" fill="#f1f3f4" rx="8"/>
  <circle cx="70" cy="70" r="6" fill="#ea4335"/>
  <circle cx="90" cy="70" r="6" fill="#fbbc04"/>
  <circle cx="110" cy="70" r="6" fill="#34a853"/>
  <rect x="150" y="60" width="500" height="20" rx="10" fill="#ffffff"/>
  <text x="160" y="75" font-family="Arial, sans-serif" font-size="12" fill="#5f6368">http://alerta-seguridad-pc-gratis.com/scan</text>
  <rect x="200" y="150" width="400" height="220" rx="4" fill="#ffffff" filter="drop-shadow(0 10px 20px rgba(0,0,0,0.5))" stroke="#d93025" stroke-width="4"/>
  <rect x="200" y="150" width="400" height="50" fill="#d93025"/>
  <text x="220" y="182" font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#ffffff">¡ALERTA DEL SISTEMA!</text>
  <text x="220" y="230" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#d93025">¡SU COMPUTADORA ESTÁ INFECTADA!</text>
  <text x="220" y="260" font-family="Arial, sans-serif" font-size="14" fill="#202124">Hemos detectado 5 virus y troyanos en su sistema.</text>
  <text x="220" y="280" font-family="Arial, sans-serif" font-size="14" fill="#202124">Sus datos personales y fotos podrían ser borrados.</text>
  <rect x="280" y="310" width="240" height="40" rx="20" fill="#1a73e8"/>
  <text x="315" y="335" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">LIMPIAR PC AHORA</text>
</svg>"""

SVG_UPDATE = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="500">
  <rect width="800" height="500" fill="#c3e0e5"/>
  <rect x="0" y="460" width="800" height="40" fill="#1e1e1e"/>
  <text x="730" y="485" font-family="Segoe UI, Arial, sans-serif" font-size="12" fill="#ffffff">14:30</text>
  <rect x="450" y="340" width="340" height="110" rx="8" fill="#2b2b2b" filter="drop-shadow(0 4px 6px rgba(0,0,0,0.3))"/>
  <rect x="470" y="360" width="24" height="24" fill="#0078d7" rx="4"/>
  <path d="M476 372 l4 4 l8 -8" stroke="#ffffff" stroke-width="2" fill="none"/>
  <text x="510" y="370" font-family="Segoe UI, Arial, sans-serif" font-size="14" font-weight="bold" fill="#ffffff">Windows Update</text>
  <text x="510" y="395" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#cccccc">Actualizaciones listas para instalar.</text>
  <text x="510" y="415" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#cccccc">Tu dispositivo requiere un reinicio para</text>
  <text x="510" y="435" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#cccccc">completar la instalación.</text>
</svg>"""

def run():
    try:
        sim = Simulacion.objects.get(titulo="Ataque de Ransomware")
    except Simulacion.DoesNotExist:
        print("La simulación de Ransomware no existe. Crea la simulación primero.")
        return

    desafios = sim.desafios.all().order_by('id')
    if len(desafios) == 3:
        # Update 1
        d1 = desafios[0]
        if d1.imagen:
            d1.imagen.delete(save=False)
        d1.imagen.save('phishing_es.svg', ContentFile(SVG_PHISHING.encode('utf-8')), save=True)
        
        # Update 2
        d2 = desafios[1]
        if d2.imagen:
            d2.imagen.delete(save=False)
        d2.imagen.save('scareware_es.svg', ContentFile(SVG_SCAREWARE.encode('utf-8')), save=True)

        # Update 3
        d3 = desafios[2]
        if d3.imagen:
            d3.imagen.delete(save=False)
        d3.imagen.save('update_es.svg', ContentFile(SVG_UPDATE.encode('utf-8')), save=True)
        
        print("¡Imágenes actualizadas a español correctamente con formato SVG!")
    else:
        print(f"Esperaba 3 desafíos pero encontré {len(desafios)}.")

if __name__ == '__main__':
    run()
