import os
import django
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from principal.models import Simulacion, DesafioSimulacion

def run():
    sim, created = Simulacion.objects.get_or_create(
        titulo="Ataque de Ransomware",
        defaults={
            "descripcion": "Identifica los diferentes vectores de ataque que pueden llevar a una infección por Ransomware. Selecciona las amenazas reales para evitar el secuestro de información.",
            "icono": "bi-shield-lock-fill",
            "puntos": 150
        }
    )
    if not created:
        print("La simulación ya existe. Eliminando desafíos anteriores...")
        sim.desafios.all().delete()

    desafios_data = [
        {
            "filepath": r"C:\Users\Ricar\.gemini\antigravity\brain\2712bd55-2b88-4edd-87c1-5101b4535ebb\ransomware_email_attachment_1777513396902.png",
            "texto_complementario": "Recibes este correo urgente sobre una factura pendiente con un archivo adjunto.",
            "es_peligro": True,
            "explicacion": "Es un claro ataque de suplantación (Phishing). El archivo tiene una doble extensión '.pdf.exe', que engaña al usuario para que ejecute el malware."
        },
        {
            "filepath": r"C:\Users\Ricar\.gemini\antigravity\brain\2712bd55-2b88-4edd-87c1-5101b4535ebb\fake_antivirus_popup_1777513489842.png",
            "texto_complementario": "Mientras navegas en un sitio de noticias, te aparece este mensaje en rojo.",
            "es_peligro": True,
            "explicacion": "Es un falso pop-up de antivirus (Scareware) intentando asustarte. Hacer clic descargará e instalará ransomware en tu equipo."
        },
        {
            "filepath": r"C:\Users\Ricar\.gemini\antigravity\brain\2712bd55-2b88-4edd-87c1-5101b4535ebb\legitimate_system_update_1777513515366.png",
            "texto_complementario": "Aparece un pequeño mensaje en la esquina inferior derecha de tu pantalla.",
            "es_peligro": False,
            "explicacion": "Es una notificación legítima de actualización del sistema. Instalar parches de seguridad a tiempo es vital para protegerte del ransomware."
        }
    ]

    for data in desafios_data:
        try:
            with open(data["filepath"], 'rb') as f:
                file_content = f.read()
            
            filename = os.path.basename(data["filepath"])
            
            d = DesafioSimulacion(
                simulacion=sim,
                texto_complementario=data["texto_complementario"],
                es_peligro=data["es_peligro"],
                explicacion=data["explicacion"]
            )
            d.imagen.save(filename, ContentFile(file_content), save=False)
            d.save()
            print(f"Desafío {filename} creado exitosamente.")
        except Exception as e:
            print(f"Error creando desafío: {e}")

    print("¡Simulación de Ransomware creada!")

if __name__ == '__main__':
    run()
