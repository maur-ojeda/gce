import reflex as rx

# --- Modelos de Datos (simulados) ---
# Usamos un State de Reflex para simular una base de datos sencilla.

class Profesor(rx.Base):
    id: int
    nombre: str

class Estudiante(rx.Base):
    id: int
    nombre: str
    nivel: str
    cursos_inscritos: list[int] = []

class Curso(rx.Base):
    id: int
    nombre: str
    profesor_id: int
    cupos_totales: int
    descripcion: str
    nivel_aplicable: str
    horario: str
    estudiantes_inscritos: list[int] = []

class State(rx.State):
    # Simulamos una base de datos con listas.
    cursos: list[Curso] = [
        Curso(id=1, nombre="Introducción a la Programación", profesor_id=1, cupos_totales=20, descripcion="Aprende los fundamentos de la programación.", nivel_aplicable="1er Medio", horario="Lunes 15:00-16:30"),
        Curso(id=2, nombre="Historia del Arte Moderno", profesor_id=2, cupos_totales=15, descripcion="Un recorrido por los movimientos artísticos del siglo XX.", nivel_aplicable="2do Medio", horario="Martes 10:00-11:30"),
        Curso(id=3, nombre="Robótica y Automatización", profesor_id=1, cupos_totales=10, descripcion="Construye y programa robots básicos.", nivel_aplicable="3ro Medio", horario="Miércoles 14:00-15:30")
    ]

    profesores: list[Profesor] = [
        Profesor(id=1, nombre="Ana López"),
        Profesor(id=2, nombre="Carlos Pérez"),
    ]
    
    estudiantes: list[Estudiante] = [
        Estudiante(id=1, nombre="Juan Pérez", nivel="2do Medio"),
        Estudiante(id=2, nombre="María González", nivel="1er Medio"),
    ]

    # Estado de la interfaz de administración
    curso_seleccionado: int = -1
    show_form_modal: bool = False
    
    # Usuario actual
    usuario_actual_id: int = 1
    rol_actual: str = "estudiante" # O "administrador"
    
    def get_estudiante_actual(self) -> Estudiante:
        """Obtiene el objeto estudiante actual."""
        for est in self.estudiantes:
            if est.id == self.usuario_actual_id:
                return est
        return Estudiante(id=0, nombre="Invitado", nivel="")

    # --- Lógica de la aplicación para el Administrador ---
    def get_nombre_profesor(self, profesor_id: int) -> str:
        """Busca el nombre de un profesor por su ID."""
        for prof in self.profesores:
            if prof.id == profesor_id:
                return prof.nombre
        return "Desconocido"
    
    def crear_curso(self, form_data: dict):
        """Maneja la creación de un nuevo curso desde el formulario."""
        nuevo_id = max([c.id for c in self.cursos]) + 1 if self.cursos else 1
        nuevo_curso = Curso(
            id=nuevo_id,
            nombre=form_data["nombre"],
            profesor_id=int(form_data["profesor"]),
            cupos_totales=int(form_data["cupos"]),
            descripcion=form_data["descripcion"],
            nivel_aplicable=form_data["nivel"],
            horario=form_data["horario"]
        )
        self.cursos.append(nuevo_curso)
        self.show_form_modal = False

    def editar_curso(self, form_data: dict):
        """Maneja la edición de un curso existente."""
        for curso in self.cursos:
            if curso.id == self.curso_seleccionado:
                curso.nombre = form_data["nombre"]
                curso.profesor_id = int(form_data["profesor"])
                curso.cupos_totales = int(form_data["cupos"])
                curso.descripcion = form_data["descripcion"]
                curso.nivel_aplicable = form_data["nivel"]
                curso.horario = form_data["horario"]
                break
        self.curso_seleccionado = -1
        self.show_form_modal = False
        
    def eliminar_curso(self, curso_id: int):
        """Elimina un curso de la lista."""
        # Se podría agregar una confirmación aquí.
        self.cursos = [c for c in self.cursos if c.id != curso_id]

    def seleccionar_curso_para_editar(self, curso_id: int):
        """Prepara el formulario para editar un curso."""
        self.curso_seleccionado = curso_id
        self.show_form_modal = True

    def toggle_form_modal(self):
        """Muestra/oculta el modal del formulario."""
        if not self.show_form_modal:
            self.curso_seleccionado = -1  # Resetear para "Crear"
        self.show_form_modal = not self.show_form_modal
    
    # --- Lógica de la aplicación para el Estudiante ---
    def inscribir_curso(self, curso_id: int):
        """Inscribe al estudiante en un curso si hay cupos disponibles."""
        estudiante = self.get_estudiante_actual()

        for curso in self.cursos:
            if curso.id == curso_id:
                # Validar nivel
                if curso.nivel_aplicable != estudiante.nivel:
                    return rx.window_alert(f"Este curso es solo para {curso.nivel_aplicable}.")
                    
                # Validar cupos
                if len(curso.estudiantes_inscritos) >= curso.cupos_totales:
                    return rx.window_alert("No hay cupos disponibles para este curso.")
                
                # Validar no duplicidad
                if estudiante.id in curso.estudiantes_inscritos:
                    return rx.window_alert("Ya estás inscrito en este curso.")
                
                # Inscribir
                curso.estudiantes_inscritos.append(estudiante.id)
                estudiante.cursos_inscritos.append(curso.id)
                
                return rx.window_alert(f"¡Te has inscrito en {curso.nombre}!")
        return rx.window_alert("Curso no encontrado.")
    
    def get_cursos_disponibles(self) -> list[Curso]:
        """Obtiene los cursos disponibles para el estudiante actual."""
        estudiante = self.get_estudiante_actual()
        return [c for c in self.cursos if c.nivel_aplicable == estudiante.nivel and len(c.estudiantes_inscritos) < c.cupos_totales]

