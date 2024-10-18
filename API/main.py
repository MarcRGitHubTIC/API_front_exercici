from csv import reader
#from datetime import datetime
import csv
import io
from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import List, Optional, Union
from fastapi.responses import JSONResponse
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
 
class aulaModel(BaseModel):
    idAula: Optional[int] = None 
    descAula: str
    building: str
    floor: int

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
    idAlumno: Optional[int] 
    idAula: int
    nameAlum: str
    cicle: str
    course: str
    group: str

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
    return [
        {
            "nameAlum": row[0],   
            "cicle": row[1],
            "course": row[2],     
            "group": row[3],     
            "descAula": row[4]  
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

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    if file.filename.endswith('.csv'):
        try:
            content = await file.read()
            decoded_content = content.decode('utf-8').splitlines()
            
            reader = csv.DictReader(decoded_content)
            
            aulasInsert = []
            alumnosInsert = []
            aulasExists = {}  
            alumnosExists = {}  
            
            for row in reader:
                try:
                    piso = int(row['Pis']) # Piso da por culo
                except ValueError:
                    raise HTTPException(status_code=400, detail=f"Error en la conversión de Pis: {row['Pis']} no es un número válido")
                
                desc_aula = row['DescAula'] 
                if desc_aula not in aulasExists:
                    aula = db_alumnos.get_aula_by_desc(desc_aula)
                    if aula is None:
                        aula_data = aulaModel(descAula=row['DescAula'], building=row['Edificio'], floor=piso)
                        aula_id = db_alumnos.create_aula(aula_data)
                        aulasInsert.append(aula_id)
                        aulasExists[desc_aula] = aula_id  
                    else:
                        aula_id = aula[0]  
                        aulasExists[desc_aula] = aula_id  
                else:
                    aula_id = aulasExists[desc_aula]  
                    
                nombre_alumno = row['NombreAlum']
                ciclo = row['Ciclo']
                curso = row['Curso']
                grupo = row['Grupo']
                
                alumno_clave = f"{nombre_alumno}-{ciclo}-{curso}-{grupo}"
                if alumno_clave not in alumnosExists:
                    alumno = db_alumnos.get_alumno_by_details(nombre_alumno, ciclo, curso, grupo)
                    if alumno is None:
                        alumno_id = db_alumnos.create(aula_id, nombre_alumno, ciclo, curso, grupo)
                        alumnosInsert.append(alumno_id)
                        alumnosExists[alumno_clave] = alumno_id 
                    else:
                        alumnosExists[alumno_clave] = alumno[0]  

                else:
                    continue  

            return JSONResponse(content={
                "message": "Datos cargados exitosamente.",
                "aulasInsert": aulasInsert,
                "alumnosInsert": alumnosInsert
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV.")
