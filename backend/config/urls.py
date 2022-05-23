from django.contrib import admin
from django.urls import path, include
from medicar import views as medicar_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'medicos', medicar_views.MedicoViewSet)
router.register(r'horarios', medicar_views.HorarioViewSet)
router.register(r'agendas', medicar_views.AgendaViewSet)
router.register(r'consultas', medicar_views.ConsultaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
