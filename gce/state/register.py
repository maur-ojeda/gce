import reflex as rx
import re
import sqlmodel as sm
from .ui import UIState
from .base import get_session
from ..models import Estudiante
from ..database import get_password_hash

class RegisterState(UIState):
    nombre: str = ""
    email: str = ""
    password: str = ""
    mensaje: str = ""

    def set_nombre(self, nombre: str):
        self.nombre = nombre

    def set_email(self, email: str):
        self.email = email

    def set_password(self, password: str):
        self.password = password

    def handle_registration(self):
        # Validar formato de correo y fortaleza de contraseña
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.mensaje = "Formato de correo electrónico inválido."
            return

        if len(self.password) < 8:
            self.mensaje = "La contraseña debe tener al menos 8 caracteres."
            return

        with get_session() as session:
            # Verificar si el correo ya existe
            existing_student = session.exec(
                sm.select(Estudiante).where(Estudiante.email == self.email)
            ).first()

            if existing_student:
                self.mensaje = "El correo electrónico ya está registrado."
                return

            # Crear cuenta con rol de "Estudiante"
            hashed_password = get_password_hash(self.password)
            new_student = Estudiante(
                nombre=self.nombre,
                email=self.email,
                password=hashed_password,
                nivel="Primaria",  # Default level
                cursos_inscritos=[]
            )
            session.add(new_student)
            session.commit()

        # Notificar al usuario
        self.mensaje = "¡Registro exitoso! Ahora puedes iniciar sesión."
        return rx.redirect("/login")

    def clear_fields(self):
        self.nombre = ""
        self.email = ""
        self.password = ""
        self.mensaje = ""
