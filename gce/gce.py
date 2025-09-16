import reflex as rx
from .state import State
from .pages.admin import vista_administrador
from .pages.student import vista_estudiante

def index() -> rx.Component:
    return rx.cond(
        State.rol_actual == "administrador",
        vista_administrador(),
        vista_estudiante()
    )

def admin_page() -> rx.Component:
    return rx.cond(
        State.rol_actual == "administrador",
        vista_administrador(),
        rx.fragment()  # Componente vacío en lugar de redirect
    )

def student_page() -> rx.Component:
    return rx.cond(
        State.rol_actual == "estudiante",
        vista_estudiante(),
        rx.fragment()  # Componente vacío en lugar de redirect
    )

app = rx.App(
    theme=rx.theme(
        accent_color="mint",
        gray_color="gray",
        panel_background="solid",
        scaling="100%",
        radius="full"
    )
)

# Rutas corregidas (sin duplicados)
app.add_page(index, route="/")           # Página principal
app.add_page(admin_page, route="/admin") # Ruta admin
app.add_page(student_page, route="/estudiante") # Ruta estudiante

