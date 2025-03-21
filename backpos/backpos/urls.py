from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from backpos.Controllers.login_controllers import login_controller, registrar_usuario_controller, login_usuario_controller, logout_usuario_controller
from backpos.Controllers.menu_users_controllers import menu_principal_controller 
from backpos.Controllers.users_controllers import mostrar_usuarios_controller
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

schema_view = get_schema_view(
    openapi.Info(
        title="POS DOCUMENTACION",
        default_version='v1',
        description="Documentación de la API del sistema",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="soporte@ejemplo.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('login/', login_controller, name='login'),
    path('crear_usuario', registrar_usuario_controller, name='registrar_usuario'),
    path('login_usuario', login_usuario_controller, name='login_usuario'),
    path('logout_usuario', logout_usuario_controller, name='logout_usuario'),
    path('home', menu_principal_controller, name='menu_principal_usuario'),
    path('update_users', mostrar_usuarios_controller, name='mostrar_usuarios_controller'),
]