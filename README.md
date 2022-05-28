# Especificações técnicas de backend do Medicar

## Passo a passo para rodar o projeto localmente

1. Faça o clone do projeto;
2. Criar ambiente virtual do python com o comando: `python3 -m venv venv`;
3. Entre no diretório do projeto e rode o comando: `source venv/bin/activate`;
4. Instale as dependências do projeto com o comando: `pip install -r requirements.txt`;
5. Crie um banco de dados utilizando PostgreSQL;
6. Crie um arquivo `.env` com as variáveis de ambiente referentes ao banco de dados para o projeto, seguindo o padrão de .env.example;
7. Criar um superusuário para o admin com o comando: `python manage.py createsuperuser`;
8. Popular o banco de dados com o comando: `python manage.py migrate`;
9. Rodar o projeto com o comando: `python3 manage.py runserver`;
10. A documentação da API também pode ser acessada por '/doc'.


## Interface administrativa

A interface administrativa (/admin) contém a funcionalidade a seguir:

### Cadastrar médico

É possível cadastrar os médicos que podem atender na clínica fornecendo as seguintes informações:

- **Nome:** Nome do médico (obrigatório)
- **CRM:** Número do médico no conselho regional de medicina (obrigatório)
- **E-mail:** Endereço de e-mail do médico (opcional)

#### Restrições:

- Não é possível cadastrar médico com um CRM que outro médico já utilize

### Criar agenda para médico

É possível criar uma agenda para o médico em um dia específico fornecendo as seguintes informações:

- **Médico:** Médico que será alocado (obrigatório)
- **Dia:** Data de alocação do médico (obrigatório)
- **Horários:** Lista de horários na qual o médico deverá ser alocado para o dia especificado (obrigatório)

#### Restrições:

- Não é possível criar mais de uma agenda para um médico em um mesmo dia
- Não é possível criar uma agenda para um médico em um dia passado

## API

### Autenticação

Todos os endpoints da API são abertos e não possuem autenticação 

### Listar consultas marcadas

Lista todas as consultas marcadas

#### Requisição

```
GET /consultas/
```

#### Retorno

```json
[
  {
    "id": 1,
    "dia": "2022-02-05",
    "horario": "12:00",
    "data_agendamento": "2022-02-01T10:45:0-03:00",
    "medico": {
      "id": 1,
      "crm": 3711,
      "nome": "Drauzio Varella",
      "email": "drauzinho@globo.com"
    }
  },
  {
    "id": 2,
    "dia": "2022-03-01",
    "horario": "09:00",
    "data_agendamento": "2022-02-01T10:45:0-03:00",
    "medico": {
      "id": 2,
      "crm": 2544,
      "nome": "Gregory House",
      "email": "greg@hbo.com.br"
    }
  }
]
```

#### Regras de negócio

- A listagem não exibe consultas para dia e horário passados
- Os itens da listagem são ordenados por ordem crescente do dia e horário da consulta

### Listar agendas disponíveis

Lista todas as agendas disponíveis na clínica

```json
[
  {
    "id": 1,
    "medico": {
      "id": 1,
      "crm": 3711,
      "nome": "Drauzio Varella",
      "email": "drauzinho@globo.com"
    },
    "dia": "2020-02-10",
    "horarios": ["14:00", "14:15", "16:00"]
  },
  {
    "id": 2,
    "medico": {
      "id": 2,
      "crm": 2544,
      "nome": "Gregory House",
      "email": "greg@hbo.com.br"
    },
    "dia": "2020-02-10",
    "horarios": ["08:00", "08:30", "09:00", "09:30", "14:00"]
  }
]
```

#### Filtros

- Identificador de um ou mais médicos
- Identificador de uma ou mais CRM
- Intervalo de data

```
# Retorna as agendas dos médicos 1 e 2 no período de 1 a 5 de janeiro
GET /agendas/?medico=1&medico=2&data_inicio=2022-01-01&data_final=2022-01-05

# Retorna as agendas dos médicos de CRM passados no filtro no período de 1 a 5 de janeiro
GET /agendas/?crm=2544&crm=3711&data_inicio=2022-01-01&data_final=2022-01-05
```

#### Regras de negócio

- As agendas são ordenadas por ordem crescente de data
- Agendas para datas passadas ou que todos os seus horários já foram preenchidos são excluídas da listagem
- Horários dentro de uma agenda que já passaram ou que foram preenchidos são excluídos da listagem

### Marcar consulta

Marca uma consulta

#### Requisição

```
POST /consultas/
{
  "agenda_id": 1,
  "horario": "14:15"
}
```

#### Retorno

```json
{
  "id": 2,
  "dia": "2022-03-01",
  "horario": "09:00",
  "data_agendamento": "2022-02-01T10:45:0-03:00",
  "medico": {
    "id": 1,
    "crm": 3711,
    "nome": "Drauzio Varella",
    "email": "drauzinho@globo.com"
  }
}
```

#### Regras de negócio

- A data em que o agendamento foi feito é salva ao se marcar uma consulta
- Não é possível marcar uma consulta para um dia e horário passados
- Não é possível marcar uma consulta se o dia e horário já foram preenchidos

### Desmarcar consulta

Desmarca uma consulta

#### Requisição

```
DELETE /consultas/<consulta_id>
```

#### Retorno

Não há retorno (vazio)

#### Regras de negócio

- Não é possível desmarcar uma consulta que nunca foi marcada (identificador inexistente)
- Não é possível desmarcar uma consulta que já aconteceu
