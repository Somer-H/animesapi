"""
Servicio para enviar notificaciones push via Firebase Cloud Messaging (FCM).

Para activar notificaciones reales necesitas:
1. Crear un proyecto en Firebase Console (https://console.firebase.google.com)
2. Descargar el archivo 'google-services.json' para la app Android
3. Generar una Service Account Key (JSON) para el backend
4. Guardar la ruta del JSON en el .env como: GOOGLE_APPLICATION_CREDENTIALS=ruta/al/archivo.json

Por ahora el módulo registra los envíos en consola si no hay credenciales configuradas.
"""

import os
import json
import logging

logger = logging.getLogger(__name__)


def send_push_notification(fcm_tokens: list[str], title: str, body: str, data: dict = None):
    """
    Envía una notificación push a una lista de tokens FCM.
    Usa el SDK de Firebase Admin si está configurado, si no registra en consola.
    """
    if not fcm_tokens:
        print("[FCM] No hay tokens para enviar.")
        return False

    try:
        import firebase_admin
        from firebase_admin import credentials, messaging

        # Inicializar Firebase Admin SDK (solo una vez)
        if not firebase_admin._apps:
            cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            
            if not cred_path:
                print("[FCM-AVISO] GOOGLE_APPLICATION_CREDENTIALS no está definido en el .env")
                _log_notifications(fcm_tokens, title, body, data)
                return False

            # Intentar resolver ruta absoluta si es relativa
            if not os.path.isabs(cred_path):
                # Asumimos que el JSON está en la raíz de la 'api' (un nivel arriba de 'tags')
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                cred_path = os.path.join(base_dir, cred_path)

            if not os.path.exists(cred_path):
                print(f"[FCM-ERROR] No se encontró el archivo de credenciales en: {cred_path}")
                _log_notifications(fcm_tokens, title, body, data)
                return False

            print(f"[FCM] Inicializando con credenciales: {cred_path}")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        # Construir el payload de datos
        payload = {
            "titulo": title,
            "cuerpo": body
        }
        if data:
            payload.update({k: str(v) for k, v in data.items()})

        # Configuración específica de Android
        android_config = messaging.AndroidConfig(
            priority="high",
            notification=messaging.AndroidNotification(
                channel_id="anime_notifications",
                tag="anime_new",
                click_action="TOP_LEVEL_ACTIVITY"
            )
        )

        message = messaging.MulticastMessage(
            tokens=fcm_tokens,
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=payload,
            android=android_config
        )

        print(f"[FCM] Intentando enviar notificación a {len(fcm_tokens)} dispositivos...")
        response = messaging.send_each_for_multicast(message)
        
        success_count = response.success_count
        failure_count = response.failure_count
        
        print(f"[FCM] Resultado: {success_count} exitosas, {failure_count} fallidas.")
        
        if failure_count > 0:
            for idx, resp in enumerate(response.responses):
                if not resp.success:
                    print(f"  - Error en token {fcm_tokens[idx][:15]}...: {resp.exception}")

        return success_count > 0

    except ImportError:
        print("[FCM-ERROR] 'firebase-admin' no instalado. Usando simulador.")
        _log_notifications(fcm_tokens, title, body, data)
        return False
    except Exception as e:
        print(f"[FCM-EXCEPTION] Error crítico: {e}")
        logger.error(f"[FCM] Error enviando notificaciones: {e}")
        return False


def _log_notifications(tokens: list[str], title: str, body: str, data: dict):
    """Fallback: imprime en consola cuando Firebase no está configurado."""
    print(f"\n🔔 [NOTIFICACIÓN SIMULADA] '{title}': {body} → {len(tokens)} destinatarios")
    if data:
        print(f"   Data: {data}")
