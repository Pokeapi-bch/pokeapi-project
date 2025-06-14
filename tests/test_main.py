from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.text


def test_get_pokemon_valid():
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json()["name"] == "pikachu"


def test_get_pokemon_invalid():
    response = client.get("/pokemon/invalidpokemon")
    assert response.status_code == 200
    assert "error" in response.json()
