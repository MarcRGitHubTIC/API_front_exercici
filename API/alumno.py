def alum_schema(alumno) -> dict:
    return {"IdAlumno": alumno[0],
            "IdAula": alumno[1],
            "NombreAlum": alumno[2],
            "Ciclo": alumno[3],
            "Curso": alumno[4],
            "Grupo": alumno[5],
            "CreatedAt": alumno[6],
            "UpdateAt": alumno[7] 
            }

def alumnos_schema(alumnos) -> dict:
    return [alum_schema(alumno) for alumno in alumnos]