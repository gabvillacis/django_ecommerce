# store/models/producto.py
from django.db import models
from .categoria import Categoria

class Producto(models.Model):
    categorias = models.ManyToManyField(Categoria, related_name='productos')
    nombre = models.CharField(max_length=125)
    id_url_friendly = models.SlugField(max_length=150, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes_prod/')
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_ult_act = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.nombre} ({self.id})'

    class Meta:
        db_table = 'st_productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'