"""
security/two_factor.py
Responsabilidad: Generación y verificación del segundo factor (2FA).
Implementa TOTP (Time-based One-Time Password) sin librerías externas.

TOTP funciona así:
  1. Se usa una clave secreta compartida entre el servidor y el usuario.
  2. Se toma el tiempo actual dividido en intervalos de 30 segundos.
  3. Se genera un HMAC-SHA1 de ese contador con la clave secreta.
  4. Se trunca a un número de 6 dígitos.
"""

import hmac
import hashlib
import time
import base64
import struct


def _base32_decode(secret: str) -> bytes:
    """Decodifica una clave en Base32 (formato estándar de TOTP)."""
    # Rellenar con '=' si es necesario
    padding = (8 - len(secret) % 8) % 8
    secret_padded = secret.upper() + "=" * padding
    return base64.b32decode(secret_padded)


def generate_totp(secret: str, interval: int = 30) -> str:
    """
    Genera un código TOTP de 6 dígitos basado en la clave secreta y el tiempo actual.

    Args:
        secret: Clave secreta del usuario en Base32.
        interval: Duración del intervalo en segundos (por defecto 30).

    Returns:
        Código TOTP de 6 dígitos como string.
    """
    key = _base32_decode(secret)

    # Contador: número de intervalos desde la época Unix
    counter = int(time.time()) // interval
    counter_bytes = struct.pack(">Q", counter)  # Big-endian, 8 bytes

    # HMAC-SHA1
    hmac_digest = hmac.new(key, counter_bytes, hashlib.sha1).digest()

    # Truncado dinámico
    offset = hmac_digest[-1] & 0x0F
    truncated = struct.unpack(">I", hmac_digest[offset:offset + 4])[0]
    truncated &= 0x7FFFFFFF  # Quitar bit de signo

    otp = truncated % 1_000_000
    return str(otp).zfill(6)  # Siempre 6 dígitos


def verify_totp(secret: str, user_code: str, window: int = 1) -> bool:
    """
    Verifica si el código ingresado por el usuario es válido.
    Acepta un margen de ±window intervalos para compensar desfase de tiempo.

    Args:
        secret: Clave secreta del usuario en Base32.
        user_code: Código ingresado por el usuario.
        window: Número de intervalos de tolerancia (±).

    Returns:
        True si el código es válido, False en caso contrario.
    """
    for delta in range(-window, window + 1):
        # Generar código para el intervalo actual ± delta
        key = _base32_decode(secret)
        counter = int(time.time()) // 30 + delta
        counter_bytes = struct.pack(">Q", counter)

        hmac_digest = hmac.new(key, counter_bytes, hashlib.sha1).digest()
        offset = hmac_digest[-1] & 0x0F
        truncated = struct.unpack(">I", hmac_digest[offset:offset + 4])[0]
        truncated &= 0x7FFFFFFF
        otp = str(truncated % 1_000_000).zfill(6)

        if hmac.compare_digest(otp, user_code.strip()):
            return True

    return False


def get_user_secret(username: str) -> str | None:
    """
    Obtiene la clave secreta 2FA de un usuario.
    """
    from auth.users import get_user
    user = get_user(username)
    if user:
        return user.get("secret_key", None)
    return None
