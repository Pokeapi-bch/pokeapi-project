import os

import httpx  # Para realizar solicitudes HTTP
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# --- Configuración de la aplicación FastAPI ---
app = FastAPI(
    title="PokeAPI Project",  # Añadir un título para la documentación de la API
    description="Una API simple para obtener información de Pokémon usando PokeAPI.",
    version="1.0.0",
)

# Montar archivos estáticos para servir el HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Funciones de Utilidad / Lógica de Negocio ---


async def fetch_pokemon_data(pokemon_name: str) -> dict:
    """
    Obtiene los datos de un Pokémon específico desde la PokeAPI.

    Args:
        pokemon_name (str): El nombre del Pokémon a buscar.

    Returns:
        dict: Un diccionario con los datos del Pokémon si se encuentra.

    Raises:
        HTTPException: Si el Pokémon no se encuentra (status 404)
                       o si hay un error en la conexión a la API (status 500).
    """
    pokeapi_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(pokeapi_url)
            response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=(
                    f"Pokémon '{pokemon_name}' no encontrado."
                ),  # Línea dividida aquí
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error al conectar con PokeAPI: {e}",  # Línea dividida aquí
            )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de red al conectar con PokeAPI: {e}",  # Línea dividida aquí
        )


# --- Endpoints de la API ---


@app.get("/", summary="Página de inicio")
async def read_root() -> FileResponse:
    """
    Sirve la página HTML de inicio.
    """
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/pokemon/{name}", summary="Obtener información de Pokémon")
async def get_pokemon(name: str) -> dict:
    """
    Endpoint para obtener información detallada de un Pokémon.

    Args:
        name (str): El nombre del Pokémon.

    Returns:
        dict: Datos JSON del Pokémon.
    """
    return await fetch_pokemon_data(name)
