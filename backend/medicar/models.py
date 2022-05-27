from django.db import models
from django.contrib.postgres.fields import ArrayField


class Medico(models.Model):
    nome = models.CharField(max_length=255, required=True)
    crm = models.IntegerField(unique=True, required=True)
    email = models.EmailField(max_length=255, default='')

    def __str__(self):
        return self.nome


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, required=True)
    dia = models.DateField(required=True)
    horarios = ArrayField(models.TimeField(), required=True)

    def __str__(self):
        return self.medico.nome


class Consulta(models.Model):
    dia = models.DateField()
    horario = models.TimeField()
    data_agendamento = models.DateTimeField(auto_now_add=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def __str__(self):
        return self.medico.nome
