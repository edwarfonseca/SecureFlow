"""
communication/receiver.py
Responsabilidad: Recibir mensajes y verificar su integridad mediante el hash.
Rechaza cualquier mensaje cuyo contenido no coincida con el hash adjunto.
"""

from security.hash_utils import verify_hash, display_hash_info


def receive_message(packet: dict, verbose: bool = True) -> bool:
    """
    Recibe un paquete de mensaje y verifica su integridad.

    Args:
        packet: Diccionario con 'content' y 'hash'.
        verbose: Si True, muestra detalles del proceso de verificación.

    Returns:
        True si el mensaje es íntegro, False si fue alterado.
    """
    content = packet.get("content", "")
    received_hash = packet.get("hash", "")

    print(f"\n  📥 Mensaje recibido.")
    print(f"     Contenido : \"{content}\"")

    if verbose:
        display_hash_info(content, received_hash)

    is_valid = verify_hash(content, received_hash)

    if is_valid:
        print("\n  ✅ INTEGRIDAD VERIFICADA: El mensaje es auténtico y no fue alterado.")
    else:
        print("\n  ❌ ALERTA DE SEGURIDAD: El mensaje fue ALTERADO. Rechazando...")

    return is_valid


def tamper_message(packet: dict, new_content: str) -> dict:
    """
    Simula la alteración de un mensaje en tránsito (para pruebas/demostración).
    Modifica el contenido pero deja el hash original intacto.

    Args:
        packet: El paquete original.
        new_content: El contenido alterado.

    Returns:
        Un nuevo paquete con el contenido modificado pero el hash original.
    """
    tampered = {
        "content": new_content,
        "hash": packet["hash"]  # Hash original — no corresponde al nuevo contenido
    }
    print(f"\n  ⚠️  [SIMULACIÓN] Mensaje alterado en tránsito.")
    print(f"     Original  : \"{packet['content']}\"")
    print(f"     Alterado  : \"{new_content}\"")
    return tampered
