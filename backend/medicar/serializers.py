from rest_framework import serializers
from medicar import models as medicar_models
from datetime import datetime
from .models import Agenda


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = medicar_models.Medico
        fields = '__all__'


class AgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = medicar_models.Agenda
        fields = '__all__'

    def validate_dia(self, dia):
        medico_ja_tem_agenda_neste_dia = Agenda.objects.filter(
            medico=self.initial_data['medico'], dia=dia
        ).exists()

        if medico_ja_tem_agenda_neste_dia:
            raise serializers.ValidationError(
                'Já existe uma agenda para este médico nesse dia'
            )
        if dia < datetime.now().date():
            raise serializers.ValidationError(
                'Não é possível cadastrar uma agenda para um dia anterior'
            )
        return dia

    def validate_horarios(self, horarios):
        if len(horarios) == 0:
            raise serializers.ValidationError('Informe pelo menos 1 horário')
        return horarios


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = medicar_models.Consulta
        fields = '__all__'

    def validate(self, data):
        now = datetime.now()
        agenda_do_medico = Agenda.objects.filter(
            medico=data['medico'], dia=data['dia']
        ).first()

        if agenda_do_medico is None:
            raise serializers.ValidationError(
                'Não existe agenda para esse médico nesse dia'
            )

        if data['horario'] not in agenda_do_medico.horarios:
            raise serializers.ValidationError(
                'O horário informado não está disponível para esse médico'
            )

        if data['dia'] < now.date():
            raise serializers.ValidationError(
                'Não é possível cadastrar uma consulta para um dia anterior'
            )

        if data['horario'] < now.time() and data['dia'] == now.date():
            raise serializers.ValidationError(
                'Não é possível cadastrar uma consulta nesse horário'
            )

        agenda_do_medico.horarios.remove(data['horario'])
        Agenda.objects.update(
            medico=data['medico'],
            dia=data['dia'],
            horarios=agenda_do_medico.horarios
        )

        return data
