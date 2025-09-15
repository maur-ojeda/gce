import reflex as rx
from .models import Profesor, Estudiante, Curso

class State(rx.State):
    # Usuario actual
    usuario_actual_id: int = 1
    rol_actual: str = "administrador"  # Puedes cambiar a "estudiante"
    
    # Estado de la interfaz de administración
    curso_seleccionado: int = -1
    show_form_modal: bool = False
    
    # Estado de la interfaz de estudiante
    curso_detalle_id: int = -1
    show_detalle_modal: bool = False
    mensaje_error: str = ""
    mensaje_exito: str = ""
    
    def toggle_form_modal(self):
        """Muestra/oculta el modal del formulario."""
        self.show_form_modal = not self.show_form_modal
        if not self.show_form_modal:
            self.curso_seleccionado = -1

    def toggle_detalle_modal(self):
        """Muestra/oculta el modal de detalles."""
        self.show_detalle_modal = not self.show_detalle_modal
        if not self.show_detalle_modal:
            self.curso_detalle_id = -1
            self.mensaje_error = ""
            self.mensaje_exito = ""

    # Datos simulados
    cursos: list[Curso] = [
        Curso(id=1, nombre="Introducción a la Programación", profesor_id=1, cupos_totales=20, descripcion="Aprende los fundamentos de la programación.", aplicable="1er Medio", horario="Lunes 15:00-16:30", estudiantes_inscritos=[]),
        Curso(id=2, nombre="Historia del Arte Moderno", profesor_id=2, cupos_totales=15, descripcion="Un recorrido por los movimientos artísticos del siglo XX.", aplicable="2do Medio", horario="Martes 10:00-11:30", estudiantes_inscritos=[]),
        Curso(id=3, nombre="Robótica y Automatización", profesor_id=1, cupos_totales=10, descripcion="Construye y programa robots básicos.", aplicable="3ro Medio", horario="Miércoles 14:00-15:30", estudiantes_inscritos=[])
    ]

    profesores: list[Profesor] = [
        Profesor(id=1, nombre="Ana López"),
        Profesor(id=2, nombre="Carlos Pérez"),
    ]

    estudiantes: list[Estudiante] = [
        Estudiante(id=1, nombre="Juan Pérez", nivel="1er Medio", cursos_inscritos=[]),
        Estudiante(id=2, nombre="María González", nivel="2do Medio", cursos_inscritos=[1]),
    ]

    # Métodos de ayuda
    def get_nombre_profesor(self, profesor_id: int) -> str:
        """Busca el nombre de un profesor por su ID."""
        for prof in self.profesores:
            if prof.id == profesor_id:
                return prof.nombre
        return "Desconocido"
    
    
    @rx.var
    def estudiante_actual(self) -> Estudiante:
        """Obtiene el objeto estudiante actual."""
        for est in self.estudiantes:
            if est.id == self.usuario_actual_id:
                return est
        return Estudiante(id=0, nombre="Invitado", nivel="", cursos_inscritos=[])

    @rx.var
    def profesor_map(self) -> dict[int, str]:
        """Devuelve un mapa de ID de profesor a nombre."""
        return {prof.id: prof.nombre for prof in self.profesores}

    @rx.var
    def cursos_con_profesores(self) -> list[dict]:
        """Devuelve una lista de cursos con el nombre del profesor incluido."""
        profesor_map = self.profesor_map
        return [
            {
                "id": curso.id,
                "nombre": curso.nombre,
                "profesor_nombre": profesor_map.get(curso.profesor_id, "Desconocido"),
                "profesor_id": curso.profesor_id,
                "cupos_totales": curso.cupos_totales,
                "descripcion": curso.descripcion,
                "aplicable": curso.aplicable,
                "horario": curso.horario,
                "inscritos_count": len(curso.estudiantes_inscritos)
            }
            for curso in self.cursos
        ]
    

    @rx.var
    def cursos_disponibles(self) -> list[dict]:
        """Obtiene los cursos disponibles para el estudiante actual."""
        estudiante = self.estudiante_actual
        profesor_map = self.profesor_map
        return [
            {
                "id": curso.id,
                "nombre": curso.nombre,
                "profesor_nombre": profesor_map.get(curso.profesor_id, "Desconocido"),
                "profesor_id": curso.profesor_id,
                "cupos_totales": curso.cupos_totales,
                "descripcion": curso.descripcion,
                "aplicable": curso.aplicable,
                "horario": curso.horario,
                "inscritos_count": len(curso.estudiantes_inscritos),
                "cupos_disponibles": curso.cupos_totales - len(curso.estudiantes_inscritos)
            }
            for curso in self.cursos
            if curso.aplicable == estudiante.nivel 
            and len(curso.estudiantes_inscritos) < curso.cupos_totales
            and curso.id not in estudiante.cursos_inscritos
        ]

    @rx.var
    def cursos_inscritos(self) -> list[dict]:
        """Obtiene los cursos en los que está inscrito el estudiante actual."""
        estudiante = self.estudiante_actual
        profesor_map = self.profesor_map
        return [
            {
                "id": curso.id,
                "nombre": curso.nombre,
                "profesor_nombre": profesor_map.get(curso.profesor_id, "Desconocido"),
                "profesor_id": curso.profesor_id,
                "cupos_totales": curso.cupos_totales,
                "descripcion": curso.descripcion,
                "aplicable": curso.aplicable,
                "horario": curso.horario,
                "inscritos_count": len(curso.estudiantes_inscritos)
            }
            for curso in self.cursos
            if curso.id in estudiante.cursos_inscritos
        ]

    # Métodos para administrador
    
    @rx.var
    def profesor_select_items(self) -> list[dict]:
        """Items para el select de profesores."""
        return [
            {"label": prof.nombre, "value": str(prof.id)} 
            for prof in self.profesores
        ]

    def crear_curso(self, form_data: dict):
        """Crea un nuevo curso."""
        nuevo_id = max([c.id for c in self.cursos], default=0) + 1
        nuevo_curso = Curso(
            id=nuevo_id,
            nombre=form_data.get("nombre", ""),
            profesor_id=int(form_data.get("profesor_id", 1)),
            cupos_totales=int(form_data.get("cupos_totales", 10)),
            descripcion=form_data.get("descripcion", ""),
            aplicable=form_data.get("aplicable", ""),
            horario=form_data.get("horario", ""),
            estudiantes_inscritos=[]
        )
        self.cursos.append(nuevo_curso)

    def editar_curso(self, form_data: dict):
        """Edita un curso existente."""
        for curso in self.cursos:
            if curso.id == self.curso_seleccionado:
                curso.nombre = form_data.get("nombre", curso.nombre)
                curso.profesor_id = int(form_data.get("profesor_id", curso.profesor_id))
                curso.cupos_totales = int(form_data.get("cupos_totales", curso.cupos_totales))
                curso.descripcion = form_data.get("descripcion", curso.descripcion)
                curso.aplicable = form_data.get("aplicable", curso.aplicable)
                curso.horario = form_data.get("horario", curso.horario)
                break

    def handle_crear_curso(self, form_data: dict):
        """Handler para crear curso."""
        self.crear_curso(form_data)
        self.show_form_modal = False

    def handle_editar_curso(self, form_data: dict):
        """Handler para editar curso."""
        self.editar_curso(form_data)
        self.show_form_modal = False
        self.curso_seleccionado = -1
    
    def eliminar_curso(self, curso_id: int):
        """Elimina un curso de la lista."""
        # Eliminar inscripciones relacionadas
        for estudiante in self.estudiantes:
            if curso_id in estudiante.cursos_inscritos:
                estudiante.cursos_inscritos.remove(curso_id)
        
        # Eliminar el curso
        self.cursos = [c for c in self.cursos if c.id != curso_id]

    def seleccionar_curso_para_editar(self, curso_id: int):
        """Prepara el formulario para editar un curso."""
        self.curso_seleccionado = curso_id
        self.show_form_modal = True

    # Métodos para estudiante
    def mostrar_detalle_curso(self, curso_id: int):
        """Muestra el modal con detalles del curso."""
        self.curso_detalle_id = curso_id
        self.show_detalle_modal = True
        self.mensaje_error = ""
        self.mensaje_exito = ""

    def inscribir_curso(self, curso_id: int):
        """Inscribe al estudiante en un curso si hay cupos disponibles."""
        self.mensaje_error = ""
        self.mensaje_exito = ""
        
        estudiante = self.estudiante_actual
        
        # Buscar el curso
        curso = next((c for c in self.cursos if c.id == curso_id), None)
        if not curso:
            self.mensaje_error = "Curso no encontrado."
            return

        # Validar nivel
        if curso.aplicable != estudiante.nivel:
            self.mensaje_error = f"Este curso es solo para {curso.aplicable}."
            return
            
        # Validar cupos
        if len(curso.estudiantes_inscritos) >= curso.cupos_totales:
            self.mensaje_error = "No hay cupos disponibles para este curso."
            return
        
        # Validar no duplicidad
        if estudiante.id in curso.estudiantes_inscritos:
            self.mensaje_error = "Ya estás inscrito en este curso."
            return
        
        # Inscribir
        curso.estudiantes_inscritos.append(estudiante.id)
        estudiante.cursos_inscritos.append(curso.id)
        
        self.mensaje_exito = f"¡Te has inscrito en {curso.nombre}!"
        
        # Cerrar modal
        self.show_detalle_modal = False
        self.curso_detalle_id = -1

    def handle_submit(self, form_data: dict):
        """Handler único para manejar submit de formularios."""
        if self.curso_seleccionado != -1:
            self.editar_curso(form_data)
        else:
            self.crear_curso(form_data)
        self.show_form_modal = False


