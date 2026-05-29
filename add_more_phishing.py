import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from principal.models import Simulacion, DesafioSimulacion

SVG_SPEAR_HR = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="background:#f3f2f1; font-family:'Segoe UI', sans-serif;">
  <rect width="900" height="48" fill="#0f6cbd"/>
  <text x="50" y="32" fill="#fff" font-size="16" font-weight="600">Outlook</text>
  <rect x="250" y="8" width="400" height="32" fill="rgba(255,255,255,0.8)" rx="4"/>
  <rect x="200" y="48" width="700" height="552" fill="#fff"/>
  <circle cx="240" cy="100" r="24" fill="#0078d4"/>
  <text x="227" y="108" fill="#fff" font-size="20" font-weight="600">RH</text>
  <text x="280" y="90" fill="#242424" font-size="20" font-weight="600">Urgente: Revisión de nueva política salarial 2026</text>
  <text x="280" y="115" fill="#242424" font-size="14" font-weight="600">Recursos Humanos</text>
  <text x="420" y="115" fill="#605e5c" font-size="12">&lt;recursos.humanos@portal-empleado-cyberpyme.com&gt;</text>
  <rect x="200" y="155" width="700" height="1" fill="#e1dfdd"/>
  <text x="240" y="195" fill="#242424" font-size="15">Hola Carlos,</text>
  <text x="240" y="235" fill="#242424" font-size="15">Adjunto el documento confidencial sobre los ajustes salariales para el</text>
  <text x="240" y="260" fill="#242424" font-size="15">departamento de Contabilidad, aprobados para este semestre.</text>
  <text x="240" y="295" fill="#242424" font-size="15">Por favor, revisa el documento en nuestro portal seguro antes de las 5 PM:</text>
  <rect x="240" y="320" width="280" height="40" fill="#0f6cbd" rx="4"/>
  <text x="260" y="346" fill="#fff" font-size="15" font-weight="600">Acceder a SharePoint Seguro</text>
  <text x="240" y="380" fill="#0f6cbd" font-size="13" text-decoration="underline">https://portal-empleado-cyberpyme.com/sharepoint/login</text>
  <text x="240" y="430" fill="#242424" font-size="15">Saludos,</text>
  <text x="240" y="450" fill="#242424" font-size="15">Dirección de Recursos Humanos</text>
</svg>"""

SVG_WHALING = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="background:#ffffff; font-family:'Helvetica Neue', sans-serif;">
  <rect x="0" y="0" width="900" height="600" fill="#fff"/>
  <rect x="0" y="0" width="900" height="60" fill="#f2f2f2" stroke="#d1d1d1" stroke-width="1"/>
  <text x="30" y="38" fill="#333" font-size="20" font-weight="bold">Bandeja de Entrada - Mail</text>
  <circle cx="50" cy="110" r="25" fill="#555"/>
  <text x="37" y="118" fill="#fff" font-size="20">RD</text>
  <text x="90" y="105" fill="#000" font-size="22" font-weight="bold">Transferencia confidencial</text>
  <text x="90" y="125" fill="#333" font-size="14" font-weight="bold">Roberto Díaz (CEO)</text>
  <text x="240" y="125" fill="#888" font-size="14">&lt;roberto.diaz.ceo@yahoo.com&gt;</text>
  <rect x="30" y="150" width="840" height="1" fill="#ddd"/>
  <text x="50" y="200" fill="#000" font-size="16">Hola,</text>
  <text x="50" y="230" fill="#000" font-size="16">Estoy en una reunión importante con unos nuevos socios europeos y no puedo hablar</text>
  <text x="50" y="255" fill="#000" font-size="16">por teléfono. Necesitamos cerrar una adquisición hoy mismo.</text>
  <text x="50" y="290" fill="#000" font-size="16">Necesito que proceses una transferencia bancaria internacional por $45,000 USD</text>
  <text x="50" y="315" fill="#000" font-size="16">a la cuenta del nuevo proveedor. Mantén esto de forma confidencial hasta que</text>
  <text x="50" y="340" fill="#000" font-size="16">anunciemos la adquisición la próxima semana.</text>
  <text x="50" y="380" fill="#000" font-size="16">Contéstame a este correo para enviarte los datos de la cuenta inmediatamente.</text>
  <text x="50" y="430" fill="#000" font-size="16">Enviado desde mi iPhone</text>
</svg>"""

