"""
auth/login.py
Responsabilidad: Validación de credenciales (usuario + contraseña).
No maneja 2FA — esa lógica vive en security/two_factor.py
"""

import hashlib
from auth.users import get_user


def hash_password(plain_password: str) -> str:
    """
    Genera el hash SHA-256 de una contraseña en texto plano.
    """
    return hashlib.sha256(plain_password.encode()).hexdigest()


def validate_credentials(username: str, password: str) -> bool:
    """
    Valida usuario y contraseña contra los datos almacenados.
    Retorna True si las credenciales son correctas, False en caso contrario.
    """
    user = get_user(username)

    if user is None:
        return False  # Usuario no existe

    stored_hash = user.get("password_hash", "")
    input_hash = hash_password(password)

    return stored_hash == input_hash
