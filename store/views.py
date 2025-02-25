from django.shortcuts import render
from django.core.paginator import Paginator
from store.models import Producto, Pedido, ItemPedido
from .forms import SignupForm
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from decimal import Decimal

def home(request):
    # Filtramos los productos activos y que están marcados como destacados
    featured_products = Producto.objects.filter(activo=True, destacado=True).order_by('-fecha_ult_act')
    context = {'featured_products': featured_products}
    return render(request, 'index.html', context)

def catalog(request):
    # Consultamos todos los productos activos
    products = Producto.objects.filter(activo=True)
    # Configuramos la paginación: 10 productos por página
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'catalog.html', context)

def cart(request):
    return render(request, 'cart.html')

def contact(request):
    return render(request, 'contact.html')

def signup(request):
    return render(request, 'signup.html')

@require_POST
def ajax_signup(request):
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        # Encriptamos la contraseña correctamente
        user.set_password(form.cleaned_data['password'])
        user.save()
        return JsonResponse({'success': True, 'message': 'Usuario registrado exitosamente.'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors})

def signin(request):
    return render(request, 'signin.html')

@require_POST
def ajax_signin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'success': True, 'message': 'Inicio de sesión exitoso.'})
    else:
        return JsonResponse({'success': False, 'errors': {'__all__': "Credenciales incorrectas."}})

def ajax_logout(request):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Sesión cerrada exitosamente.'})


@require_POST
@login_required  # Solo usuarios autenticados pueden realizar pedidos
def ajax_checkout(request):
    """
    Se espera recibir un JSON en el cuerpo de la solicitud con la estructura:
    {
        "items": [
            {"product_id": "1", "nombre": "Producto A", "precio": 9.99, "cantidad": 2},
            {"product_id": "3", "nombre": "Producto B", "precio": 19.99, "cantidad": 1},
            ...
        ]
    }
    """
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        if not items:
            return JsonResponse({'success': False, 'message': 'El carrito está vacío.'})

        total_pedido = Decimal('0.00')
        for item in items:
            precio = Decimal(str(item.get('precio', '0.00')))
            cantidad = int(item.get('cantidad', 0))
            total_pedido += precio * cantidad

        pedido = Pedido.objects.create(
            usuario=request.user,
            total=total_pedido
        )

        for item in items:
            product_id = item.get('product_id')
            cantidad = int(item.get('cantidad', 0))
            # Se obtiene el producto desde el modelo Producto
            producto = Producto.objects.get(pk=product_id)
            # Se usa el precio actual del producto; alternativamente, se puede usar el enviado
            precio = producto.precio  
            ItemPedido.objects.create(
                pedido=pedido,
                producto=producto,
                precio=precio,
                cantidad=cantidad
            )

        return JsonResponse({
            'success': True,
            'message': 'Pedido procesado exitosamente.',
            'pedido_id': pedido.id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})