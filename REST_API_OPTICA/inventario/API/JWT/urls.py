from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from inventario.API.vistas import RegisterView, LogoutView
from inventario.API.vistas import ProductoListView

urlpatterns = [
    # Login - obtener tokens (access y refresh)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Refrescar token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Logout - invalidar token
    path('logout/', LogoutView.as_view(), name='logout'),
    # Registro
    path('register/',RegisterView.as_view(), name= 'register'),

    path('productos/', ProductoListView.as_view(), name='productos-list'),

]
