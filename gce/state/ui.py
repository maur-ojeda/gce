import reflex as rx
from .base import BaseState

class UIState(BaseState):
    show_form_modal: bool = False
    show_detalle_modal: bool = False
    detalle_curso_id: int = -1

    def toggle_modal(self):
        self.show_form_modal = not self.show_form_modal

    def toggle_detalle(self):
        self.show_detalle_modal = not self.show_detalle_modal
        if not self.show_detalle_modal:
            self.detalle_curso_id = -1
