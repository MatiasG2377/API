from django.db import migrations

def actualizar_imagenes(apps, schema_editor):
    # Obtén el modelo Producto
    Producto = apps.get_model('inventario', 'Producto')
    # URL que deseas asignar
    url_default = "https://andromedainc.com/cdn/shop/products/LENTESPARACOMPUTADORA43930AISO.jpg?v=1669831838"
    # Actualizar todas las filas con la URL predeterminada
    Producto.objects.filter(imagen_producto__isnull=True).update(imagen_producto=url_default)

class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0004_alter_producto_imagen_producto'),  # Cambia este número por el de tu migración anterior
    ]

    operations = [
        migrations.RunPython(actualizar_imagenes),
    ]
