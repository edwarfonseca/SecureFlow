# 🔐 Sistema de Seguridad — Ingeniería de Software II

Sistema de consola que implementa **autenticación de dos pasos (2FA)** y **verificación de integridad de mensajes** como atributos de calidad de software.

---

## 📋 Requisitos

- Python **3.10 o superior**
- No requiere librerías externas — solo módulos de la librería estándar de Python (`hashlib`, `hmac`, `struct`, `base64`, `time`)

---

## 📁 Estructura del proyecto

```
project/
│
├── main.py                  # Punto de entrada
│
├── auth/
│   ├── __init__.py
│   ├── login.py             # Validación de credenciales
│   └── users.py             # Carga de usuarios desde JSON
│
├── security/
│   ├── __init__.py
│   ├── two_factor.py        # Generación y verificación TOTP (2FA)
│   └── hash_utils.py        # Hash SHA-256 para integridad de mensajes
│
├── communication/
│   ├── __init__.py
│   ├── sender.py            # Empaqueta mensajes con huella digital
│   └── receiver.py          # Verifica integridad al recibir
│
└── data/
    └── users.json           # Base de datos de usuarios
```

---

## ▶️ Cómo ejecutar

### 1. Clona o descarga el repositorio

```bash
git clone https://github.com/tu-usuario/proyecto-seguridad-sw2.git
cd proyecto-seguridad-sw2
```

### 2. Ejecuta el programa

```bash
python main.py
```

> En algunos sistemas puede ser necesario usar `python3` en lugar de `python`.

```bash
python3 main.py
```

### 3. Navega por el menú

Al iniciar verás el siguiente menú:

```
┌─────────────────────────────────────────┐
│         SISTEMA SEGURO — MENÚ           │
├─────────────────────────────────────────┤
│  1. Iniciar sesión (flujo completo)      │
│  2. Demo: credenciales incorrectas       │
│  3. Demo: 2FA incorrecto                 │
│  4. Demo: integridad de mensajes         │
│  5. Salir                                │
└─────────────────────────────────────────┘
```

---

## 👥 Usuarios de prueba

| Usuario | Contraseña    |
|---------|---------------|
| alice   | `password123` |
| bob     | `password`    |

> Las contraseñas se almacenan como hashes SHA-256 en `data/users.json`. Nunca en texto plano.

---

## 🧪 Escenarios de prueba

### ✅ Opción 1 — Inicio de sesión completo (flujo exitoso)

1. Selecciona la opción `1`
2. Ingresa usuario: `alice` y contraseña: `password123`
3. El sistema mostrará el código 2FA generado (simulación)
4. Ingresa ese mismo código
5. Una vez autenticado, escribe un mensaje para ver la verificación de integridad

**Resultado esperado:** acceso concedido → mensaje aceptado → mensaje alterado rechazado

---

### ❌ Opción 2 — Credenciales incorrectas

Selecciona la opción `2`. El sistema intentará autenticarse con credenciales inválidas.

**Resultado esperado:**
```
❌ Credenciales incorrectas. Acceso denegado.
```

---

### ❌ Opción 3 — 2FA incorrecto

Selecciona la opción `3`. Las credenciales son correctas pero el código 2FA es `000000` (inválido).

**Resultado esperado:**
```
✅ Credenciales correctas.
❌ Código 2FA '000000' incorrecto. Acceso denegado.
```

---

### 🔏 Opción 4 — Demo de integridad de mensajes

Selecciona la opción `4`. Se envía un mensaje de prueba y luego se simula su alteración en tránsito.

**Resultado esperado:**
```
✅ INTEGRIDAD VERIFICADA: El mensaje es auténtico y no fue alterado.
❌ ALERTA DE SEGURIDAD: El mensaje fue ALTERADO. Rechazando...
```

---

## 🏛️ Arquitectura

El sistema aplica **separación de responsabilidades** en capas independientes:

| Módulo | Responsabilidad |
|--------|----------------|
| `auth/login.py` | Validación de usuario y contraseña |
| `auth/users.py` | Acceso a la base de datos de usuarios |
| `security/two_factor.py` | Generación y verificación de TOTP (RFC 6238) |
| `security/hash_utils.py` | Generación y verificación de hashes SHA-256 |
| `communication/sender.py` | Empaquetado de mensajes con huella digital |
| `communication/receiver.py` | Verificación de integridad en recepción |

---

## 🔒 Decisiones de seguridad

- **SHA-256** para hashing de contraseñas y huellas de mensajes
- **TOTP (RFC 6238)** implementado desde cero sin librerías externas
- **`hmac.compare_digest()`** para comparaciones seguras (evita ataques de temporización)
- Ventana de tolerancia de ±1 intervalo (30s) en el TOTP para compensar desfases de reloj

---

## 👨‍💻 Autores

- Edwar Esteban Fonseca Jimenez
- Marlon Andres Delgado Lopez


**Curso:** Ingeniería de Software II  
**Institución:** UPTC