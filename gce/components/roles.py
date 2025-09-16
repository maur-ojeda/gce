# gce/components/roles.py
import reflex as rx
from gce.state import BaseState as State   # alias local

def admin_only(page_func):
    """Wrapper de página: sólo admin."""
    def _wrapped():
        return rx.cond(
            State.rol_actual == "administrador",
            page_func(),
            rx.redirect("/")
        )
    return _wrapped

def student_only(page_func):
    """Wrapper de página: sólo estudiante."""
    def _wrapped():
        return rx.cond(
            State.rol_actual == "estudiante",
            page_func(),
            rx.redirect("/")
        )
    return _wrapped