# Guía de Restaurantes

Proyecto desarrollado para la Evaluación 2 de Programación Back End.

La aplicación fue desarrollada con Django y permite gestionar restaurantes mediante un sistema CRUD, autenticación de usuarios y una base de datos PostgreSQL alojada en Supabase.

## Funcionalidades

- Inicio y cierre de sesión.
- Usuarios autenticados.
- Crear restaurantes.
- Listar restaurantes.
- Editar restaurantes.
- Eliminar restaurantes.
- Cada usuario puede gestionar sus propios restaurantes.
- Filtro por tipo de comida.
- Calificación de restaurantes.
- Estado abierto o cerrado.
- Fecha de visita.
- Django Admin personalizado.
- Protección CSRF.
- Validación de formularios.

## Tecnologías utilizadas

- Python
- Django
- PostgreSQL
- Supabase
- HTML
- CSS
- Git
- GitHub

## Base de datos

El proyecto utiliza PostgreSQL mediante Supabase.

La conexión se realiza utilizando una variable de entorno:

```text
DATABASE_URL