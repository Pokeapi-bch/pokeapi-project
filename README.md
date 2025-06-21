# PokeAPI Project



Este proyecto es una interfaz sencilla para consultar información de Pokémon utilizando la API pública [PokeAPI](https://pokeapi.co/), construida con FastAPI para el backend y una interfaz web estática en HTML y JavaScript.



## Características



- Servidor FastAPI que sirve una página web estática.

- Endpoint para obtener datos de Pokémon desde la API oficial.

- Interfaz web para buscar Pokémon por nombre y mostrar detalles como ID, altura, peso, tipos, habilidades e imagen.

- Contenedor Docker para facilitar el despliegue.



## Requisitos



- Python 3.10+

- Dependencias listadas en `requirements.txt`:

  - fastapi

  - uvicorn

  - httpx

- Docker (opcional, para usar el contenedor)



## Instalación y ejecución local



1. Clonar el repositorio:



   git clone https://github.com/Pokeapi-bch/pokeapi-project.git

   cd pokeapi-project



2. Crear y activar un entorno virtual (opcional pero recomendado):



   ```bash

   python -m venv venv

   source venv/bin/activate  # En Windows: venv\Scripts\activate

   ```



3. Instalar dependencias:



   ```bash

   pip install -r requirements.txt

   ```



4. Ejecutar la aplicación:



   ```bash

   uvicorn main:app --reload

   ```



5. Abrir en el navegador la URL:



   ```

   http://localhost:8000/

   ```



## Uso con Docker



1. Construir la imagen Docker:



   ```bash

   docker build -t pokeapi-project .

   ```



2. Ejecutar el contenedor:



   ```bash

   docker run -p 8000:8000 pokeapi-project

   ```



3. Abrir en el navegador la URL:



   ```

   http://localhost:8000/

   ```



## Endpoints API



- `GET /pokemon/{name}`: Obtiene información del Pokémon con el nombre especificado.



  - Parámetros:

    - `name` (string): Nombre del Pokémon (ejemplo: pikachu).



## Interfaz Web



- Página principal con formulario para ingresar el nombre del Pokémon.

- Muestra detalles como nombre, ID, altura, peso, tipos, habilidades e imagen.

- Validación básica y mensajes de error si no se encuentra el Pokémon.



## Estructura del proyecto



----------------------

.

├── Dockerfile

├── main.py

├── requirements.txt

└── static

    └── index.html
