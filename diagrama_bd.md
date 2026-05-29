# Diagrama de la Base de Datos (Modelo Entidad-Relación)

Este diagrama representa la estructura de las tablas de la base de datos de la plataforma y sus relaciones.

```mermaid
erDiagram
    User ||--|| Perfil : "tiene un"
    User ||--o{ ProgresoCurso : "registra"
    User ||--o{ ProgresoSimulacion : "completa"
    User ||--o{ Perfil : "asocia empleado a empresa (empresa_id)"
    
    Curso ||--o{ ProgresoCurso : "pertenece"
    Curso ||--o{ ContenidoCurso : "contiene slides"
    Curso ||--o{ Pregunta : "tiene cuestionario"
    Curso ||--o{ MaterialCurso : "posee archivos"
    
    Pregunta ||--o{ Opcion : "tiene opciones de respuesta"
    
    Simulacion ||--o{ DesafioSimulacion : "contiene desafios"
    Simulacion ||--o{ ProgresoSimulacion : "pertenece"
    
    User {
        int id PK
        string username "CURP para empleados"
        string email
        string first_name
        string last_name
        boolean is_staff
        boolean is_active
    }

    Perfil {
        int id PK
        int usuario_id FK "OneToOne con User"
        int empresa_id FK "ForeignKey con User"
        string curp
        string rfc
        string nombre_empresa
        string telefono
        text notas
    }

    Curso {
        int id PK
        string titulo
        text descripcion
        int orden
        int puntos
        string icono
        file video
    }

    ContenidoCurso {
        int id PK
        int curso_id FK
        string titulo
        text texto
        file imagen
        int orden
    }

    Pregunta {
        int id PK
        int curso_id FK
        text texto
        int orden
    }

    Opcion {
        int id PK
        int pregunta_id FK
        string texto
        boolean es_correcta
    }

    MaterialCurso {
        int id PK
        int curso_id FK
        string nombre
        file archivo
    }

    ProgresoCurso {
        int id PK
        int usuario_id FK
        int curso_id FK
        string estado "bloqueado | disponible | en_curso | completado"
        int porcentaje
        int ultima_pagina "slide actual"
        datetime fecha_completado
    }

    Simulacion {
        int id PK
        string titulo
        text descripcion
        string icono
        int puntos
    }

    DesafioSimulacion {
        int id PK
        int simulacion_id FK
        file imagen
        text texto_complementario
        boolean es_peligro
        text explicacion
    }

    ProgresoSimulacion {
        int id PK
        int usuario_id FK
        int simulacion_id FK
        boolean completado
        int puntaje
        datetime fecha
    }

    AlertaSeguridad {
        int id PK
        string titulo
        text descripcion
        string nivel "alta | media | baja"
        datetime fecha
    }
```

---

## Descripción de las Relaciones Clave

1. **Usuarios y Perfiles (Multi-tenancy)**: 
   - La tabla `User` (nativo de Django) se extiende mediante `Perfil` (relación 1-a-1).
   - Un empleado tiene su perfil asociado a una empresa (`empresa_id` apunta al `User` de tipo Empresa), permitiendo la segmentación de datos.

2. **Cursos y Contenido**:
   - Cada `Curso` tiene un conjunto ordenado de diapositivas (`ContenidoCurso`), archivos multimedia (`MaterialCurso`) y un cuestionario final (`Pregunta` -> `Opcion`).

3. **Seguimiento de Progreso**:
   - `ProgresoCurso` y `ProgresoSimulacion` actúan como tablas relacionales que enlazan a los usuarios con su avance individual, guardando el estado, página actual y puntuaciones.