SVG_AMAZON = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="background:#f2f2f2; font-family:'Amazon Ember', Arial, sans-serif;">
  <rect x="150" y="30" width="600" height="520" fill="#fff" rx="4" stroke="#ddd" stroke-width="1"/>
  <rect x="150" y="30" width="600" height="80" fill="#232f3e" rx="4"/>
  <text x="380" y="80" fill="#fff" font-size="32" font-weight="bold">amazon</text>
  <path d="M 385 88 Q 420 100 455 88" fill="none" stroke="#ff9900" stroke-width="3"/>
  <polygon points="450,83 460,88 450,93" fill="#ff9900"/>
  <text x="190" y="150" fill="#0f1111" font-size="24" font-weight="bold">Problema con tu método de pago</text>
  <text x="190" y="190" fill="#0f1111" font-size="16">Estimado cliente,</text>
  <text x="190" y="220" fill="#0f1111" font-size="16">No pudimos procesar el pago de tu último pedido de Amazon Prime.</text>
  <text x="190" y="245" fill="#0f1111" font-size="16">Tu suscripción ha sido suspendida temporalmente.</text>
  <rect x="190" y="280" width="520" height="100" fill="#f6f6f6" stroke="#ddd"/>
  <text x="210" y="310" fill="#0f1111" font-size="16">Monto adeudado: $99.00 MXN</text>
  <text x="210" y="340" fill="#0f1111" font-size="16">Tarjeta rechazada: Visa terminada en ****</text>
  <rect x="190" y="400" width="300" height="40" fill="#ffd814" rx="4"/>
  <text x="240" y="425" fill="#0f1111" font-size="16" font-weight="bold">Actualizar método de pago</text>
  <text x="190" y="470" fill="#007185" font-size="14" text-decoration="underline">https://amazon.com-seguridad-pagos.net/update</text>
  <text x="190" y="520" fill="#565959" font-size="12">Por favor no responda a este correo electrónico. Este buzón no se supervisa.</text>
</svg>"""

SVG_LINKEDIN = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="600" viewBox="0 0 900 600" style="background:#f3f2ef; font-family:-apple-system, system-ui, sans-serif;">
  <rect x="200" y="40" width="500" height="500" fill="#fff" stroke="#e0e0e0" stroke-width="1"/>
  <rect x="200" y="40" width="500" height="60" fill="#0a66c2"/>
  <text x="230" y="78" fill="#fff" font-size="28" font-weight="bold">in</text>
  <text x="230" y="140" fill="#000000" font-size="20" font-weight="bold">Apareciste en 18 búsquedas esta semana</text>
  <rect x="230" y="160" width="440" height="1" fill="#e0e0e0"/>
  <circle cx="260" cy="210" r="30" fill="#b3b3b3"/>
  <text x="310" y="200" fill="#000000" font-size="16" font-weight="bold">Reclutador Senior</text>
  <text x="310" y="220" fill="#666666" font-size="14">Te ha enviado un mensaje directo:</text>
  <rect x="230" y="260" width="440" height="100" fill="#f3f2ef" rx="8"/>
  <text x="250" y="290" fill="#000000" font-size="15">"Hola, tu perfil encaja perfectamente con un puesto directivo</text>
  <text x="250" y="315" fill="#000000" font-size="15">que estamos manejando con un salario de $10,000 USD al mes.</text>
  <text x="250" y="340" fill="#000000" font-size="15">Revisa la descripción del puesto y aplica aquí:"</text>
  <rect x="230" y="390" width="200" height="40" fill="#0a66c2" rx="20"/>
  <text x="280" y="415" fill="#fff" font-size="16" font-weight="bold">Ver Oferta</text>
  <text x="230" y="450" fill="#0a66c2" font-size="14" text-decoration="underline">http://linkedin-jobs-secure.com/oferta/84920</text>
</svg>"""

def run():
    try:
        sim = Simulacion.objects.get(titulo__icontains="Phishing")
    except Simulacion.DoesNotExist:
        print("La simulación no existe.")
        return

    # Increment points since it's a longer simulation now
    sim.puntos = 400
    sim.save()

    desafios_data = [
        {
            "svg": SVG_SPEAR_HR,
            "filename": "hr_spear_phishing.svg",
            "contexto": "Recibes este correo electrónico de Recursos Humanos dirigido específicamente a ti.",
            "es_peligro": True,
            "explicacion": "Ataque de 'Spear Phishing' (Phishing Dirigido). Los atacantes usaron tu nombre y departamento para ganar confianza. El dominio 'portal-empleado-cyberpyme.com' es un dominio falso diseñado para parecerse a la intranet real de la empresa."
        },
        {
            "svg": SVG_WHALING,
            "filename": "ceo_whaling_fraud.svg",
            "contexto": "Trabajas en finanzas y recibes este correo directamente de tu CEO.",
            "es_peligro": True,
            "explicacion": "Fraude del CEO o 'Whaling'. El atacante suplanta la identidad de un alto directivo, pide confidencialidad y urgencia para saltarse los protocolos normales de transferencias bancarias. Fíjate que el correo fue enviado desde un '@yahoo.com'."
        },
        {
            "svg": SVG_AMAZON,
            "filename": "amazon_clone_phishing.svg",
            "contexto": "Recibes un correo de alerta en tu cuenta personal sobre una suscripción.",
            "es_peligro": True,
            "explicacion": "Ataque de 'Clone Phishing'. Copian el diseño de empresas famosas (como Amazon, Netflix o Bancos) para informarte de un falso problema de pago. El dominio en la parte inferior es falso y busca robar los datos de tu tarjeta."
        },
        {
            "svg": SVG_LINKEDIN,
            "filename": "linkedin_phishing.svg",
            "contexto": "Recibes un mensaje en LinkedIn sobre una increíble oferta de trabajo.",
            "es_peligro": True,
            "explicacion": "Phishing en Redes Sociales. Promesas de altos salarios con perfiles falsos de reclutadores buscan que hagas clic en un enlace externo malicioso que puede descargar malware o robar tus datos de acceso de LinkedIn."
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
        print(f"Creado nuevo desafío: {data['filename']}")

    print(f"¡Se han agregado 4 desafíos adicionales! Ahora la simulación tiene {sim.desafios.count()} desafíos.")

if __name__ == '__main__':
    run()
