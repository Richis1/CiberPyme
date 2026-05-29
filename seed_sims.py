import os
import django
import sys

# Añadir el path del proyecto al sys.path
sys.path.append('c:/Users/Ricar/OneDrive/Documentos/pymes')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from principal.models import Simulacion, DesafioSimulacion

def run():
    print("Iniciando seed de simulaciones...")
    s1, created = Simulacion.objects.get_or_create(
        titulo="Detección de Phishing",
        defaults={
            'descripcion': "Aprende a identificar correos electrónicos maliciosos que intentan robar tus credenciales.",
            'icono': "bi-envelope-exclamation",
            'puntos': 100
        }
    )
    
    # Limpiar desafíos previos si existen (opcional)
    # s1.desafios.all().delete()
    
    # Desafío 1: Phishing
    DesafioSimulacion.objects.get_or_create(
        simulacion=s1,
        imagen="simulaciones/phishing.png",
        defaults={
            'texto_complementario': "Has recibido un correo de 'soporte@seguridad-servidor.com' pidiendo una verificación urgente.",
            'es_peligro': True,
            'explicacion': "¡Correcto! Este es un caso clásico de phishing. Fíjate en el dominio falso y el tono de urgencia innecesario."
        }
    )
    
    # Desafío 2: Seguro
    DesafioSimulacion.objects.get_or_create(
        simulacion=s1,
        imagen="simulaciones/safe.png",
        defaults={
            'texto_complementario': "Un compañero te envía un mensaje por Teams preguntando por el estado de un proyecto.",
            'es_peligro': False,
            'explicacion': "Correcto. Este mensaje es seguro. Es una comunicación habitual y no pide información sensible ni contiene enlaces sospechosos."
        }
    )

    print("Simulaciones creadas con éxito.")

if __name__ == "__main__":
    run()
