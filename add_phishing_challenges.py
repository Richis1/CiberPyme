import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from principal.models import Simulacion, DesafioSimulacion

SVG_OUTLOOK = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="background:#f3f2f1; font-family:'Segoe UI', system-ui, sans-serif;">
  <rect width="900" height="48" fill="#0f6cbd"/>
  <rect x="20" y="16" width="16" height="16" fill="#fff" rx="2"/>
  <rect x="24" y="20" width="8" height="8" fill="#0f6cbd" rx="1"/>
  <text x="50" y="32" fill="#fff" font-size="16" font-weight="600">Outlook</text>
  <rect x="250" y="8" width="400" height="32" fill="rgba(255,255,255,0.8)" rx="4"/>
  <text x="260" y="29" fill="#0f6cbd" font-size="14">🔍 Buscar</text>
  <rect y="48" width="200" height="552" fill="#f3f2f1"/>
  <text x="40" y="85" fill="#242424" font-size="14" font-weight="600">Bandeja de entrada</text>
  <text x="40" y="125" fill="#605e5c" font-size="14">Elementos enviados</text>
  <text x="40" y="165" fill="#605e5c" font-size="14">Elementos eliminados</text>
  <text x="40" y="205" fill="#605e5c" font-size="14">Correo no deseado</text>
  <rect x="200" y="48" width="250" height="552" fill="#fff" stroke="#e1dfdd" stroke-width="1"/>
  <rect x="200" y="48" width="250" height="80" fill="#f3f2f1" stroke="#0f6cbd" stroke-width="2"/>
  <circle cx="230" cy="88" r="16" fill="#d13438"/>
  <text x="224" y="94" fill="#fff" font-size="14" font-weight="600">S</text>
  <text x="255" y="75" fill="#242424" font-size="14" font-weight="600">Soporte IT</text>
  <text x="255" y="95" fill="#0f6cbd" font-size="13">Alerta de Seguridad</text>
  <text x="255" y="115" fill="#605e5c" font-size="12">Acción requerida inmediata...</text>
  <rect x="450" y="48" width="450" height="552" fill="#fff"/>
  <circle cx="490" cy="100" r="24" fill="#d13438"/>
  <text x="483" y="108" fill="#fff" font-size="20" font-weight="600">S</text>
  <text x="530" y="90" fill="#242424" font-size="20" font-weight="600">Alerta de Seguridad: Inicio de sesión bloqueado</text>
  <text x="530" y="115" fill="#242424" font-size="14" font-weight="600">Soporte IT</text>
  <text x="605" y="115" fill="#605e5c" font-size="12">&lt;soporte-seguridad@actualizacion-microsoft-web.com&gt;</text>
  <text x="530" y="135" fill="#605e5c" font-size="13">Para: ti</text>
  <rect x="450" y="155" width="450" height="1" fill="#e1dfdd"/>
  <text x="490" y="195" fill="#242424" font-size="15">Estimado usuario,</text>
  <text x="490" y="235" fill="#242424" font-size="15">Hemos detectado múltiples intentos de acceso a su cuenta desde Rusia.</text>
  <text x="490" y="260" fill="#242424" font-size="15">Por motivos de seguridad, su cuenta será suspendida en 24 horas.</text>
  <text x="490" y="285" fill="#242424" font-size="15">Para cancelar la suspensión y confirmar su identidad, haga clic en el</text>
  <text x="490" y="310" fill="#242424" font-size="15">siguiente enlace y proporcione su contraseña actual:</text>
  <rect x="490" y="340" width="220" height="40" fill="#0f6cbd" rx="4"/>
  <text x="525" y="366" fill="#fff" font-size="15" font-weight="600">Verificar Cuenta Ahora</text>
  <text x="490" y="415" fill="#0f6cbd" font-size="13" text-decoration="underline">http://actualizacion-microsoft-web.com/login-verify-account</text>
  <text x="490" y="460" fill="#242424" font-size="15">Atentamente,</text>
  <text x="490" y="480" fill="#242424" font-size="15">Equipo de Seguridad y Cuentas.</text>
