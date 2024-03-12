from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel

app = FastAPI()

class Noticias(BaseModel):
    contenido: str 
    categoria: str
    titulo: str
    autor: str 
    fecha: str 

db_noticias = []

# trayendo la base de datos 

@app.get("/noticias/")
async def noticias():
    return db_noticias

# Agregando noticias 
@app.post("/noticias/")
async def agregarNoticia(noticia : Noticias):
    db_noticias.append(noticia)
    return noticia