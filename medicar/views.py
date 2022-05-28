from rest_framework import viewsets
from medicar import models as medicar_models
from medicar import serializers as medicar_serializers
from datetime import datetime
from django_filters import rest_framework as filters


class MedicoViewSet(viewsets.ModelViewSet):
    queryset = medicar_models.Medico.objects.all()
    serializer_class = medicar_serializers.MedicoSerializer


class AgendaFilter(filters.FilterSet):
    data_inicio = filters.DateFilter(field_name='dia', lookup_expr='gte')
    data_fim = filters.DateFilter(field_name='dia', lookup_expr='lte')
    medico = filters.NumberFilter(field_name='medico', lookup_expr='exact')
    crm = filters.NumberFilter(field_name='medico__crm', lookup_expr='exact')

    class Meta:
        model = medicar_models.Agenda
        fields = ['dia', 'medico']


class AgendaViewSet(viewsets.ModelViewSet):
    queryset = medicar_models.Agenda.objects.all()
    serializer_class = medicar_serializers.AgendaSerializer
    filterset_class = AgendaFilter

    def get_queryset(self):
        queryset = medicar_models.Agenda.objects.filter(
            dia__gte=datetime.now().date(), horarios__len__gt=0
        ).order_by('dia')
        for agenda in queryset:
            if agenda.dia == datetime.now().date():
                agenda.horarios = [
                    horario for horario in agenda.horarios
                    if horario >= datetime.now().time()
                ]

        return queryset


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = medicar_models.Consulta.objects.filter(
        dia__gte=datetime.now().date()
    ).order_by('dia', 'horario')
    serializer_class = medicar_serializers.ConsultaSerializer
    http_method_names = ['get', 'post', 'delete']
