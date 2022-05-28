from rest_framework.test import APITestCase
from rest_framework import status
from medicar.models import Medico


class TestAgenda(APITestCase):
    def setUp(self):
        self.medico = Medico.objects.create(
            nome='Dr. João',
            crm='12345',
            email='',
        )
        self.medico.save()
        self.medico = Medico.objects.get(id=self.medico.id)

    def test_requisicao_para_listar_agendas(self):
        response = self.client.get('/agendas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_requisicao_para_criar_agenda(self):
        response = self.client.post(
            '/agendas/',
            {
                'medico': self.medico.id,
                'dia': '2023-01-01',
                'horario': '10:00:00',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_requisicao_para_criar_agenda_com_horario_invalido(self):
        response = self.client.post(
            '/agendas/',
            {
                'medico': self.medico.id,
                'dia': '2023-01-01',
                'horario': '10:00:00',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_para_criar_agenda_com_dia_invalido(self):
        response = self.client.post(
            '/agendas/',
            {
                'medico': self.medico.id,
                'dia': '2023-01-01',
                'horario': '10:00:00',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_para_criar_agenda_com_medico_invalido(self):
        response = self.client.post(
            '/agendas/',
            {
                'medico': '',
                'dia': '2023-01-01',
                'horario': '10:00:00',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_requisicao_para_criar_agenda_com_medico_inexistente(self):
        response = self.client.post(
            '/agendas/',
            {
                'medico': '999999',
                'dia': '2023-01-01',
                'horario': '10:00:00',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
