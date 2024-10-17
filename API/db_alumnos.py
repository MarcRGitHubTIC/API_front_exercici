from client import db_client

"""def read():
    conn = db_client()
    if isinstance(conn, dict):
        print("Error de conexión: ", conn["message"])
        return conn  

    try:
        cur = conn.cursor()  
        cur.execute("SELECT a.NombreAlum, a.Ciclo, a.Curso, a.Grupo, aula.DescAula FROM alumno a JOIN aula ON a.IdAula = aula.IdAula")
        alumno = cur.fetchall()
        print(alumno)

    except Exception as e:
        print(f"Error en la consulta: {e}")  
        return {"status": -1, "message": f"Error en la consulta: {e}"}

    finally:
        if conn and hasattr(conn, "close"):  
            conn.close()

    return alumno"""

def read(orderby=None, contain=None, skip=0, limit=None):
    conn = db_client()
    if isinstance(conn, dict):
        return conn

    try:
        cur = conn.cursor()
        query = """
        SELECT a.NombreAlum, a.Ciclo, a.Curso, a.Grupo, aula.DescAula
        FROM alumno a
        JOIN aula ON a.IdAula = aula.IdAula
        """

        if contain:
            query += f" WHERE a.NombreAlum LIKE %s"
            values = [f"%{contain}%"]
        else:
            values = []

        if orderby in ["asc", "desc"]:
            query += f" ORDER BY a.NombreAlum {orderby.upper()}"

        if limit:
            query += f" LIMIT %s OFFSET %s"
            values.append(limit)
            values.append(skip)

        cur.execute(query, values)
        alumnos = cur.fetchall()

    except Exception as e:
        return {"status": -1, "message": f"Error en la consulta: {e}"}

    finally:
        if conn and hasattr(conn, "close"):
            conn.close()

    return alumnos

def read_id(id):
    conn = db_client()  
    if isinstance(conn, dict):  
        return conn

    try:
        cur = conn.cursor()
        query = "SELECT * FROM alumno WHERE IdAlumno = %s"  
        value = (id,)
        cur.execute(query, value)
    
        alumno = cur.fetchone() 

    except Exception as e:
        return {"status": -1, "message": f"Error de conexión: {e}"}
    
    finally:
        if conn and hasattr(conn, "close"):
            conn.close()
    
    return alumno

def create(idAula, nameAlum, cicle, course, group):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT INTO alumno (IdAula, NombreAlum, Ciclo, Curso, Grupo) VALUES (%s, %s, %s, %s, %s)"
        values = (idAula, nameAlum, cicle, course, group)
        cur.execute(query, values)
    
        conn.commit()
        alumno_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión: {e}" }
    
    finally:
        conn.close()

    return alumno_id

def update(id, idAula=None, nameAlum=None, cicle=None, course=None, group=None):
    try:
        conn = db_client()
        cur = conn.cursor()

        
        updates = []
        values = []

        if idAula is not None:
            updates.append("idAula = %s")
            values.append(idAula)

        if nameAlum is not None:
            updates.append("NombreAlum = %s")
            values.append(nameAlum)

        if cicle is not None:
            updates.append("Ciclo = %s")
            values.append(cicle)

        if course is not None:
            updates.append("Curso = %s")
            values.append(course)

        if group is not None:
            updates.append("Grupo = %s")
            values.append(group)

        
        values.append(id)

        query = f"UPDATE alumno SET {', '.join(updates)} WHERE idAlumno = %s"
        cur.execute(query, values)

        conn.commit()

    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    
    finally:
        conn.close()
    
    return {"status": 1, "message": "Alumno actualizado correctamente"}

def delete_alum(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM ALUMNO WHERE IdAlumno = %s;"  
        cur.execute(query, (id,))
        deleted_alum = cur.rowcount
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión: {e}"}
    
    finally:
        conn.close()
        
    return deleted_alum  

def show_all():
    conn = db_client()
    if isinstance(conn, dict):  
        print("Error de conexión: ", conn["message"])
        return conn

    try:
        cur = conn.cursor()  
        query = """
        SELECT 
        a.IdAlumno,
        a.IdAula,
        a.NombreAlum,
        a.Ciclo,
        a.Curso,
        a.Grupo,
        au.DescAula,
        au.Edificio,
        au.Pis
        FROM 
            alumno AS a
        JOIN 
            aula AS au ON a.IdAula = au.IdAula;
        """ 
        cur.execute(query)
        alumno = cur.fetchall()

    except Exception as e:
        return {"status": -1, "message": f"Error en la consulta: {e}"}

    finally:
        if conn and hasattr(conn, "close"):
            conn.close()

    return alumno 

