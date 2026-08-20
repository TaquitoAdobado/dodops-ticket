# En este archivo se prueba la creación de tickets.

import pytest

# TEST CREACION TICKET VALIDO
def test_create_ticket(client):
    '''
    Prueba la creación de un ticket valido.
    Los datos enviados en el body deben ser:
    - title
    - description
    
    El retorno del ticket debe contener:
    - Un titulo
    - Una descripcion
    - Una fecha de creacion
    - Una fecha de cierre (null por defecto)
    '''
    # Enviamos la solicitud de prueba POST
    response = client.post('/tickets', json={
        'title': 'Title example ticket',
        'description': 'This is an example description for a ticket.'
    })

    # Validamos status code CREADO
    assert response.status_code == 201

    # Validamos estructura del JSON
    data = response.get_json()
    assert 'id' in data
    assert data['title'] == 'Title example ticket'
    assert data['description'] == 'This is an example description for a ticket.'
    assert 'creation_date' in data
    assert data['closed_date'] is None


# TEST CREACION TICKET INVALIDO
@pytest.mark.parametrize("payload", [
    {'title': '', 'description': ''},           # Ambos campos vacios
    {'title': '   \t ', 'description': '\n'},   # Ambos campos con espacios
    {'title': ''},                              # Campo description ausente
    {'description': ''},                        # Campo title ausente
    {},                                         # Campos title y description ausentes
    None                                        # JSON con body None
    ])
def test_create_invalid_ticket(client, payload):
    '''
    pytest.mark.parametrize es un decorador que permite ejecutar la prueba con distintos parametros.

    Prueba la creacion de un ticket invalido.
    Para que un ticket sea considerado invalido al crearse y que devuelva un status code 400,
    debe cumplirse almenos una de las siguientes condiciones:
    - Ausente title o description
    - Vacios title o description
    - JSON con body None
    '''
    
    # Enviamos la solicitud de prueba POST
    response = client.post('/tickets', json = payload)
    assert response.status_code == 400

#--------------------------------------------------------------------------------------------------
# TEST VER TICKETS (TODOS)
def test_get_tickets(client, post_sample_tickets):
    # Enviamos la solicitud de prueba GET
    response = client.get('/tickets')

    # Validamos status code OK
    assert response.status_code == 200

    # Validamos contenido del JSON
    data = response.get_json()
    assert len(data) == 3 # 3 tickets de prueba
    assert (data[0]['id'], data[0]['title'], data[0]['description']) == (1, 'T1', 'D1')
    assert (data[1]['id'], data[1]['title'], data[1]['description']) == (2, 'T2', 'D2')
    assert (data[2]['id'], data[2]['title'], data[2]['description']) == (3, 'T3', 'D3')

    assert 'creation_date' in data[0]
    assert 'closed_date' in data[0]
    assert data[0]['closed_date'] is None

# TEST VER TICKET ESPECIFICO (POR ID)
@pytest.mark.parametrize("id", [1,2,3,0,"a",-1,12345678901234567890])
def test_get_ticket(client, post_sample_tickets, id):
    response = client.get(f'/tickets/{id}')
    data =  response.get_json()

    if response.status_code == 200:
        
        # Validacion de contenido del JSON
        assert (data['id'], data['title'], data['description']) == (id, 'T'+str(id), 'D'+str(id))
        assert "creation_date" in data and "closed_date" in data 

    if response.status_code == 400:
        assert 'error' in data
        assert data['error'] == 'Invalid ticket ID'

    if response.status_code == 404:
        assert 'error' in data
        assert data['error'] == 'Ticket not found'

#--------------------------------------------------------------------------------------------------
# TEST ACTUALIZACION DE TICKET COMPLETO (title y description)
@pytest.mark.parametrize("id, payload, expected_error,expected_status", [
    (1, {'title': 'Edited title', 'description': 'Edited description'}, None, 200),
    (-1, {'title': 'Edited title', 'description': 'Edited description'}, "Invalid ticket ID", 400),
    ("a", {'title': 'Edited title', 'description': 'Edited description'}, "Invalid ticket ID", 400),
    (9999, {'title': 'Edited title', 'description': ''}, "Ticket not found", 404),
    (2, {'title': 'Edited title', 'description': ''}, "Title or description can't be empty", 400),
    (2, {'title': '', 'description': 'Edited description'}, "Title or description can't be empty", 400),
    (2, {}, "Missing title or description", 400),
    (2, None, "invalid or missing JSON body",400)
])
def test_put_valid_ticket(client, post_sample_tickets, id, payload, expected_error, expected_status):
    response = client.put(f'/tickets/{id}',json=payload)

    assert response.status_code == expected_status
    data = response.get_json()

    if 'error' in data:
        assert data['error'] == expected_error

    else:
        assert data['title'] == payload['title']
        assert data['description'] == payload['description']

#--------------------------------------------------------------------------------------------------
# TEST ACTUALIZACION DE TICKET PARCIAL (title o description)
@pytest.mark.parametrize("id, payload, expected_error,expected_status", [
    (1, {'title': 'Edited title'}, None, 200),
    (1, {'description': 'Edited description'}, None, 200),
    (-1, {'title': 'Edited title'}, "Invalid ticket ID", 400),
    ("a", {'title': 'Edited title'}, "Invalid ticket ID", 400),
    (9999, {'title': 'Edited title', 'description': ''}, "Ticket not found", 404),
    (2, {'description': ''}, "Description can't be empty", 400),
    (2, {'title': ''}, "Title can't be empty", 400),
    (2, {}, "Missing data", 400),
    (2, None, "invalid or missing JSON body",400)
])
def test_patch_valid_ticket(client, post_sample_tickets, id, payload, expected_error, expected_status):
    response = client.patch(f'/tickets/{id}',json=payload)

    assert response.status_code == expected_status
    data = response.get_json()

    if 'error' in data:
        assert data['error'] == expected_error

    else:
        if 'title' in payload:
            assert data['title'] == payload['title']
        if 'description' in payload:
            assert data['description'] == payload['description']

#--------------------------------------------------------------------------------------------------
# TEST ELIMINACION DE TICKET
@pytest.mark.parametrize("id, expected_error, expected_status", [
    (1, None, 204),
    (-1, "Invalid ticket ID", 400),
    ("a", "Invalid ticket ID", 400),
    (9999, "Ticket not found", 404),
    (0, "Invalid ticket ID", 400)
])
def test_delete_ticket(client, post_sample_tickets, id, expected_error, expected_status):
    response = client.delete(f'/tickets/{id}')

    assert response.status_code == expected_status

    data = response.get_json()
    if data:
        assert data['error'] == expected_error



