# store/models/pedido.py
from django.db import models
from django.conf import settings

class Pedido(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Usuario"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total del Pedido")

    def __str__(self):
        return f"Pedido {self.id}"

    class Meta:
        db_table = 'st_pedidos'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
