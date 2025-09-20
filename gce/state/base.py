import reflex as rx
from ..models import Curso, Profesor, Estudiante

# ---------- 1. BASE STATE (datos y helpers comunes) ----------
class BaseState(rx.State):
    usuario_actual_id: int = 1
    rol_actual: str = ""

    # DATOS → siempre en BaseState
    cursos: list[Curso] = [
        Curso(id=1, nombre="Intro Programación", profesor_id=1, cupos_totales=20,
              descripcion="Fundamentos de programación", aplicable="1er Medio", horario="Lunes 15:00-16:30",
              estudiantes_inscritos=[1, 3]),
        Curso(id=2, nombre="Matemáticas Avanzadas", profesor_id=2, cupos_totales=15,
              descripcion="Cálculo y álgebra lineal", aplicable="2do Medio", horario="Martes 10:00-11:30",
              estudiantes_inscritos=[2, 4]),
        Curso(id=3, nombre="Historia Universal", profesor_id=3, cupos_totales=25,
              descripcion="Desde la antigüedad hasta hoy", aplicable="1er Medio", horario="Miércoles 09:00-10:30",
              estudiantes_inscritos=[1, 2, 5]),
        Curso(id=4, nombre="Física Cuántica", profesor_id=4, cupos_totales=10,
              descripcion="Principios de la mecánica cuántica", aplicable="3er Medio", horario="Jueves 14:00-15:30",
              estudiantes_inscritos=[3]),
        Curso(id=5, nombre="Literatura Clásica", profesor_id=5, cupos_totales=18,
              descripcion="Análisis de obras literarias", aplicable="2do Medio", horario="Viernes 11:00-12:30",
              estudiantes_inscritos=[4, 5]),
        # New courses
        Curso(id=6, nombre="Química Orgánica", profesor_id=1, profesor_suplente_id=2, cupos_totales=12,
              descripcion="Estudio de compuestos de carbono", aplicable="3er Medio", horario="Lunes 09:00-10:30",
              estudiantes_inscritos=[]),
        Curso(id=7, nombre="Programación Web", profesor_id=3, cupos_totales=10,
              descripcion="Desarrollo de aplicaciones web", aplicable="2do Medio", horario="Martes 14:00-15:30",
              estudiantes_inscritos=[2]), # Already has one student
        Curso(id=8, nombre="Diseño Gráfico", profesor_id=4, profesor_suplente_id=5, cupos_totales=8,
              descripcion="Principios de diseño visual", aplicable="1er Medio", horario="Miércoles 11:00-12:30",
              estudiantes_inscritos=[]),
        Curso(id=9, nombre="Economía Global", profesor_id=5, cupos_totales=20,
              descripcion="Análisis de mercados internacionales", aplicable="3er Medio", horario="Jueves 10:00-11:30",
              estudiantes_inscritos=[]),
        Curso(id=10, nombre="Filosofía Antigua", profesor_id=1, cupos_totales=15,
              descripcion="Pensadores griegos y romanos", aplicable="1er Medio", horario="Viernes 09:00-10:30",
              estudiantes_inscritos=[]),
    ]
    profesores: list[Profesor] = [
        Profesor(id=1, nombre="Ana López"),
        Profesor(id=2, nombre="Carlos Pérez"),
        Profesor(id=3, nombre="Laura García"),
        Profesor(id=4, nombre="Miguel Fernández"),
        Profesor(id=5, nombre="Sofía Ruiz"),
    ]
    estudiantes: list[Estudiante] = [
        Estudiante(id=1, nombre="Juan Pérez", nivel="1er Medio", cursos_inscritos=[1, 3]),
        Estudiante(id=2, nombre="María González", nivel="2do Medio", cursos_inscritos=[2, 3]),
        Estudiante(id=3, nombre="Pedro Ramírez", nivel="1er Medio", cursos_inscritos=[1, 4]),
        Estudiante(id=4, nombre="Ana Torres", nivel="2do Medio", cursos_inscritos=[2, 5]),
        Estudiante(id=5, nombre="Luis Soto", nivel="1er Medio", cursos_inscritos=[3, 5]),
    ]

    # HELPERS / VARS
    @rx.var(cache=True)
    def profesor_map(self) -> dict[int, str]:
        return {p.id: p.nombre for p in self.profesores}

    @rx.var(cache=True)
    def profesor_nombres(self) -> list[str]:
        return [p.nombre for p in self.profesores]

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
                "profesor_suplente_nombre": self.profesor_map.get(curso.profesor_suplente_id, "N/A") if curso.profesor_suplente_id else "N/A",
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