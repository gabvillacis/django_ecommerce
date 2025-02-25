from django.contrib import admin
from store.models import Categoria, Producto, Pedido, ItemPedido
from django.db.models import Count

admin.site.site_header = 'Administrador de Ecommerce'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'fecha_registro', 'fecha_ult_act')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion', 'precio', 'activo', 'destacado', 'fecha_registro', 'fecha_ult_act')

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido    
    extra = 0
    
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    inlines = (ItemPedidoInline,)
    list_display = ('id', 'usuario', 'fecha_creacion', 'total', 'cantidad_items')
    list_filter = ('usuario', 'fecha_creacion')
    search_fields = ('items__producto__nombre',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(num_items = Count('items'))
    
    def cantidad_items(self, obj):
        return obj.num_items
    
    cantidad_items.short_description = 'Cantidad de Items'