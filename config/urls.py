from django.contrib import admin
from django.urls import path, include
from medicar import views as medicar_views
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Medicar API",
        default_version='v1',
        description="API para gerenciamento de consultas",
        terms_of_service="#",
        contact=openapi.Contact(email="@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'medicos', medicar_views.MedicoViewSet)
router.register(r'agendas', medicar_views.AgendaViewSet)
router.register(r'consultas', medicar_views.ConsultaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path(
        'doc/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
]
