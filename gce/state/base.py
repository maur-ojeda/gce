import reflex as rx
from ..models import Curso, Profesor, Estudiante

# ---------- 1. BASE STATE (datos y helpers comunes) ----------
class BaseState(rx.State):
    usuario_actual_id: int = 1
    rol_actual: str = ""

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

    @rx.var
    def is_authenticated(self) -> bool:
        return self.rol_actual != ""

    # MÉTODOS COMUNES
    def login(self, rol: str):
        self.rol_actual = rol
        if rol == "administrador":
            return rx.redirect("/admin")
        elif rol == "estudiante":
            return rx.redirect("/estudiante")

    def logout(self):
        self.rol_actual = ""
        self.usuario_actual_id = 1
        return rx.redirect("/login")

    def require_admin(self):
        if not self.is_authenticated or self.rol_actual != "administrador":
            return rx.redirect("/login")

    def require_student(self):
        if not self.is_authenticated or self.rol_actual != "estudiante":
            return rx.redirect("/login")

    def cambiar_rol(self, nuevo: str):
        self.rol_actual = nuevo
        if nuevo == "administrador":
            return rx.redirect("/admin")
        elif nuevo == "estudiante":
            return rx.redirect("/estudiante")
