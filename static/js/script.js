// Guardar y obtener el carrito en localStorage
const guardarCarrito = (carrito) => {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

const obtenerCarrito = () => {
    return JSON.parse(localStorage.getItem('carrito')) || [];
} 

// Agregar un producto al carrito
const agregarAlCarrito = (boton) => {
    let divProductCard = boton.closest('.product-card');
    let productId = divProductCard.getAttribute('data-product-id');
    let nombreProducto = divProductCard.querySelector('h3').textContent;
    let precioProducto = parseFloat(divProductCard.querySelector('p').textContent.replace('$', ''));
    let cantidad = parseInt(divProductCard.querySelector('input').value);

    let carrito = obtenerCarrito();
    // Crear objeto con los datos necesarios
    let producto = { product_id: productId, nombre: nombreProducto, precio: precioProducto, cantidad: cantidad };
    let existente = carrito.find(item => item.product_id === productId);
    if (existente) {
        existente.cantidad += cantidad;
    } else {
        carrito.push(producto);
    }
    guardarCarrito(carrito);
    alert(`Se añadió el producto al carrito: ${nombreProducto}`);
}

// Renderizar el carrito en la página del carrito
const renderizarCarrito = () => {
    let tablaCarrito = document.getElementById('body-cart');
    if (!tablaCarrito) return;
    tablaCarrito.innerHTML = '';
    let carrito = obtenerCarrito();
    let total = 0;

    carrito.forEach((item, index) => {
        let fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${item.nombre}</td>
            <td>$${item.precio.toFixed(2)}</td>
            <td>${item.cantidad}</td>
            <td>$${(item.precio * item.cantidad).toFixed(2)}</td>
            <td><button onclick="eliminarDelCarrito(${index})">Eliminar</button></td>
        `;
        total += (item.precio * item.cantidad);
        tablaCarrito.appendChild(fila);
    });
    document.querySelector('#foot-cart td:last-child').textContent = `$${total.toFixed(2)}`;
}

// Eliminar un elemento del carrito
const eliminarDelCarrito = (index) => {
    let carrito = obtenerCarrito();
    carrito.splice(index, 1);
    guardarCarrito(carrito);
    renderizarCarrito();
}

// Función para procesar el checkout del pedido
const procesarCheckout = () => {
    let carrito = obtenerCarrito();
    if (carrito.length === 0) {
        alert("El carrito está vacío.");
        return;
    }

    // Enviar los datos del carrito en formato JSON al servidor
    axios.post(ajaxCheckoutUrl, {
        items: carrito
    }, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => {
        if (response.data.success) {
            alert(response.data.message);
            // Limpiar el carrito
            localStorage.removeItem('carrito');
            window.location.href = homeUrl;
        } else {
            alert("Error al procesar el pedido: " + response.data.message);
        }
    })
    .catch(error => {
        console.error('Error en checkout:', error);
        alert("Ocurrió un error en el proceso de compra.");
    });
}

// Asignar eventos basados en la existencia de elementos en el DOM
document.addEventListener('DOMContentLoaded', function() {
    // Si estamos en la página del carrito, renderizamos el contenido
    if (document.getElementById('body-cart')) {
        renderizarCarrito();
    }
    // Si existe el botón de checkout (por id "btn-checkout"), asociar el evento
    let btnCheckout = document.getElementById('btn-checkout');
    if (btnCheckout) {
        btnCheckout.addEventListener('click', procesarCheckout);
    }
});