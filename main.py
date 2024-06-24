import io
import os
import subprocess
from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import networkx as nx
import matplotlib.pyplot as plt

from src.utils import prim, dijkstra, draw_dijkstra, draw_prim, obtener_camino
from src.classes import Prim, Dijkstra

algorithms = ["dijkstra", "flujo-maximo", "prim"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar la carpeta frontend/dist para servir contenido estático


@app.post("/prim")
async def prim_algorithm(request: Request):
    body = await request.json()
    # [['A', 'B', 1], ['A', 'C', 4], ['B', 'C', 2], ['B', 'D', 5], ['C', 'D', 1]]
    conexiones = body.get("conexiones")
    filename_path = "mst.png"
    if len(conexiones) == 0:
        return JSONResponse(content={"message": "Empty graph"}, status_code=400)
    P = Prim(conexiones=conexiones)
    try:
        mst = prim(P)
        print("Vértices del MST:", mst.vertices())
        print("Aristas del MST:", mst.aristas())
        draw_prim(P, mst, filename=filename_path)
    except ValueError as e:
        draw_prim(P, filename=filename_path)
        print("Error:", e)

    if not os.path.exists(filename_path):
        raise HTTPException(
            status_code=500, detail="Error al crear la imagen.")

    return FileResponse(filename_path, media_type="image/png")


@app.post("/dijkstra")
async def dijkstra_algorithm(request: Request):
    body = await request.json()
    conexiones = body.get("conexiones")
    start = body.get("start")
    end = body.get("end")
    filename_path = "dijkstra.png"

    try:
        G = Dijkstra(conexiones=conexiones)
        distances, parents = dijkstra(G, start)
        camino = obtener_camino(parents, end)
        draw_dijkstra(G, path=camino, filename=filename_path,
                      layout="circular")
        return FileResponse(filename_path, media_type="image/png")
    except Exception as e:
        print(e)


@app.get("/prim")
def get_prim():
    try:
        index_file_path = os.path.join("frontend/dist", "index.html")
        if os.path.exists(index_file_path):
            with open(index_file_path, "r") as file:
                return HTMLResponse(content=file.read(), status_code=200)
        else:
            return JSONResponse(content={"message": "index.html not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500)


@app.get("/dijkstra")
def get_dijkstra():
    try:
        index_file_path = os.path.join("frontend/dist", "index.html")
        if os.path.exists(index_file_path):
            with open(index_file_path, "r") as file:
                return HTMLResponse(content=file.read(), status_code=200)
        else:
            return JSONResponse(content={"message": "index.html not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500)


app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")


if __name__ == "__main__":
    try:
        subprocess.run(
            ["pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run(["npm", "install"], cwd="frontend", check=True)
        subprocess.run(["npm", "run", "build"], cwd="frontend", check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while building frontend: {e}")
        exit(1)
    run("main:app", port=4000, log_level="info", reload=True)
