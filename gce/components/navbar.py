# components/navbar.py
import reflex as rx
from ..state import State

def navbar():
    """Barra de navegación con cambio de roles."""
    return rx.box(
        rx.hstack(
            rx.heading("Sistema de Cursos", size="6"),
            rx.spacer(),
            rx.hstack(
                rx.cond(
                    State.rol_actual == "administrador",
                    rx.button(
                        "Vista Estudiante",
                        on_click=lambda: State.cambiar_rol("estudiante"),
                        color_scheme="blue"
                    ),
                    rx.button(
                        "Vista Administrador",
                        on_click=lambda: State.cambiar_rol("administrador"),
                        color_scheme="orange"
                    )
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.cond(
                                State.rol_actual == "administrador",
                                "👤 Admin",
                                "👤 Estudiante"
                            ),
                            rx.icon("chevron_down"),
                            variant="ghost"
                        )
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "Cambiar a Administrador",
                            on_click=lambda: State.cambiar_rol("administrador")
                        ),
                        rx.menu.item(
                            "Cambiar a Estudiante",
                            on_click=lambda: State.cambiar_rol("estudiante")
                        ),
                        rx.menu.separator(),
                        rx.menu.item(
                            "Cerrar Sesión",
                            on_click=State.logout,
                            color="red"
                        )
                    )
                ),
                spacing="4"
            ),
            width="100%",
            padding="1rem"
        ),
        bg="gray.100",
        width="100%"
    )