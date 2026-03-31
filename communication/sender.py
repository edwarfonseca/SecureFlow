"""
communication/sender.py
Responsabilidad: Preparar y "enviar" mensajes entre sistemas.
Adjunta el hash SHA-256 al mensaje para que el receptor pueda verificar integridad.
"""

from security.hash_utils import generate_hash


def prepare_message(content: str) -> dict:
    """
    Prepara un mensaje para su envío, generando su huella digital (hash).

    Args:
        content: El texto del mensaje a enviar.

    Returns:
        Diccionario con el mensaje y su hash:
        {
            "content": "texto del mensaje",
            "hash": "hash sha-256 del mensaje"
        }
    """
    message_hash = generate_hash(content)
    packet = {
        "content": content,
        "hash": message_hash
    }
    return packet


def send_message(content: str) -> dict:
    """
    Simula el envío de un mensaje al sistema receptor.
    En un sistema real, aquí iría la lógica de red (HTTP, sockets, etc.).

    Args:
        content: El texto del mensaje a enviar.

    Returns:
        El paquete del mensaje listo para ser recibido.
    """
    packet = prepare_message(content)
    print(f"\n  📤 Mensaje preparado para envío.")
    print(f"     Contenido : \"{packet['content']}\"")
    print(f"     Hash      : {packet['hash']}")
    return packet
