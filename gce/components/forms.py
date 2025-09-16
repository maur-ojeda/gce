import reflex as rx
from ..state import AdminState
from ..models import Curso


def FormularioCurso():
    
    return rx.model_form(
        Curso,
        # mostrar solo estos camados
        ["nombre", "profesor_id", "aplicable", "horario", "cupos_totales", "descripcion"],
        # submit único
        on_submit=AdminState.guardar,
        # mapeo personalizado
        field_mapping={
            "profesor_id": lambda: rx.select(
                [(str(p.id), p.nombre) for p in AdminState.profesores],
                placeholder="Seleccionar profesor"
            )
        }
    )
        