</svg>"""

SVG_TEAMS = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="background:#ebebeb; font-family:'Segoe UI', system-ui, sans-serif;">
  <rect width="900" height="48" fill="#e0e0e0"/>
  <rect x="250" y="8" width="400" height="32" fill="#fff" rx="6" stroke="#d1d1d1" stroke-width="1"/>
  <text x="420" y="29" fill="#605e5c" font-size="14">Buscar</text>
  <rect y="48" width="68" height="552" fill="#ebebeb"/>
  <rect x="14" y="60" width="40" height="40" fill="#fff" rx="4"/>
  <rect x="14" y="115" width="40" height="40" fill="#fff" rx="4"/>
  <rect x="10" y="115" width="4" height="40" fill="#5b5fc7" rx="2"/>
  <text x="22" y="140" fill="#5b5fc7" font-size="12" font-weight="600">Chat</text>
  <rect x="68" y="48" width="250" height="552" fill="#fff"/>
  <text x="85" y="80" fill="#242424" font-size="20" font-weight="600">Chat</text>
  <rect x="68" y="100" width="250" height="70" fill="#f5f5f5"/>
  <circle cx="95" cy="135" r="18" fill="#ca5010"/>
  <text x="86" y="140" fill="#fff" font-size="14" font-weight="600">AR</text>
  <circle cx="106" cy="146" r="6" fill="#107c10" stroke="#fff" stroke-width="2"/>
  <text x="125" y="125" fill="#242424" font-size="14" font-weight="600">Ana Ruiz</text>
  <text x="125" y="145" fill="#605e5c" font-size="13">Hola, ¿tienes un minuto?</text>
  <text x="270" y="125" fill="#605e5c" font-size="12">10:45</text>
  <rect x="318" y="48" width="582" height="552" fill="#f5f5f5"/>
  <rect x="318" y="48" width="582" height="65" fill="#fff" stroke="#e1dfdd" stroke-width="1"/>
  <circle cx="355" cy="80" r="18" fill="#ca5010"/>
  <text x="346" y="85" fill="#fff" font-size="14" font-weight="600">AR</text>
  <circle cx="366" cy="91" r="6" fill="#107c10" stroke="#fff" stroke-width="2"/>
  <text x="385" y="75" fill="#242424" font-size="16" font-weight="600">Ana Ruiz</text>
  <text x="385" y="93" fill="#605e5c" font-size="12">Gerente de Recursos Humanos</text>
  <text x="550" y="160" fill="#605e5c" font-size="12">Hoy 10:45 AM</text>
  <circle cx="355" cy="200" r="18" fill="#ca5010"/>
  <text x="346" y="205" fill="#fff" font-size="14" font-weight="600">AR</text>
  <text x="385" y="195" fill="#242424" font-size="14" font-weight="600">Ana Ruiz</text>
  <text x="450" y="195" fill="#605e5c" font-size="12">10:45 AM</text>
  <rect x="385" y="205" width="400" height="60" fill="#fff" rx="8" filter="drop-shadow(0 2px 4px rgba(0,0,0,0.05))"/>
  <text x="400" y="230" fill="#242424" font-size="14">¡Hola! ¿Cómo vas con la revisión de los perfiles que te</text>
  <text x="400" y="250" fill="#242424" font-size="14">envié ayer? Avisame si necesitas algo más.</text>
  <rect x="340" y="520" width="540" height="50" fill="#fff" rx="4" stroke="#d1d1d1" stroke-width="1"/>
  <text x="360" y="550" fill="#605e5c" font-size="14">Escribe un mensaje nuevo</text>
</svg>"""