# --- Vistas (Frontend) ---

# Componente para el formulario de crear/editar curso
def formulario_curso():
    """Formulario para crear o editar un curso."""
    curso_a_editar = rx.State.cursos.find(lambda c: c.id == rx.State.curso_seleccionado)
    
    return rx.form(
        rx.vstack(
            rx.heading("Crear/Editar Curso", size="lg", margin_bottom="1em"),
            rx.input(
                placeholder="Nombre del Curso",
                name="nombre",
                default_value=curso_a_editar.nombre if curso_a_editar else ""
            ),
            rx.select(
                State.profesores.map(lambda prof: rx.option(prof.nombre, value=str(prof.id))),
                placeholder="Seleccionar Profesor",
                name="profesor",
                default_value=str(curso_a_editar.profesor_id) if curso_a_editar else ""
            ),
            rx.input(
                placeholder="Nivel Aplicable",
                name="nivel",
                default_value=curso_a_editar.nivel_aplicable if curso_a_editar else ""
            ),
            rx.input(
                placeholder="Horario (Ej. Lunes 15:00-16:30)",
                name="horario",
                default_value=curso_a_editar.horario if curso_a_editar else ""
            ),
            rx.input(
                placeholder="Cupos Totales",
                name="cupos",
                type="number",
                default_value=str(curso_a_editar.cupos_totales) if curso_a_editar else ""
            ),
            rx.text_area(
                placeholder="Descripción del Curso",
                name="descripcion",
                default_value=curso_a_editar.descripcion if curso_a_editar else ""
            ),
            rx.button(
                "Guardar Curso",
                width="100%",
                type="submit",
                color_scheme="blue"
            ),
            spacing="1em"
        ),
        on_submit=State.editar_curso if rx.State.curso_seleccionado != -1 else State.crear_curso
    )


