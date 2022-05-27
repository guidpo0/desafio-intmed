from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime
from django.core.exceptions import ValidationError


class Medico(models.Model):
    nome = models.CharField(max_length=255)
    crm = models.IntegerField(unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome


class Agenda(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    dia = models.DateField()
    horarios = ArrayField(models.TimeField())

    class Meta:
        unique_together = ('medico', 'dia')

    def __str__(self):
        return self.medico.nome

    def clean(self, *args, **kwargs):
        super(Agenda, self).clean(*args, **kwargs)
        now = datetime.now()
        existe_dia_na_agenda_do_medico = Agenda.objects.filter(
            medico=self.medico, dia=self.dia
        ).exists()

        if existe_dia_na_agenda_do_medico:
            raise ValidationError('Esse dia já foi cadastrado para esse médico')

        if self.dia < now.date():
            raise ValidationError(
                'Não é possível cadastrar uma data anterior'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Agenda, self).save(*args, **kwargs)


class Consulta(models.Model):
    dia = models.DateField()
    horario = models.TimeField()
    data_agendamento = models.DateTimeField(auto_now_add=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)

    def __str__(self):
        return self.medico.nome

    def clean(self, *args, **kwargs):
        super(Consulta, self).clean(*args, **kwargs)
        now = datetime.now()
        agenda_do_medico = Agenda.objects.filter(
            medico=self.medico, dia=self.dia
        ).first()

        if agenda_do_medico is None:
            raise ValidationError(
                'Não existe agenda para esse médico nesse dia'
            )

        if self.horario not in agenda_do_medico.horarios:
            raise ValidationError(
                'O horário informado não está disponível para esse médico'
            )

        if self.dia < now.date():
            raise ValidationError(
                'Não é possível cadastrar uma consulta para um dia anterior'
            )

        if self.horario < now.time() and self.dia == now.date():
            raise ValidationError(
                'Não é possível cadastrar uma consulta nesse horário'
            )

        agenda_do_medico.horarios.remove(self.horario)
        Agenda.objects.update(
            medico=self.medico,
            dia=self.dia,
            horarios=agenda_do_medico.horarios
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Consulta, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        now = datetime.now()
        now = datetime.now()

        if now.date() > self.dia:
            raise ValidationError(
                'Não é possível cancelar uma consulta que já ocorreu'
            )

        if now.date() == self.dia and now.time() > self.horario:
            raise ValidationError(
                'Não é possível cancelar uma consulta para um horário anterior'
            )

        agenda_do_medico = Agenda.objects.filter(
            medico=self.medico, dia=self.dia
        ).first()

        agenda_do_medico.horarios.append(self.horario)
        Agenda.objects.update(
            medico=self.medico,
            dia=self.dia,
            horarios=agenda_do_medico.horarios
        )

        super(Consulta, self).delete(*args, **kwargs)