# Agrega estos métodos a tu State en state.py

    def cambiar_rol(self, nuevo_rol: str):
        """Cambia el rol del usuario actual."""
        self.rol_actual = nuevo_rol
        # Resetear estados de UI
        self.show_form_modal = False
        self.show_detalle_modal = False
        self.curso_seleccionado = -1
        self.curso_detalle_id = -1

    def logout(self):
        """Cierra sesión y vuelve al rol por defecto."""
        self.rol_actual = "estudiante"  # o "invitado"
        self.usuario_actual_id = 1        


    @rx.var
    def puede_ver_admin(self) -> bool:
        """Verifica si el usuario puede ver la vista de admin."""
        return self.rol_actual == "administrador"

    @rx.var
    def puede_ver_estudiante(self) -> bool:
        """Verifica si el usuario puede ver la vista de estudiante."""
        return self.rol_actual == "estudiante"

    def ir_a_admin(self):
        """Navega a la vista de administrador."""
        if self.rol_actual == "administrador":
            return rx.redirect("/admin")
        return rx.window_alert("No tienes permisos de administrador")

    def ir_a_estudiante(self):
        """Navega a la vista de estudiante."""
        if self.rol_actual == "estudiante":
            return rx.redirect("/estudiante")
        return rx.window_alert("No tienes permisos de estudiante")

    # En state.py
    def check_admin_access(self):
        """Verifica acceso de admin y redirige si no tiene permisos."""
        if self.rol_actual != "administrador":
            return rx.redirect("/")
        return None

    def check_student_access(self):
        """Verifica acceso de estudiante y redirige si no tiene permisos."""
        if self.rol_actual != "estudiante":
            return rx.redirect("/")
        return None

