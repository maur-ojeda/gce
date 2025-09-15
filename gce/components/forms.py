import reflex as rx
from ..state import State

def formulario_curso():
    """Formulario para crear o editar un curso."""
    
    return rx.cond(
        State.curso_seleccionado != -1,
        # Formulario para editar
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Nombre del Curso",
                    name="nombre"
                ),
                rx.select(
                    ["Ana López", "Carlos Pérez"],
                    placeholder="Seleccionar Profesor",
                    name="profesor_id"
                ),
                rx.input(
                    placeholder="Aplicable para (Ej. 1er Medio)",
                    name="aplicable"
                ),
                rx.input(
                    placeholder="Horario (Ej. Lunes 15:00-16:30)",
                    name="horario"
                ),
                rx.input(
                    placeholder="Cupos Totales",
                    name="cupos_totales",
                    type="number"
                ),
                rx.text_area(
                    placeholder="Descripción del Curso",
                    name="descripcion"
                ),
                rx.button(
                    "Actualizar Curso",
                    width="100%",
                    type="submit",
                    color_scheme="blue"
                ),
                spacing="2",
                width="100%"
            ),
            on_submit=State.editar_curso
        ),
        # Formulario para crear
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="Nombre del Curso",
                    name="nombre"
                ),
                rx.select(
                    ["Ana López", "Carlos Pérez"],
                    placeholder="Seleccionar Profesor",
                    name="profesor_id"
                ),
                rx.input(
                    placeholder="Aplicable para (Ej. 1er Medio)",
                    name="aplicable"
                ),
                rx.input(
                    placeholder="Horario (Ej. Lunes 15:00-16:30)",
                    name="horario"
                ),
                rx.input(
                    placeholder="Cupos Totales",
                    name="cupos_totales",
                    type="number"
                ),
                rx.text_area(
                    placeholder="Descripción del Curso",
                    name="descripcion"
                ),

                rx.flex(

                     rx.dialog.close(
                        rx.button(
                            "Cerrar",
                            size="3",
                            color_scheme="gray",
                            width="50%",
                        ),
                    ),

                    rx.button(
                    "Crear Curso",                
                    type="submit",
                    color_scheme="green",
                    size="3",
                    width="50%",
                    ),
                    spacing="2",
                    width="100%",
                    padding_top="2"
                    ),
                margin_bottom="2",
                margin_top="2",          
                spacing="2",
                width="100%"
            ),
            on_submit=State.crear_curso
        )
    )