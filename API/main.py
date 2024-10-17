from datetime import datetime
from sqlite3 import Timestamp
from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import db_alumnos
from alumno import alumnos_schema  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
class alumno_param(BaseModel):
    nameAlum: str
    cicle: str
    course: str
    group: str
    descAula:str
 
class ShowAllAlum(BaseModel):
    IdAlumno: int
    IdAula: int
    NombreAlum: str
    Ciclo: str
    Curso: str
    Grupo: str
    DescAula: str
    Edificio: str
    Pis: int

class UpdateAlumnoModel(BaseModel):
    idAula: Optional[int] = None
    nameAlum: Optional[str] = None
    cicle: Optional[str] = None 
    course: Optional[str] = None
    group: Optional[str] = None
    
class alumno_Model(BaseModel):
    idAlumno: int 
    idAula: int
    nameAlum: str
    cicle: str
    course: str
    group: str

class aulaModel(BaseModel):
    idAula: int
    descAula: str
    building: str
    floor: int
    createdAt: str
    updatedAt: str

@app.get("/")
def read_root():
    return {"alumno API Marc R"}

@app.get("/alumno/list", response_model=List[alumno_param])
def read_alumno(orderby: Optional[str] = None, contain: Optional[str] = None, skip: int = 0, limit: Optional[int] = None):
    alum_data = db_alumnos.read(orderby=orderby, contain=contain, skip=skip, limit=limit) 
    #alum_data=db_alumnos.read()

    
    if isinstance(alum_data, dict) and alum_data.get("status") == -1:
        raise HTTPException(status_code=500, detail=alum_data["message"])
    
    if alum_data is None:
        raise HTTPException(status_code=404, detail="Items not found")
    """
    response_data = []
    for alum in alum_data:
        response_data.append({
            "idAlumno":alum[0],
            "idAula": alum[1],
            "nameAlum": alum[2],
            "cicle": alum[3],
            "course": alum[4],
            "group": alum[5]
        })

    return response_data   
    """
    return [
        {
            "nameAlum": row[0],   # Assegura't que coincideixi amb el nom esperat
            "cicle": row[1],
            "course": row[2],     # Mapeja el camp 'curs' a 'course'
            "group": row[3],      # Mapeja el camp 'grup' a 'group'
            "descAula": str(row[4])  # Converteix a cadena si és necessari
        }
        for row in alum_data
    ]

@app.get("/alumno/show/{id}", response_model=alumno_Model)
def read_alum_id(id: int):
    alum_data = db_alumnos.read_id(id)

    if isinstance(alum_data, dict) and alum_data.get("status") == -1:
        raise HTTPException(status_code=500, detail=alum_data["message"])
    
    if alum_data is None:
        raise HTTPException(status_code=404, detail="Item not found")

    mapped_alum = {
        "idAlum": alum_data[0],
        "idAula": alum_data[1] if alum_data[1] is not None else 0,
        "nameAlum": alum_data[2],
        "cicle": alum_data[3],
        "course": str(alum_data[4]) if alum_data[4] is not None else "",
        "group": alum_data[5],
        "createdAt": alum_data[6].isoformat(),
        "updatedAt": alum_data[7].isoformat(),
    }

    return mapped_alum

@app.post("/alumno/create")
async def create_alum(data: alumno_Model):
    idAula = data.idAula
    nameAlum = data.nameAlum
    cicle = data.cicle
    course = data.course
    group = data.group  
    c_alum_create = db_alumnos.create(idAula, nameAlum, cicle, course, group)

    return {
        "msg": "Data successfully added to DB",
        "idAlumno": c_alum_create,
        "name": nameAlum
    }
    
@app.put("/alumno/update/{id}",response_model=dict)
async def update_alum(id: int, data: UpdateAlumnoModel):
    update_response = db_alumnos.update(
        id,
        idAula=data.idAula,
        nameAlum=data.nameAlum,
        cicle=data.cicle,
        course=data.course,
        group=data.group
    )

    if isinstance(update_response, dict) and update_response.get("status") == -1:
        raise HTTPException(status_code=500, detail=update_response["message"])
    return {"msg": "Alumno actualizado correctamente", "idAlumno": id}

@app.delete("/alumno/delete/{id}")
def delete_film(id: int):
    deleted_records = db_alumnos.delete_alum(id)
    if deleted_records == 0:
        raise HTTPException(status_code=404, detail="Items to delete not found") 

    return {"msg": "Alumno deleted successfully", "deleted_records": deleted_records}
   
@app.get("/alumno/listAll", response_model=list[ShowAllAlum])
async def list_all_alum():
    alum_data = db_alumnos.show_all()  

    if isinstance(alum_data, dict) and alum_data.get("status") == -1:
        raise HTTPException(status_code=500, detail=alum_data["message"])

    if alum_data is None or len(alum_data) == 0:
        raise HTTPException(status_code=404, detail="Items not found")

    response_data = [
        ShowAllAlum(
            IdAlumno=row[0],
            IdAula=row[1],
            NombreAlum=row[2],
            Ciclo=row[3],
            Curso=row[4],
            Grupo=row[5],
            DescAula=row[6],
            Edificio=row[7],
            Pis=row[8]
        )
        for row in alum_data
    ]
    
    return response_data

