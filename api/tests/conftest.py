import pytest
from app import create_app
from instance import TestingConfig

# Se crea un fixture para el client
@pytest.fixture
def client():
    # Como en app.py la instancia se crea desde una funcion, la importamos y la creamos en el fixture
    app = create_app(TestingConfig)
    # Configuramos el entorno de pruebas
    app.config['TESTING'] = True
    # Creamos el client
    with app.test_client() as client:
        yield client


# Fixture POST para crear tickets de prueba validos
@pytest.fixture
def post_sample_tickets(client):
    '''
    Inserta 3 tickets de prueba validos antes del testeo.
    '''
    client.post('/tickets', json={"title": "T1", "description": "D1"})
    client.post('/tickets', json={"title": "T2", "description": "D2"})
    client.post('/tickets', json={"title": "T3", "description": "D3"})
