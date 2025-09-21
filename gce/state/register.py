import reflex as rx
import re
from .ui import UIState
from ..models import Estudiante

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
        # CA-1.3: Validar formato de correo y fortaleza de contraseña
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            self.mensaje = "Formato de correo electrónico inválido."
            return

        if len(self.password) < 8:
            self.mensaje = "La contraseña debe tener al menos 8 caracteres."
            return

        # CA-1.6: Verificar si el correo ya existe
        if any(est.nombre == self.email for est in self.estudiantes):
            self.mensaje = "El correo electrónico ya está registrado."
            return

        # CA-1.4: Crear cuenta con rol de "Estudiante"
        # For now, we are using the student's name as the email.
        # In a real application, you would have a separate User model.
        new_student_id = len(self.estudiantes) + 1
        new_student = Estudiante(
            id=new_student_id,
            nombre=self.nombre,
            nivel="Primaria",  # Default level
            cursos_inscritos=[]
        )
        self.estudiantes.append(new_student)

        # CA-1.5: Notificar al usuario
        self.mensaje = "¡Registro exitoso! Ahora puedes iniciar sesión."
        return rx.redirect("/login")