SVG_WHATSAPP = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="background:#efeae2; font-family:'Segoe UI', system-ui, sans-serif;">
  <rect y="0" width="900" height="100" fill="#00a884"/>
  <rect x="20" y="20" width="860" height="560" fill="#fff" rx="4" filter="drop-shadow(0 4px 10px rgba(0,0,0,0.1))"/>
  <rect x="20" y="20" width="280" height="560" fill="#fff" stroke="#d1d7db" stroke-width="1"/>
  <rect x="20" y="20" width="280" height="60" fill="#f0f2f5"/>
  <circle cx="50" cy="50" r="20" fill="#dfe5e7"/>
  <rect x="30" y="90" width="260" height="35" fill="#f0f2f5" rx="8"/>
  <text x="50" y="112" fill="#54656f" font-size="14">Busca un chat o inicia uno nuevo</text>
  <rect x="20" y="140" width="280" height="72" fill="#f0f2f5"/>
  <circle cx="55" cy="176" r="24" fill="#dfe5e7"/>
  <text x="95" y="165" fill="#111b21" font-size="16">+52 55 1234 5678</text>
  <text x="95" y="185" fill="#667781" font-size="14">Su tarjeta ha sido...</text>
  <rect x="300" y="20" width="580" height="60" fill="#f0f2f5"/>
  <circle cx="340" cy="50" r="20" fill="#dfe5e7"/>
  <text x="375" y="45" fill="#111b21" font-size="16">+52 55 1234 5678</text>
  <text x="375" y="65" fill="#667781" font-size="13">~ Banco Seguridad</text>
  <rect x="300" y="80" width="580" height="440" fill="#efeae2"/>
  <rect x="540" y="100" width="100" height="26" fill="#fff" rx="6" filter="drop-shadow(0 1px 1px rgba(0,0,0,0.05))"/>
  <text x="570" y="118" fill="#54656f" font-size="12">HOY</text>
  <rect x="340" y="150" width="380" height="150" fill="#fff" rx="8" filter="drop-shadow(0 1px 1px rgba(0,0,0,0.05))"/>
  <text x="355" y="175" fill="#111b21" font-size="15">🚨 ALERTA DE BANCO CENTRAL 🚨</text>
  <text x="355" y="205" fill="#111b21" font-size="15">Se autorizó un cargo de $8,500.00 MXN</text>
  <text x="355" y="225" fill="#111b21" font-size="15">en su tarjeta terminada en 4321.</text>
  <text x="355" y="255" fill="#111b21" font-size="15">Si no reconoce este cargo, cancele aquí:</text>
  <text x="355" y="280" fill="#027eb5" font-size="15">https://cancelacion-banco-alerta.net/auth</text>
  <text x="670" y="290" fill="#8696a0" font-size="11">12:30 p.m.</text>
  <rect x="300" y="520" width="580" height="60" fill="#f0f2f5"/>
  <rect x="360" y="530" width="460" height="40" fill="#fff" rx="8"/>
  <text x="380" y="555" fill="#8696a0" font-size="15">Escribe un mensaje</text>
</svg>"""

SVG_DRIVE = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="background:#f2f2f2; font-family:'Roboto', system-ui, sans-serif;">
  <rect x="150" y="50" width="600" height="450" fill="#fff" rx="8" stroke="#dadce0" stroke-width="1"/>
  <rect x="150" y="50" width="600" height="80" fill="#fff" rx="8"/>
  <rect x="150" y="130" width="600" height="1" fill="#dadce0"/>
  <polygon points="180,90 190,70 210,70 200,90" fill="#1aa260"/>
  <polygon points="180,90 200,90 210,110 190,110" fill="#4285f4"/>
  <polygon points="210,70 220,90 210,110 200,90" fill="#fbbc04"/>
  <text x="230" y="95" fill="#5f6368" font-size="22" font-weight="600">Google Drive</text>
  <text x="190" y="180" fill="#202124" font-size="18"><b>Maria Gonzalez</b> compartió un documento contigo</text>
  <rect x="190" y="210" width="520" height="80" fill="#fff" rx="8" stroke="#dadce0" stroke-width="1"/>
  <rect x="210" y="235" width="24" height="30" fill="#4285f4" rx="2"/>
  <rect x="215" y="240" width="14" height="2" fill="#fff"/>
  <rect x="215" y="245" width="14" height="2" fill="#fff"/>
  <rect x="215" y="250" width="14" height="2" fill="#fff"/>
  <rect x="215" y="255" width="10" height="2" fill="#fff"/>
  <text x="250" y="245" fill="#202124" font-size="16" font-weight="600">Reporte_Anual_Ventas_2026.docx</text>
  <text x="250" y="265" fill="#5f6368" font-size="14">Documento de Microsoft Word</text>
  <rect x="190" y="320" width="100" height="36" fill="#1a73e8" rx="4"/>
  <text x="215" y="343" fill="#fff" font-size="14" font-weight="600">Abrir</text>
  <rect x="150" y="390" width="600" height="1" fill="#dadce0"/>
  <text x="190" y="420" fill="#5f6368" font-size="12">Google LLC, 1600 Amphitheatre Parkway, Mountain View, CA 94043, USA</text>
  <text x="190" y="440" fill="#5f6368" font-size="12">Has recibido este correo porque alguien ha compartido un archivo contigo.</text>
</svg>"""

