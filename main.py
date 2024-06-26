import os
import subprocess
from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.utils import prim, dijkstra, draw_dijkstra, draw_prim
from src.classes import Prim, Dijkstra, MaxFlow

# Si no existe la carpeta frontend/dist, la creamos
if not os.path.exists("frontend/dist"):
    os.makedirs("frontend/dist")

app = FastAPI()

app.add_middleware(CORSMiddleware)

app.add_middleware(
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


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

    if len(conexiones) == 0:
        return JSONResponse(content={"message": "Empty graph"}, status_code=400)

    G = Dijkstra(conexiones=conexiones)
    try:
        dist, path = dijkstra(G, start, end)
        print(f"Distancia desde {start} hasta {end}: {dist[end]}")
        print("Camino más corto:", path)
        draw_dijkstra(
            G, path=path, distance=dist[end], start=start, end=end, filename=filename_path)
        # draw_dijkstra(G, path=path, filename=filename_path)
    except ValueError as e:
        draw_dijkstra(G, filename=filename_path)
        print("Error:", e)

    if not os.path.exists(filename_path):
        raise HTTPException(
            status_code=500, detail="Error al crear la imagen.")

    return FileResponse(filename_path, media_type="image/png")


@app.post("/flujo-maximo")
async def max_flow_post(request: Request):
    body = await request.json()
    conexiones = body.get("conexiones")
    start = body.get("start")
    end = body.get("end")
    filename_path = "max_flow.png"
    try:
        G = MaxFlow(connections=conexiones)
        max_flow = G.FordFulkerson(start, end)
        # print(max_flow)
        G.graficar_grafo_residual(max_flow, filename=filename_path)
    except ValueError as e:
        print("Error:", e)
    if not os.path.exists(filename_path):
        raise HTTPException(
            status_code=500, detail="Error al crear la imagen.")
    return FileResponse(filename_path, media_type="image/png")


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


@app.get("/flujo-maximo")
def get_flujo_maximo():
    try:
        index_file_path = os.path.join("frontend/dist", "index.html")
        if os.path.exists(index_file_path):
            with open(index_file_path, "r") as file:
                return HTMLResponse(content=file.read(), status_code=200)
        else:
            return JSONResponse(content={"message": "index.html not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"message": "Internal Server Error"}, status_code=500)


app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="public")


@app.get("/{full_path:path}")
async def catch_all(request: Request, full_path: str):
    try:
        index_file_path = os.path.join("frontend", "dist", "index.html")
        return HTMLResponse(content=open(index_file_path).read(), status_code=200)
    except Exception as e:
        raise HTTPException(status_code=404, detail="File not found")


if __name__ == "__main__":
    PORT = os.getenv("PORT", 4000)
    ENV = os.getenv("ENV", "development")

    try:
        # subprocess.run(
        #     ["pip", "install", "-r", "requirements.txt"], check=True)
        subprocess.run(["npm", "install"], cwd="frontend", check=True)
        subprocess.run(["npm", "run", "build"], cwd="frontend", check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while building frontend: {e}")
        exit(1)
    if ENV == "development":
        run("main:app", host="127.0.0.1", port=int(
            PORT), log_level="info", reload=True)
    if ENV == "production":
        run("main:app", host="0.0.0.0", port=int(
            PORT), log_level="info", reload=True)
