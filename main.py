"""
main.py
Punto de entrada de la aplicación.
Orquesta los módulos de autenticación, 2FA y comunicación segura.

Escenarios cubiertos:
  Autenticación:
    ✅ Credenciales correctas + 2FA correcto → acceso permitido
    ❌ Credenciales incorrectas → acceso denegado
    ❌ 2FA incorrecto → acceso denegado

  Integridad:
    ✅ Mensaje íntegro → aceptado
    ❌ Mensaje alterado → rechazado
"""

from auth.login import validate_credentials
from security.two_factor import verify_totp, generate_totp, get_user_secret
from communication.sender import send_message
from communication.receiver import receive_message, tamper_message


# ─────────────────────────────────────────────
#  UTILIDADES DE CONSOLA
# ─────────────────────────────────────────────

def separator(title: str = "") -> None:
    line = "─" * 55
    if title:
        print(f"\n{line}")
        print(f"  {title}")
        print(f"{line}")
    else:
        print(f"\n{line}")


def menu_principal() -> str:
    print("\n┌─────────────────────────────────────────┐")
    print("│         SISTEMA SEGURO — MENÚ           │")
    print("├─────────────────────────────────────────┤")
    print("│  1. Iniciar sesión (flujo completo)      │")
    print("│  2. Demo: credenciales incorrectas       │")
    print("│  3. Demo: 2FA incorrecto                 │")
    print("│  4. Demo: integridad de mensajes         │")
    print("│  5. Salir                                │")
    print("└─────────────────────────────────────────┘")
    return input("\n  Selecciona una opción [1-5]: ").strip()


# ─────────────────────────────────────────────
#  FLUJO DE AUTENTICACIÓN
# ─────────────────────────────────────────────

def flujo_login() -> str | None:
    """
    Ejecuta el flujo completo de autenticación:
    1. Solicita usuario y contraseña.
    2. Valida credenciales.
    3. Solicita código 2FA.
    4. Retorna el nombre de usuario si todo es correcto, None si falla.
    """
    separator("MÓDULO DE AUTENTICACIÓN")

    username = input("\n  Usuario   : ").strip()
    password  = input("  Contraseña: ").strip()

    # — Paso 1: validar credenciales —
    print("\n  🔐 Validando credenciales...")
    if not validate_credentials(username, password):
        print("  ❌ Credenciales incorrectas. Acceso denegado.")
        return None

    print("  ✅ Credenciales correctas.")

    # — Paso 2: solicitar 2FA —
    separator("MÓDULO 2FA")
    secret = get_user_secret(username)

    # Mostramos el código generado (en producción esto va al teléfono/app)
    current_code = generate_totp(secret)
    print(f"\n  📱 [SIMULACIÓN] Código 2FA generado para '{username}': {current_code}")
    print("     (En producción este código llega a tu app autenticadora)")

    user_code = input("\n  Ingresa el código 2FA: ").strip()

    print("\n  🔑 Verificando segundo factor...")
    if not verify_totp(secret, user_code):
        print("  ❌ Código 2FA incorrecto. Acceso denegado.")
        return None

    print(f"  ✅ 2FA correcto. ¡Bienvenido, {username}!")
    return username


# ─────────────────────────────────────────────
#  FLUJO DE MENSAJERÍA SEGURA
# ─────────────────────────────────────────────

def flujo_mensajeria(username: str) -> None:
    """
    Permite al usuario enviar mensajes y demuestra la verificación de integridad.
    """
    separator("MÓDULO DE COMUNICACIÓN SEGURA")

    message_text = input(f"\n  [{username}] Escribe tu mensaje: ").strip()

    # Envío
    packet = send_message(message_text)

    # Recepción normal
    separator("SISTEMA RECEPTOR — Mensaje original")
    receive_message(packet)

    # Demostración de mensaje alterado
    separator("SISTEMA RECEPTOR — Mensaje alterado (simulación)")
    tampered = tamper_message(packet, message_text + " [MODIFICADO]")
    receive_message(tampered)


# ─────────────────────────────────────────────
#  DEMOS DE ESCENARIOS
# ─────────────────────────────────────────────

def demo_credenciales_incorrectas() -> None:
    separator("DEMO — Credenciales incorrectas")
    print("\n  Intentando login con: usuario='hacker', contraseña='wrongpass'")
    resultado = validate_credentials("hacker", "wrongpass")
    if not resultado:
        print("  ❌ Credenciales incorrectas. Acceso denegado.")
    else:
        print("  ✅ Acceso concedido (no debería llegar aquí)")


def demo_2fa_incorrecto() -> None:
    separator("DEMO — 2FA incorrecto")
    print("\n  Credenciales de 'alice' correctas, pero 2FA erróneo.")
    creds_ok = validate_credentials("alice", "password123")
    if creds_ok:
        print("  ✅ Credenciales correctas.")
        code_ok = verify_totp(get_user_secret("alice"), "000000")  # Código inválido
        if not code_ok:
            print("  ❌ Código 2FA '000000' incorrecto. Acceso denegado.")
        else:
            print("  ✅ 2FA correcto (improbable con 000000)")


def demo_integridad() -> None:
    separator("DEMO — Integridad de mensajes")

    test_message = "Transferencia autorizada: $10,000 a cuenta 987654321"
    packet = send_message(test_message)

    separator("  → Mensaje SIN alterar")
    receive_message(packet)

    separator("  → Mensaje CON alteración")
    tampered = tamper_message(packet, "Transferencia autorizada: $99,999 a cuenta 111111111")
    receive_message(tampered)


# ─────────────────────────────────────────────
#  ENTRADA PRINCIPAL
# ─────────────────────────────────────────────

def main():
    print("\n╔═════════════════════════════════════════════╗")
    print("║   SISTEMA DE SEGURIDAD — Ingeniería SW II   ║")
    print("║   Autenticación 2FA + Integridad de mensajes║")
    print("╚═════════════════════════════════════════════╝")
    print("\n  Usuarios disponibles: alice (pass: password123)")
    print("                        bob   (pass: password)")

    while True:
        opcion = menu_principal()

        if opcion == "1":
            usuario = flujo_login()
            if usuario:
                flujo_mensajeria(usuario)

        elif opcion == "2":
            demo_credenciales_incorrectas()

        elif opcion == "3":
            demo_2fa_incorrecto()

        elif opcion == "4":
            demo_integridad()

        elif opcion == "5":
            print("\n  👋 Cerrando sistema. ¡Hasta luego!\n")
            break

        else:
            print("\n  ⚠️  Opción no válida. Intenta de nuevo.")

        input("\n  [Enter para continuar...]")


if __name__ == "__main__":
    main()
