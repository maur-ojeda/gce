# Gestor de Cursos Escolares (GCE)

Este es un proyecto de aplicación web para la gestión de cursos escolares, construido con el framework [Reflex](https://reflex.dev/) en Python. La aplicación permite a los administradores gestionar los cursos y a los estudiantes inscribirse en ellos.

## Características

La aplicación cuenta con dos roles de usuario principales: Administrador y Estudiante.

### Administrador

*   **Gestión de Cursos:**
    *   Crear, leer, actualizar y eliminar cursos.
    *   Ver una lista de todos los cursos con su información detallada.
    *   Asignar profesores a los cursos.
    *   Establecer el número de cupos para cada curso.

### Estudiante

*   **Inscripción a Cursos:**
    *   Ver una lista de los cursos en los que está inscrito.
    *   Ver una lista de los cursos disponibles para inscribirse.
    *   Inscribirse y darse de baja de los cursos.
    *   Ver los detalles de cada curso, incluyendo el profesor, el horario y la descripción.

## Tech Stack

*   **Framework:** [Reflex](https://reflex.dev/) (Python)
*   **Lenguaje:** Python 3

## Instalación y Configuración

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### Prerrequisitos

*   Python 3.8 o superior
*   pip

### Pasos de Instalación

1.  **Clona el repositorio:**

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd gce
    ```

2.  **Crea un entorno virtual:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
    *En Windows, usa `.venv\Scripts\activate`*

3.  **Instala las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Inicializa y ejecuta la aplicación:**

    ```bash
    reflex init
    reflex run
    ```

La aplicación estará disponible en `http://localhost:3000`.

## Estructura del Proyecto

El proyecto está estructurado de la siguiente manera:

```
/
├── gce/
│   ├── __init__.py
│   ├── gce.py              # Punto de entrada de la aplicación
│   ├── models.py           # Modelos de datos (Pydantic)
│   ├── state.py            # Estado global de la aplicación
│   ├── components/         # Componentes de la interfaz de usuario
│   │   ├── __init__.py
│   │   ├── cards.py
│   │   ├── forms.py
│   │   └── ...
│   ├── pages/              # Páginas de la aplicación
│   │   ├── admin.py        # Vista y lógica del administrador
│   │   └── student.py      # Vista y lógica del estudiante
│   └── ...
├── requirements.txt        # Dependencias de Python
└── ...
```

## Uso

Una vez que la aplicación esté en funcionamiento, puedes acceder a las siguientes rutas:

*   **Página de Administración:** `http://localhost:3000/admin`
*   **Página de Estudiante:** `http://localhost:3000/estudiante`

La página de inicio (`/`) redirige a la página de administración.
