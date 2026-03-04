import pytest
import requests_mock
from pieces_service import app as app_pieces
from models_service import app as app_models

@pytest.fixture
def client_pieces():
    app_pieces.config['TESTING'] = True
    with app_pieces.test_client() as client:
        yield client

@pytest.fixture
def client_models():
    app_models.config['TESTING'] = True
    with app_models.test_client() as client:
        yield client

def test_service_models_non_autorise(client_models):
    response = client_models.get('/api/internal/used_pieces')
    assert response.status_code == 401

def test_service_models_autorise(client_models):
    en_tetes = {"Authorization": "Bearer secret-token-123"}
    response = client_models.get('/api/internal/used_pieces', headers=en_tetes)
    assert response.status_code == 200
    assert "p1" in response.get_json()["ids_pieces_utilisees"]

def test_service_pieces_filtre_pieces_utilisees(client_pieces):
    with requests_mock.Mocker() as m:
        m.get("http://localhost:5002/api/internal/used_pieces", json={"ids_pieces_utilisees": ["p1"]}, status_code=200)
        
        response = client_pieces.get('/pieces/available')
        donnees = response.get_json()
        
        assert response.status_code == 200
        assert len(donnees) == 2
        assert not any(p["id"] == "p1" for p in donnees)