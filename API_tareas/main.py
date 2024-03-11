from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Tareas(BaseModel):
    id: Optional[int] # el id opcional no me funciono por eso se implemento con la variable ultimo_id, incrementa el numero de id sin importar que escribamos en el body JSON
    tarea: str

db_fake = []
# Tareas(id=0, tarea="Hacer compras del mes"),
# Tareas(id=1, tarea="Corregir detalles de la reunion") con tareas o en este caso sin las tareas 

ultimo_id = len(db_fake) #definiendo el contador de ids

# listando las tareas
@app.get("/tarea/", status_code=200)
async def lista():
    if len(db_fake) == 0:
        return {"No tenes tareas agregadas"}
    
    return db_fake # retorna la db fake con toda la lista actual


# agregando tareas 
@app.post("/tarea/", response_model=Tareas, status_code=201)
async def agregarTarea(tarea: Tareas):
    global ultimo_id
    ultimo_id +=1
    tarea.id = ultimo_id 
    db_fake.append(tarea)
    return tarea
    
    
# actualizando tareas segun id 

@app.put("/tarea/", response_model=Tareas, status_code=200)
async def actualizarTarea(tarea: Tareas):
    found = False

    for index, saved_task in enumerate(db_fake):
        if saved_task.id == tarea.id:
            db_fake[index] = tarea
            found = True
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error, el id no existe")
    else:      
        return tarea
    
# Borrando tareas por id 

@app.delete("/tarea/{id}", status_code=200)        # usando query
async def borrarTarea(id: int):
    found = False
    for index, saved_task in enumerate(db_fake):
        if saved_task.id == id:
           del db_fake[index]
           found = True           
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="error, no se ha podido eliminar la tarea") 