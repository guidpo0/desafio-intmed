from rest_framework import serializers
from medicar import models as medicar_models


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = medicar_models.Medico
        fields = '__all__'


class AgendaSerializer(serializers.ModelSerializer):
    medico = MedicoSerializer(read_only=True)

    class Meta:
        model = medicar_models.Agenda
        fields = '__all__'


class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = medicar_models.Consulta
        fields = '__all__'
