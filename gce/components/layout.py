import reflex as rx
from .navbar import navbar
def PageShell(*children, bg="#0066cc", **kw) -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(*children, width="100%", padding="20px"),
        bg=bg,
        width="100%",
        min_h="100vh",
        **kw
    )