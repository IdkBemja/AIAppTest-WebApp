# ![UrraHosting Logo](https://github.com/IdkBemja/Urrahost/blob/main/assets/imgs/logo.png)

# AI Chat Test (Web & Mobile Backend)

**Hosted on [UrraHosting](https://urrahost.app)**

**Production URL:** [https://aichattest.urrahost.app](https://aichattest.urrahost.app)

AI Chat Test es una plataforma de backend en Python Flask con MySQL, diseñada para servir como base de un sistema de chat con IA, integrable tanto con una app web como con una futura app móvil Android.

## Características principales
- Registro y login de usuarios con credenciales y token de IA.
- Generación y validación de JWT para autenticación segura.
- Envío de preguntas a modelos de IA (OpenAI) usando el token personalizado de cada usuario.
- Blacklist de JWT para logout seguro y protección ante tokens comprometidos.
- Endpoint para refrescar el JWT antes de su expiración.
- Inicialización automática de bases de datos y tablas requeridas.

## Endpoints REST

- `POST /api/register` — Registro de usuario (username, password, token IA).
- `POST /api/login` — Login, devuelve JWT con username y token IA.
- `POST /api/ask` — Enviar pregunta a la IA (requiere JWT en header Authorization).
- `POST /api/logout` — Logout, agrega el JWT a la blacklist.
- `POST /api/refresh-token` — Refresca el JWT si está por expirar.

## Seguridad
- Contraseñas hasheadas con bcrypt.
- JWT firmado y con expiración.
- Blacklist de JWT en MySQL para invalidar tokens tras logout.
- Validación estricta de datos de entrada.

## Inicialización automática
Al iniciar la app (ver `main.py`), se verifica y crea automáticamente:
- Bases de datos configuradas en `.env` (`DB_NAME`, `DB_Blacklist_JWT`)
- Tablas `users` y `jwt_blacklist` si no existen.

## Requisitos
- Python 3.8+
- MySQL
- Paquetes: flask, flask-bcrypt, pymysql, python-dotenv, openai

## Configuración
Crea un archivo `.env` con las siguientes variables:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=usuario
DB_PASSWORD=contraseña
DB_NAME=ai_chat_db
DB_Blacklist_JWT=ai_chat_blacklist_db  # (opcional, puede ser igual a DB_NAME)
SECRET_KEY=clave_secreta_para_jwt
```

## Ejecución
```bash
python main.py
```

---

## 📱 Futuro: App Móvil Android (AI Chat Test)

La app móvil (Android Studio, Java/Kotlin) se conectará a este backend y tendrá:
- **Pantalla de Login:**
  - Envía credenciales a `/api/login` y recibe JWT con username y token IA.
- **Pantalla de Chat:**
  - Envía preguntas a `/api/ask` usando el JWT en el header.
  - Muestra la respuesta de la IA recibida del backend.
- **Logout:**
  - Llama a `/api/logout` para invalidar el JWT.
- **Refresh Token:**
  - Llama a `/api/refresh-token` para renovar el JWT antes de que expire.

**Nota:** La app móvil no almacena información sensible, solo el JWT y el token IA temporalmente en memoria.

---

## Estructura del proyecto

```
main.py
app/
    controllers/
        api_controller.py
        app_controller.py
    models/
        Users.py
    utils/
        config/
            env_config.py
        mysqlconnection.py
        mysqlhandler.py
        jwt.py
        OpenAIUtil.py
    static/
        css/
        js/
    templates/
        index.html
```

---

## Licencia
MIT