def run():
    try:
        sim = Simulacion.objects.get(titulo__icontains="Phishing")
    except Simulacion.DoesNotExist:
        print("La simulación no existe.")
        return

    sim.descripcion = "Evalúa diferentes escenarios de comunicación empresarial (Correos, Mensajería y Almacenamiento en la nube) e identifica cuáles son ataques de suplantación de identidad (Phishing/Smishing) y cuáles son legítimos."
    sim.puntos = 200
    sim.save()

    print("Limpiando desafíos antiguos...")
    for d in sim.desafios.all():
        if d.imagen:
            d.imagen.delete(save=False)
        d.delete()

    desafios_data = [
        {
            "svg": SVG_OUTLOOK,
            "filename": "outlook_phishing.svg",
            "contexto": "Recibes este correo electrónico en la bandeja de entrada de tu trabajo.",
            "es_peligro": True,
            "explicacion": "¡Atención! Este es un ataque de Phishing. Fíjate en el remitente: el dominio es 'actualizacion-microsoft-web.com' en lugar de 'microsoft.com'. Intenta generar urgencia amenazando con suspender la cuenta y te dirige a un enlace falso."
        },
        {
            "svg": SVG_TEAMS,
            "filename": "teams_safe.svg",
            "contexto": "Un compañero de trabajo te envía un mensaje directo por Microsoft Teams.",
            "es_peligro": False,
            "explicacion": "Este mensaje es seguro. Es una comunicación interna habitual de una colega verificada dentro de tu organización, y no contiene enlaces externos ni solicita información confidencial."
        },
        {
            "svg": SVG_WHATSAPP,
            "filename": "whatsapp_smishing.svg",
            "contexto": "Te llega esta notificación y mensaje por WhatsApp de un número desconocido.",
            "es_peligro": True,
            "explicacion": "Este es un ataque de 'Smishing' (Phishing por mensajería). Los bancos reales no te envían enlaces por WhatsApp para cancelar cargos de esta manera. El enlace es fraudulento y busca robar tus credenciales bancarias."
        },
        {
            "svg": SVG_DRIVE,
            "filename": "drive_safe.svg",
            "contexto": "Recibes una notificación en tu correo corporativo de que se ha compartido un documento.",
            "es_peligro": False,
            "explicacion": "Es una notificación legítima de Google Drive. El remitente es conocido, el nombre del archivo tiene sentido y el formato visual, así como los enlaces implícitos, corresponden al servicio original verificado."
        }
    ]

    for data in desafios_data:
        d = DesafioSimulacion(
            simulacion=sim,
            texto_complementario=data["contexto"],
            es_peligro=data["es_peligro"],
            explicacion=data["explicacion"]
        )
        d.imagen.save(data["filename"], ContentFile(data["svg"].encode('utf-8')), save=True)
        print(f"Creado: {data['filename']}")

    print("¡Simulación de Phishing actualizada con 4 escenarios ultra-realistas!")

if __name__ == '__main__':
    run()
