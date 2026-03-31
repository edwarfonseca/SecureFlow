"""
auth/users.py
Responsabilidad: Carga y gestión de usuarios desde el archivo de datos.
"""

import json
import os

# Ruta al archivo de usuarios
USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")


def load_users() -> dict:
    """
    Carga el diccionario de usuarios desde el archivo JSON.
    Retorna un dict con los datos de los usuarios.
    """
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def get_user(username: str) -> dict | None:
    """
    Busca y retorna los datos de un usuario por nombre.
    Retorna None si el usuario no existe.
    """
    users = load_users()
    return users.get(username, None)


def user_exists(username: str) -> bool:
    """Verifica si un usuario existe en el sistema."""
    users = load_users()
    return username in users
