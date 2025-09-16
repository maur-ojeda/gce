import reflex as rx
from ..state import AdminState




def FormularioCurso():
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Nombre del Curso *",
                name="nombre",
                required=True
            ),
            rx.select(
                ["Ana López", "Carlos Pérez"],
                placeholder="Seleccionar Profesor *",
                name="profesor_id",
                required=True
            ),
            rx.input(
                placeholder="Aplicable para (Ej. 1er Medio) *",
                name="aplicable",
                required=True
            ),
            rx.input(
                placeholder="Horario (Ej. Lunes 15:00-16:30) *",
                name="horario",
                required=True
            ),
            rx.input(
                placeholder="Cupos Totales *",
                name="cupos_totales",
                type="number",
                required=True,
                min="1"
            ),
            rx.text_area(
                placeholder="Descripción del Curso *",
                name="descripcion",
                required=True,
                rows="4"
            ),
            rx.button(
                rx.cond(
                    AdminState.curso_editando != -1,
                    "Actualizar Curso",
                    "Crear Curso"
                ),
                width="100%",
                type="submit",
                color_scheme="blue",
                margin_top="1em"
            ),
            spacing="1",
            width="100%"
        ),
        on_submit=AdminState.guardar
    )