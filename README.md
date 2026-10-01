# Guía de Restaurantes

Aplicación web hecha con Django para registrar restaurantes visitados, con su tipo de comida, calificación, estado y fecha de visita. Proyecto de la Evaluación 2 (Caso 3).

## Tecnologías
- Python y Django
- PostgreSQL en Supabase
- python-decouple y dj-database-url para leer la configuración desde el archivo .env

## Cómo ejecutarlo
1. Clonar el repositorio y crear un entorno virtual:
   `python -m venv venv` y luego `.\venv\Scripts\Activate.ps1`
2. Instalar las dependencias: `pip install -r requirements.txt`
3. Crear un archivo `.env` en la raíz con una línea: `DATABASE_URL=` seguida de la cadena de conexión de Supabase (Session pooler).
4. Aplicar las migraciones: `python manage.py migrate`
5. Crear un administrador: `python manage.py createsuperuser`
6. Iniciar el servidor: `python manage.py runserver`

## Seguridad
El archivo `.env` está en `.gitignore`, así que la contraseña de la base de datos no se sube a GitHub.

## Equipo
- Catalina Navarrete
- Ignacio Cancino
- Luis Ramirez
- Facundo Carotta