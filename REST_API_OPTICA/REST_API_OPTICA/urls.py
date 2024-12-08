from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('inventario.API.JWT.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('inventario.API.rutas'))
]
