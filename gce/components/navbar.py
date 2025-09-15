# components/navbar.py - Versión actualizada
import reflex as rx
from ..state import State

def navbar():
    return rx.box(
        rx.hstack(
            rx.link(
                rx.heading("Sistema de Cursos", size="6", color="white"),
                href="/",
                underline="none",
                _hover={}
            ),
            rx.spacer(),
            rx.hstack(
                # Solo mostrar links según el rol actual
                rx.cond(
                    State.rol_actual == "administrador",
                    rx.link(
                        "Panel Admin",
                        href="/admin",
                        color="white",
                        padding="0.5rem 1rem",
                        border_radius="md",
                        _hover={"bg": "white", "color": "blue.600"}
                    )
                ),
                rx.cond(
                    State.rol_actual == "estudiante",
                    rx.link(
                        "Mis Cursos",
                        href="/estudiante",
                        color="white",
                        padding="0.5rem 1rem",
                        border_radius="md",
                        _hover={"bg": "white", "color": "blue.600"}
                    )
                ),
                # Menú de usuario (igual que antes)
                rx.menu.root(
                    rx.menu.trigger(
                        rx.button(
                            rx.hstack(
                                rx.cond(
                                    State.rol_actual == "administrador",
                                    rx.icon("shield", color="white"),
                                    rx.icon("user", color="white")
                                ),
                                rx.text(
                                    rx.cond(
                                        State.rol_actual == "administrador",
                                        "Admin",
                                        State.estudiante_actual.nombre
                                    ),
                                    color="white"
                                ),
                                rx.icon("chevron_down", color="white"),
                                align="center",
                                spacing="2"
                            ),
                            variant="ghost",
                            bg="blue.600",
                            _hover={"bg": "blue.700"}
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
                spacing="4",
                align="center"
            ),
            width="100%",
            padding="1rem"
        ),
        bg="blue.600",
        width="100%",
        box_shadow="0 2px 4px rgba(0,0,0,0.1)"
    )