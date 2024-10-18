document.addEventListener("DOMContentLoaded", async function() {
    const alumnesTableBody = document.querySelector("#tablaAlumne tbody");

    // Función para obtener datos de la API
    async function getData() {
        try {
            const response = await fetch("http://127.0.0.1:8000/alumno/list");
            
            if (!response.ok) {
                throw new Error("Error en la respuesta del servidor");
            }else{
                console.log("Error")
            }
            
            const data = await response.json();

                
            alumnesTableBody.innerHTML = "";

            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");
                
                //const IdAlumno = document.createElement("td");
                //IdAlumno.textContent = alumne.idAlumno; // Este .idAlumno debe ser igual que en el main/BaseModel usado para este trozo a.k.a alumno_model
                //row.appendChild(IdAlumno);

                //const IdAula = document.createElement("td");
                //IdAula.textContent = alumne.idAula; 
                //row.appendChild(IdAula);

                const NombreAlum = document.createElement("td");
                NombreAlum.textContent = alumne.nameAlum;  
                row.appendChild(NombreAlum);

                const Ciclo = document.createElement("td");
                Ciclo.textContent = alumne.cicle;  
                row.appendChild(Ciclo);

                const Curso = document.createElement("td");
                Curso.textContent = alumne.course;  
                row.appendChild(Curso);

                const Grupo = document.createElement("td");
                Grupo.textContent = alumne.group;  
                row.appendChild(Grupo);

                const DescAula = document.createElement("td");
                DescAula.textContent = alumne.descAula;  
                row.appendChild(DescAula);

                alumnesTableBody.appendChild(row);
            });
        } catch (error) {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        }
    }

    // Cridar la funció
    getData();
});
