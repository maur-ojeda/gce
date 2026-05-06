<p align="center">
  <h1 align="center">Gestor de Cursos Escolares (GCE)</h1>
  <p align="center">
    <em>School Course Management System — Built with Reflex &amp; SQLModel</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Reflex-0.8.10-6E40C9?style=for-the-badge&logo=reflex&logoColor=white" alt="Reflex" />
  <img src="https://img.shields.io/badge/SQLModel-0.0.x-9B4DCA?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLModel" />
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

---

## Características

La aplicación cuenta con dos roles de usuario principales: **Administrador** y **Estudiante**.

### Administrador

- **Gestión de Cursos:** Crear, leer, actualizar y eliminar cursos.
- Ver una lista de todos los cursos con su información detallada.
- Asignar profesores a los cursos (principal y suplente).
- Establecer el número de cupos para cada curso.

### Estudiante

- **Inscripción a Cursos:** Ver cursos inscritos y disponibles.
- Inscribirse y darse de baja de los cursos.
- Ver los detalles de cada curso, incluyendo el profesor, el horario y la descripción.
- Validación de conflictos de horario y límite de cursos.

### Registro

- Registro de nuevos estudiantes con validación de email y contraseña.

---

## Arquitectura

GCE sigue el patrón **Reflex State** — una arquitectura unidireccional donde la UI se renderiza declarativamente y los cambios de estado disparan re-renderizados automáticos.

```mermaid
graph TD
    A[Pages] -->|eventos| B[State]
    B -->|vars reactivas| A
    B -->|consultas| C[Models]
    C -->|SQLModel ORM| D[(SQLite DB)]
    D -->|datos| C
    C -->|objetos| B

    subgraph Pages
        A1[login.py]
        A2[register.py]
        A3[admin.py]
        A4[student.py]
    end

    subgraph State
        B1[BaseState]
        B2[UIState]
        B3[AdminState]
        B4[StudentState]
        B5[RegisterState]
    end

    subgraph Models
        C1[Profesor]
        C2[Estudiante]
        C3[Curso]
        C4[AuditLog]
    end
```

### Jerarquía de State

| State | Hereda de | Responsabilidad |
|-------|-----------|-----------------|
| `BaseState` | `rx.State` | Datos compartidos, autenticación, helpers |
| `UIState` | `BaseState` | Modales y flags de UI |
| `AdminState` | `UIState` | CRUD de cursos, estudiantes y profesores |
| `StudentState` | `UIState` | Inscripción, baja, validaciones de horario |
| `RegisterState` | `UIState` | Registro de nuevos estudiantes |

---

## Tech Stack

| Tecnología | Propósito |
|-----------|-----------|
| ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) | Lenguaje principal |
| ![Reflex](https://img.shields.io/badge/Reflex-6E40C9?logo=reflex&logoColor=white) | Framework web fullstack |
| ![SQLModel](https://img.shields.io/badge/SQLModel-9B4DCA?logo=sqlalchemy&logoColor=white) | ORM / modelos de datos |
| ![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white) | Base de datos embebida |
| ![TailwindCSS](https://img.shields.io/badge/Tailwind-06B6D4?logo=tailwindcss&logoColor=white) | Estilos (via Reflex plugin) |
| ![Bcrypt](https://img.shields.io/badge/Bcrypt-4.0-000000?logo=libreoffice&logoColor=white) | Hash de contraseñas |

---

## Instalación y Configuración

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### Prerrequisitos

- Python 3.8 o superior
- pip

### Pasos de Instalación

1. **Clona el repositorio:**

   ```bash
   git clone https://github.com/maur-ojeda/gce.git
   cd gce
   ```

2. **Crea un entorno virtual:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   *En Windows, usa `.venv\Scripts\activate`*

3. **Instala las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Inicializa y ejecuta la aplicación:**

   ```bash
   reflex init
   reflex run
   ```

La aplicación estará disponible en `http://localhost:3000`.

---

## Estructura del Proyecto

```
/
├── gce/
│   ├── __init__.py
│   ├── gce.py                # Punto de entrada de la aplicación
│   ├── models.py             # Modelos de datos (SQLModel)
│   ├── database.py           # Configuración de BD y seed data
│   ├── components/           # Componentes reutilizables de UI
│   │   ├── cards.py          # Tarjetas de cursos
│   │   ├── forms.py          # Formularios
│   │   ├── layout.py         # Layout con navbar
│   │   └── navbar.py         # Barra de navegación
│   ├── pages/                # Páginas/rutas de la aplicación
│   │   ├── admin.py          # Vista del administrador
│   │   ├── student.py        # Vista del estudiante
│   │   ├── login.py          # Login por rol
│   │   └── register.py       # Registro de estudiantes
│   └── state/                # Estado reactivo (Reflex State)
│       ├── base.py           # BaseState — datos compartidos
│       ├── ui.py             # UIState — modales y flags
│       ├── admin.py          # AdminState — CRUD
│       ├── student.py        # StudentState — inscripción
│       └── register.py       # RegisterState — registro
├── requirements.txt          # Dependencias de Python
├── rxconfig.py               # Configuración de Reflex
└── LICENSE                    # MIT License
```

---

## Uso

Una vez que la aplicación esté en funcionamiento, puedes acceder a las siguientes rutas:

| Ruta | Descripción |
|------|-------------|
| `/` | Página de inicio (redirige a login) |
| `/login` | Selección de rol |
| `/register` | Registro de nuevo estudiante |
| `/admin` | Panel de administración |
| `/estudiante` | Vista del estudiante |

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.