"""
security/hash_utils.py
Responsabilidad: Generación y verificación de hashes para integridad de mensajes.
Utiliza SHA-256 de la librería estándar hashlib.
"""

import hashlib
import hmac


def generate_hash(message: str) -> str:
    """
    Genera el hash SHA-256 de un mensaje.

    Args:
        message: El contenido del mensaje en texto plano.

    Returns:
        Hash SHA-256 como cadena hexadecimal (64 caracteres).
    """
    return hashlib.sha256(message.encode("utf-8")).hexdigest()


def verify_hash(message: str, expected_hash: str) -> bool:
    """
    Verifica la integridad de un mensaje comparando su hash con el esperado.
    Usa hmac.compare_digest para evitar ataques de temporización.

    Args:
        message: El mensaje recibido.
        expected_hash: El hash original enviado junto con el mensaje.

    Returns:
        True si el mensaje no fue alterado, False si fue modificado.
    """
    computed_hash = generate_hash(message)
    return hmac.compare_digest(computed_hash, expected_hash)


def display_hash_info(message: str, message_hash: str) -> None:
    """
    Muestra información de depuración sobre el hash de un mensaje.
    """
    computed = generate_hash(message)
    print(f"\n  📋 Hash esperado  : {message_hash}")
    print(f"  📋 Hash calculado : {computed}")
    print(f"  {'✅ Coinciden' if computed == message_hash else '❌ No coinciden'}")