def vista_curso_estudiante(curso: Curso):
    """Componente para mostrar la tarjeta de un curso para el estudiante."""
    cupos_disponibles = curso.cupos_totales - len(curso.estudiantes_inscritos)
    
    return rx.box(
        rx.vstack(
            rx.heading(curso.nombre, size="lg"),
            rx.text(f"Profesor: {State.get_nombre_profesor(curso.profesor_id)}", color="gray"),
            rx.text(curso.descripcion),
            rx.spacer(),
            rx.hstack(
                rx.text(f"Cupos disponibles: {cupos_disponibles}/{curso.cupos_totales}"),
                rx.button(
                    "Inscribirse",
                    on_click=State.inscribir_curso(curso.id),
                    is_disabled=cupos_disponibles <= 0 or curso.id in State.get_estudiante_actual().cursos_inscritos,
                    color_scheme="blue",
                ),
                justify="between",
                width="100%",
            ),
            align_items="start",
            spacing="1em"
        ),
        border_radius="15px",
        border="1px solid #E0E0E0",
        padding="1.5em",
        box_shadow="0px 4px 15px rgba(0, 0, 0, 0.1)",
        bg="white"
    )

# --- Vista de Estudiante ---
def vista_estudiante():
    """Interfaz para que el estudiante gestione sus inscripciones."""
    estudiante = State.get_estudiante_actual()
    return rx.vstack(
        rx.center(
            rx.heading("Catálogo de Cursos", color="white", font_size="2em"),
        ),
        bg="#0066cc",
        padding="20px",
        width="100%",
        rx.container(
            rx.heading(f"¡Hola, {estudiante.nombre}!", margin_top="20px"),
            rx.text(f"Nivel: {estudiante.nivel}"),
            rx.text("Explora los cursos disponibles e inscríbete."),
            rx.divider(),
            rx.grid(
                rx.foreach(State.get_cursos_disponibles, vista_curso_estudiante),
                columns="1fr",
                spacing="2em",
                width="100%",
                margin_top="20px"
            ),
            max_width="800px",
            padding="2em",
        ),
        width="100%",
        min_height="100vh",
        bg="#F5F5F5",
    )


# --- Vista del Administrador ---
def vista_administrador():
    """Interfaz para que el administrador gestione los cursos."""
    return rx.vstack(
        rx.center(
            rx.heading("Panel de Administración de Cursos", color="white", font_size="2em"),
        ),
        
        rx.container(
            rx.hstack(
                rx.heading("Cursos Existentes", size="lg"),
                rx.spacer(),
                rx.button(
                    "Crear Nuevo Curso",
                    on_click=State.toggle_form_modal,
                    color_scheme="green"
                ),
                width="100%",
                margin_top="20px"
            ),
            rx.divider(),
            rx.box(
                rx.table_container(
                    rx.table(
                        rx.thead(
                            rx.tr(
                                rx.th("ID"),
                                rx.th("Nombre"),
                                rx.th("Profesor"),
                                rx.th("Cupos"),
                                rx.th("Inscritos"),
                                rx.th("Acciones")
                            )
                        ),
                        rx.tbody(
                            rx.foreach(
                                State.cursos,
                                lambda curso: rx.tr(
                                    rx.td(curso.id),
                                    rx.td(curso.nombre),
                                    rx.td(State.get_nombre_profesor(curso.profesor_id)),
                                    rx.td(f"{curso.cupos_totales}"),
                                    rx.td(f"{len(curso.estudiantes_inscritos)}"),
                                    rx.td(
                                        rx.hstack(
                                            rx.button("✏️", on_click=State.seleccionar_curso_para_editar(curso.id)),
                                            rx.button("🗑️", on_click=State.eliminar_curso(curso.id), color_scheme="red"),
                                            spacing="1em"
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                margin_top="1em"
            ),
            # Modal del formulario
            rx.modal(
                rx.modal_overlay(
                    rx.modal_content(
                        rx.modal_body(
                            formulario_curso()
                        )
                    )
                ),
                is_open=State.show_form_modal,
                on_close=State.toggle_form_modal
            ),
            max_width="1000px",
            padding="2em",
            width="100%"
        ),
        bg="#0066cc",
        padding="20px",
        width="100%",
    )
    
# --- Configuración de la App ---
def index():
    return rx.cond(
        State.rol_actual == "administrador",
        vista_administrador(),
        vista_estudiante()
    )

app = rx.App()
app.add_page(index, "/")