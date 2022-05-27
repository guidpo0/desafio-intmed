from rest_framework import viewsets, serializers
from medicar import models as medicar_models
from medicar import serializers as medicar_serializers
from datetime import datetime
from .models import Agenda


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

    def destroy(self, request, *args, **kwargs):
        consulta = self.get_object()
        medico = consulta.medico
        dia = consulta.dia
        horario = consulta.horario
        now = datetime.now()

        if now.date() > dia:
            raise serializers.ValidationError(
                'Não é possível cancelar uma consulta que já ocorreu'
            )

        if now.date() == dia and now.time() > horario:
            raise serializers.ValidationError(
                'Não é possível cancelar uma consulta para um horário anterior'
            )

        agenda_do_medico = Agenda.objects.filter(
            medico=medico, dia=dia
        ).first()

        agenda_do_medico.horarios.append(horario)
        Agenda.objects.update(
            medico=medico,
            dia=dia,
            horarios=agenda_do_medico.horarios
        )

        return super().destroy(request, *args, **kwargs)
