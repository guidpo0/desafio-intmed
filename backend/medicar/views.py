from rest_framework import viewsets
from medicar import models as medicar_models
from medicar import serializers as medicar_serializers


class MedicoViewSet(viewsets.ModelViewSet):
    queryset = medicar_models.Medico.objects.all()
    serializer_class = medicar_serializers.MedicoSerializer


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = medicar_models.Agenda.objects.all()
    serializer_class = medicar_serializers.AgendaSerializer


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = medicar_models.Consulta.objects.all()
    serializer_class = medicar_serializers.ConsultaSerializer
    http_method_names = ['get', 'post', 'delete']
