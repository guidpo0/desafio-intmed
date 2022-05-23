from django.db import models


class Medico(models.Model):
    nome = models.CharField(max_length=255)
    crm = models.IntegerField(unique=True)
    email = models.EmailField(max_length=255)

    def __str__(self):
        return self.nome


class Horario(models.Model):
    horario = models.TimeField()

    def __str__(self):
        return self.horario


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia = models.DateField()
    horarios = models.ManyToManyField('Horario')

    def __str__(self):
        return self.medico.nome


class Consulta(models.Model):
    dia = models.DateField()
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    data_agendamento = models.DateTimeField(auto_now_add=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def __str__(self):
        return self.medico.nome
