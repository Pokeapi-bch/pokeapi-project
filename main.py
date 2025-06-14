import os
import re  # Agregado para validación

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join("static", "index.html"))


@app.get("/pokemon/{name}")
async def get_pokemon(name: str):
    # Validación de entrada: solo letras y guiones permitidos
    if not re.fullmatch(r"[a-zA-Z\-]+", name):
        raise HTTPException(
            status_code=400,
            detail="Nombre inválido. Solo se permiten letras y guiones.",
        )

    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Pokemon no encontrado"}
