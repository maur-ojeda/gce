import reflex as rx
from .ui import UIState
from ..models import Curso

class StudentState(UIState):
    mensaje: str = ""

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
