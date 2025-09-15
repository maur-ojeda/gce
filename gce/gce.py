import reflex as rx

from rxconfig import config

from .state import State

from .pages.admin import vista_administrador
from .pages.student import vista_estudiante
from .components.navbar import navbar

def index() -> rx.Component:

    return rx.container(
         rx.cond(
             State.rol_actual == "administrador", 
             vista_administrador(), 
             vista_estudiante(),
        )
    )

def admin_page():
    return rx.cond(
        State.rol_actual == "administrador",
        vista_administrador(),
        rx.fragment(on_mount=rx.redirect("/"))

    )

def estudiante_page():
    return rx.cond(
        State.rol_actual == "estudiante",
        vista_estudiante(),
        rx.fragment(on_mount=rx.redirect("/"))
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
app.add_page(index)
app.add_page(index, route="/")
app.add_page(admin_page, route="/admin")
app.add_page(estudiante_page, route="/estudiante")
