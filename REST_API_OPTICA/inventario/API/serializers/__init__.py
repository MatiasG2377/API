from .categoria import CategoriaSerializer
from .proveedor import ProveedorSerializer
from .producto import ProductoSerializer
from .cliente import ClienteSerializer
from .venta import VentaSerializer, ArticuloVentaSerializer
from .abono import AbonoReadSerializer, AbonoWriteSerializer, ClienteAbonoSerializer, VentaAbonoSerializer
from .kardex import KardexReadSerializer,KardexWriteSerializer
from .usuario import UsuarioSerializer, UsuarioIdSerializer
from .paciente import PacienteSerializer
from .ficha_medica import FichaMedicaReadSerializer, FichaMedicaWriteSerializer
from .auth import UserSerializer
from .reportes import EtiquetaValorSerializer
from .movimiento_inventario import MovimientoInventarioSerializer