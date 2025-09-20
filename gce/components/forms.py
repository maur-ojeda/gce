import reflex as rx
from gce.state.admin import AdminState
from gce.state.base import BaseState # Add this import

def FormularioCurso(profesor_nombres: list[str]): # Add the prop here
    return rx.form(
        rx.vstack(
            rx.input(
                placeholder="Nombre del Curso *",
                name="nombre",
                required=True,
                value=AdminState.nombre,
                on_change=AdminState.set_nombre,
            ),
            rx.select(
                BaseState.profesor_nombres, # Use the prop here
                placeholder="Seleccionar Profesor Principal *",
                name="profesor_id",
                required=True,
                value=AdminState.profesor_id,
                on_change=AdminState.set_profesor_id,
            ),
            rx.select(
                BaseState.profesor_nombres, # Use the prop here
                placeholder="Seleccionar Profesor Suplente (Opcional)",
                name="profesor_suplente_id",
                value=AdminState.profesor_suplente_id,
                on_change=AdminState.set_profesor_suplente_id,
            ),
            rx.input(
                placeholder="Aplicable para (Ej. 1er Medio) *",
                name="aplicable",
                required=True,
                value=AdminState.aplicable,
                on_change=AdminState.set_aplicable,
            ),
            rx.input(
                placeholder="Horario (Ej. Lunes 15:00-16:30) *",
                name="horario",
                required=True,
                value=AdminState.horario,
                on_change=AdminState.set_horario,
            ),
            rx.input(
                placeholder="Cupos Totales *",
                name="cupos_totales",
                type="number",
                required=True,
                min="1",
                value=AdminState.cupos_totales.to_string(),
                on_change=AdminState.set_cupos_totales,
            ),
            rx.text_area(
                placeholder="Descripción del Curso *",
                name="descripcion",
                required=True,
                rows="4",
                value=AdminState.descripcion,
                on_change=AdminState.set_descripcion,
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