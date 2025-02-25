# store/models/itempedido.py
from django.db import models
from store.models import Producto, Pedido

class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, related_name='items', 
        on_delete=models.CASCADE, verbose_name="Pedido"
    )
    producto = models.ForeignKey(
        Producto, on_delete=models.PROTECT, verbose_name="Producto"
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")

    def total_item(self):
        return self.precio * self.cantidad

    def __str__(self):
        return f"{self.producto.nombre}"

    class Meta:
        db_table = 'st_items_pedido'
        verbose_name = "Item de Pedido"
        verbose_name_plural = "Items de Pedido"