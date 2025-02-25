from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.ajax_logout, name='logout'),
    
    # Rutas para procesar solicitudes AJAX:
    path('ajax/signup/', views.ajax_signup, name='ajax_signup'),
    path('ajax/signin/', views.ajax_signin, name='ajax_signin'),
    path('ajax/checkout/', views.ajax_checkout, name='ajax_checkout')
]
