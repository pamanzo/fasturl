# FastURL

FastURL es un servicio para acortar URLs, gestionar enlaces personalizados y hacer un seguimiento de las visitas a los enlaces.

## Requisitos

Asegúrate de tener los siguientes requisitos previos instalados:

- Python 3.8+
- PostgreSQL o SQLite (configurable)

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu_usuario/fasturl.git
   cd fasturl

   ```

2. Crea un entorno virtual (recomendado):

   ```python
   python -m venv venv
   source venv/bin/activate # en Windows: venv\Scripts\activate

   ```

3. Instala las dependencias:

   ```python
    pip install -r requirements.txt
   ```

## Variables de entorno

Antes de ejecutar la aplicación, asegúrate de crear un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

````env
SECRET_KEY=tu_clave_secreta
SQLALCHEMY_DATABASE_URL=sqlite:///./fasturl.db # ejemplo


## Ejecución

Para ejecutar el servidor de desarrollo, usa el siguiente comando:

```bash
 uvicorn app.main:app --reload

````

## Endpoints

- **POST /auth/signup:** Registra un nuevo usuario.
- **POST /auth/login:** Inicia sesión con un usuario existente.
- **GET /urls:** Obtiene todos los enlaces de un usuario autenticado.
- **POST /urls:** Crea un nuevo enlace acortado.
- **DELETE /urls/{url_id}:** Elimina un enlace específico de un usuario autenticado.
