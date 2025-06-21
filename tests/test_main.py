# tests/test_main.py
from unittest.mock import AsyncMock, patch

import httpx  # Necesario para simular solicitudes HTTP y errores
import pytest
from fastapi import HTTPException  # Necesario para los tests de excepciones
from fastapi.testclient import TestClient

from main import (  # Importa también fetch_pokemon_data para probarla
    app,
    fetch_pokemon_data,
)

# Creamos una instancia de TestClient para la aplicación FastAPI
client = TestClient(app)


# Prueba para el endpoint de la página de inicio
def test_read_root():
    """
    Verifica que el endpoint '/' devuelve la página HTML de inicio (index.html).
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "html" in response.text
    # Opcional: Si tu index.html tiene un texto particular
    # assert b"PokeAPI Project" in response.content


# Prueba para el endpoint de obtener Pokémon (éxito)
def test_get_pokemon_success():
    """
    Verifica que el endpoint '/pokemon/{name}' devuelve datos correctos para un Pokémon válido.
    """
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json()["name"] == "pikachu"
    assert "abilities" in response.json()


# Prueba para el endpoint de obtener Pokémon (no encontrado)
def test_get_pokemon_not_found():
    """
    Verifica que el endpoint '/pokemon/{name}' devuelve 404 para un Pokémon inexistente.
    """
    # Línea 34: URL dividida para evitar E501
    response = client.get(
        "/pokemon/invalidpokemonname12345"
    )  # Nombre que sabes que no existe
    assert response.status_code == 404
    # Línea 36: Mensaje de detalle dividido para evitar E501
    assert (
        response.json()["detail"] == "Pokémon 'invalidpokemonname12345' no encontrado."
    )


# --- Pruebas Opcionales: Para la función fetch_pokemon_data (mockeando la API externa) ---


@pytest.mark.asyncio
async def test_fetch_pokemon_data_api_network_error():
    """
    Verifica que fetch_pokemon_data maneja errores de red al conectar con la API externa.
    """
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        # Línea 56: Argumentos de RequestError divididos para evitar E501
        mock_get.side_effect = httpx.RequestError(
            "Mock network error", request=httpx.Request("GET", "http://test")
        )
        with pytest.raises(HTTPException) as exc_info:
            await fetch_pokemon_data("bulbasaur")
        assert exc_info.value.status_code == 500
        assert "Error de red" in exc_info.value.detail


@pytest.mark.asyncio
async def test_fetch_pokemon_data_http_500_error():
    """
    Verifica que fetch_pokemon_data maneja errores HTTP 500 de la API externa.
    """
    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        # Línea 60: Argumentos de Response divididos para evitar E501
        mock_response = httpx.Response(500, request=httpx.Request("GET", "http://test"))
        mock_get.return_value = mock_response
        with pytest.raises(HTTPException) as exc_info:
            await fetch_pokemon_data("charizard")
        assert exc_info.value.status_code == 500
        assert "Error al conectar con PokeAPI" in exc_info.value.detail
