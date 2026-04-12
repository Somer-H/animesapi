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
        return

    try:
        import firebase_admin
        from firebase_admin import credentials, messaging

        # Inicializar Firebase Admin SDK (solo una vez)
        if not firebase_admin._apps:
            cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if not cred_path or not os.path.exists(cred_path):
                _log_notifications(fcm_tokens, title, body, data)
                return
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)

        # Construir el mensaje multicast
        message = messaging.MulticastMessage(
            tokens=fcm_tokens,
            notification=messaging.Notification(title=title, body=body),
            data={k: str(v) for k, v in (data or {}).items()},
            android=messaging.AndroidConfig(priority="high")
        )
        response = messaging.send_each_for_multicast(message)
        logger.info(f"[FCM] Enviadas {response.success_count}/{len(fcm_tokens)} notificaciones para: {title}")

    except ImportError:
        # firebase-admin no instalado → registrar en consola
        _log_notifications(fcm_tokens, title, body, data)
    except Exception as e:
        logger.error(f"[FCM] Error enviando notificaciones: {e}")


def _log_notifications(tokens: list[str], title: str, body: str, data: dict):
    """Fallback: imprime en consola cuando Firebase no está configurado."""
    logger.info(f"[FCM-SIMULADO] → {len(tokens)} dispositivos")
    logger.info(f"  Título: {title}")
    logger.info(f"  Cuerpo: {body}")
    logger.info(f"  Data:   {data}")
    print(f"\n🔔 [NOTIFICACIÓN SIMULADA] '{title}': {body} → {len(tokens)} destinatarios")
