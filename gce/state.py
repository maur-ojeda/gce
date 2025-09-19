import reflex as rx
from .models import Curso, Profesor, Estudiante

# ---------- 1. BASE STATE (datos y helpers comunes) ----------
class BaseState(rx.State):
    usuario_actual_id: int = 1
    rol_actual: str = "administrador"

    # DATOS → siempre en BaseState
    cursos: list[Curso] = [
        Curso(id=1, nombre="Intro Programación", profesor_id=1, cupos_totales=20,
              descripcion="Fundamentos", aplicable="1er Medio", horario="Lunes 15:00-16:30",
              estudiantes_inscritos=[]),
        
    ]
    profesores: list[Profesor] = [
        Profesor(id=1, nombre="Ana López"),
        Profesor(id=2, nombre="Carlos Pérez"),
    ]
    estudiantes: list[Estudiante] = [
        Estudiante(id=1, nombre="Juan Pérez", nivel="1er Medio", cursos_inscritos=[]),
        Estudiante(id=2, nombre="María González", nivel="2do Medio", cursos_inscritos=[1]),
    ]

    # HELPERS / VARS
    @rx.var(cache=True)
    def profesor_map(self) -> dict[int, str]:
        return {p.id: p.nombre for p in self.profesores}

    @rx.var(cache=True)
    def estudiante_actual(self) -> Estudiante:
        return next(
            (e for e in self.estudiantes if e.id == self.usuario_actual_id),
            Estudiante(id=0, nombre="Invitado", nivel="", cursos_inscritos=[])
        )

    @rx.var(cache=True)
    def cursos_con_profesores(self) -> list[dict]:
        return [
            {
                **curso.dict(),
                "profesor_nombre": self.profesor_map.get(curso.profesor_id, "Desconocido"),
                "inscritos_count": len(curso.estudiantes_inscritos),
                "cupos_disponibles": curso.cupos_totales - len(curso.estudiantes_inscritos)
            }
            for curso in self.cursos
        ]

    # MÉTODOS COMUNES
    def logout(self):
        self.rol_actual = "estudiante"
        self.usuario_actual_id = 1

    def cambiar_rol(self, nuevo: str):
        self.rol_actual = nuevo
        self.logout()


# ---------- 2. ADMIN STATE (solo lógica de admin) ----------
class AdminState(BaseState):
    show_form_modal: bool = False
    curso_editando: int = -1

    def toggle_modal(self):
        self.show_form_modal = not self.show_form_modal
        if not self.show_form_modal:
            self.curso_editando = -1

    def editar(self, curso_id: int):
        self.curso_editando = curso_id
        self.toggle_modal()

    def guardar(self, form: dict):
        profesor_nombre = form.get("profesor_id")
        profesor_id = next(
            (p.id for p in self.profesores if p.nombre == profesor_nombre),
            1
        )
        if self.curso_editando == -1:  # CREAR
            nuevo_id = max((c.id for c in self.cursos), default=0) + 1
            self.cursos.append(Curso(
                id=nuevo_id,
                nombre=form["nombre"],
                profesor_id=profesor_id,
                cupos_totales=int(form["cupos_totales"]),
                descripcion=form["descripcion"],
                aplicable=form["aplicable"],
                horario=form["horario"],
                estudiantes_inscritos=[]
            ))
        else:  # EDITAR
            curso = next(c for c in self.cursos if c.id == self.curso_editando)
            curso.nombre = form["nombre"]
            curso.profesor_id = profesor_id
            curso.cupos_totales = int(form["cupos_totales"])
            curso.descripcion = form["descripcion"]
            curso.aplicable = form["aplicable"]
            curso.horario = form["horario"]
        self.toggle_modal()

    def eliminar(self, curso_id: int):
        for est in self.estudiantes:
            if curso_id in est.cursos_inscritos:
                est.cursos_inscritos.remove(curso_id)
        self.cursos = [c for c in self.cursos if c.id != curso_id]


# ---------- 3. STUDENT STATE (solo lógica de estudiante) ----------
class StudentState(BaseState):
    show_detalle_modal: bool = False
    detalle_curso_id: int = -1
    mensaje: str = ""

    def toggle_detalle(self):
        self.show_detalle_modal = not self.show_detalle_modal
        if not self.show_detalle_modal:
            self.detalle_curso_id = -1

    def mostrar_detalle(self, curso_id: int):
        self.detalle_curso_id = curso_id
        self.toggle_detalle()

    def _validar_inscripcion(self, curso: Curso) -> str | None:
        est = self.estudiante_actual
        if curso.aplicable != est.nivel:
            return f"Solo para {curso.aplicable}"
        if len(curso.estudiantes_inscritos) >= curso.cupos_totales:
            return "Sin cupos"
        if est.id in curso.estudiantes_inscritos:
            return "Ya inscrito"
        return None

    def inscribir(self, curso_id: int):
        curso = next((c for c in self.cursos if c.id == curso_id), None)
        if not curso:
            self.mensaje = "Curso no encontrado"
            return
        if err := self._validar_inscripcion(curso):
            self.mensaje = err
            return
        curso.estudiantes_inscritos.append(self.estudiante_actual.id)
        self.estudiante_actual.cursos_inscritos.append(curso_id)
        self.mensaje = f"¡Inscrito en {curso.nombre}!"
        self.toggle_detalle()

    @rx.var(cache=True)
    def cursos_disponibles(self) -> list[dict]:
        est = self.estudiante_actual
        return [
            c for c in self.cursos_con_profesores
            if c["aplicable"] == est.nivel
            and c["id"] not in est.cursos_inscritos
            and c["cupos_disponibles"] > 0
        ]

    @rx.var(cache=True)
    def cursos_inscritos(self) -> list[dict]:
        est = self.estudiante_actual
        return [c for c in self.cursos_con_profesores if c["id"] in est.cursos_inscritos]