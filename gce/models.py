import reflex as rx
import sqlmodel as sm
import sqlalchemy as sa
import datetime

class Profesor(sm.SQLModel, table=True):
    id: int | None = sm.Field(default=None, primary_key=True)
    nombre: str

class Estudiante(sm.SQLModel, table=True):
    id: int | None = sm.Field(default=None, primary_key=True)
    nombre: str
    email: str = sm.Field(unique=True, index=True)
    password: str
    nivel: str
    cursos_inscritos: list[int] = sm.Field(default=[], sa_column=sa.Column(sa.JSON))
    is_active: bool = sm.Field(default=True, index=True)

class Curso(sm.SQLModel, table=True):
    id: int | None = sm.Field(default=None, primary_key=True)
    nombre: str
    profesor_id: int
    profesor_suplente_id: int | None = None
    cupos_totales: int
    descripcion: str
    aplicable: str
    horario: str
    estudiantes_inscritos: list[int] = sm.Field(default=[], sa_column=sa.Column(sa.JSON))

class AuditLog(sm.SQLModel, table=True):
    id: int | None = sm.Field(default=None, primary_key=True)
    timestamp: datetime.datetime = sm.Field(default_factory=datetime.datetime.utcnow, nullable=False)
    actor_id: int # Assuming admin is a user with an ID
    action: str
    target_entity: str
    target_id: int
    details: dict = sm.Field(default={}, sa_column=sa.Column(sa.JSON))
    