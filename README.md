  # Gestor de Tareas
Este proyecto es una aplicación de escritorio construida en Python utilizando sqlite3 para el manejo de la base de datos, json para la exportación e importación de datos, y tkinter para la interfaz gráfica de usuario. Permite a los usuarios gestionar tareas de manera sencilla, incluyendo la creación, listado, edición, eliminación y exportación/importación de tareas.

## Características
 -CRUD de Tareas: Crear, leer, actualizar y eliminar tareas.

 -Gestión de Estado: Cambiar el estado de una tarea entre "pendiente" y "completada".

 -Persistencia Local: Almacenar datos en una base de datos SQLite.

 -Importación/Exportación: Exportar tareas a un archivo JSON e importarlas desde el mismo.

 -Interfaz Gráfica: Una interfaz de usuario interactiva creada con tkinter.

## Requisitos
 -Python 3.11 o superior

 -Módulos incluidos en la biblioteca estándar:
 
  -sqlite3
  
  -json
  
 -tkinter

 -os

## Instalación y Ejecución
1. Clona este repositorio o copia el archivo del proyecto.

2. Ejecuta el archivo principal:

        python gestor_tareas.py

3. Base de datos:
El programa creará automáticamente el archivo de base de datos tareas.db si no existe.

## Estructura del Proyecto

-Base de Datos SQLite:

Tabla tareas con las columnas:

    id (INTEGER, PRIMARY KEY)

    titulo (TEXT, NOT NULL)

    descripcion (TEXT)

    estado (TEXT, por defecto "pendiente")

-Archivo JSON:

Estructura de exportación/importación:

[

    {
        "id": 1,
        "titulo": "Tarea ejemplo",
        "descripcion": "Descripción de la tarea",
        "estado": "pendiente"
    }
]

## Uso
### Interfaz Principal

  Interfaz Principal

    -Agregar Tareas:

    -Rellena los campos "Título" y "Descripción".

    -Haz clic en "Agregar Tarea".

 Gestión de Tareas:

    -Selecciona una tarea en la tabla para:

    -Marcar como completada.

    -Desmarcar como pendiente.

    -Eliminarla.

  Exportar/Importar Tareas:

    -Haz clic en "Exportar Tareas" para guardar las tareas actuales en un archivo JSON.

    -Haz clic en "Importar Tareas" para cargar tareas desde un archivo JSON.


## Funciones Principales
### Base de Datos

    crear_tabla: Crea la tabla tareas en la base de datos.

    agregar_tarea: Inserta una nueva tarea.

    listar_tareas: Recupera todas las tareas.

    marcar_completada: Cambia el estado de una tarea a "completada".

    desmarcar_tarea: Cambia el estado de una tarea a "pendiente".

    eliminar_tarea: Elimina una tarea específica.

    reiniciar_ids: Optimiza la base de datos después de eliminar tareas.

### Importación/Exportación

    exportar_tareas: Guarda las tareas en un archivo JSON.

    importar_tareas: Carga tareas desde un archivo JSON.

### Interfaz de Usuario

    refrescar_lista: Actualiza el contenido de la tabla de tareas en la interfaz gráfica.

    agregar_tarea_desde_gui: Maneja la interacción del usuario para agregar tareas.


## Captura de Pantalla

![image](https://github.com/user-attachments/assets/9c4b5a56-3c06-482a-ac4e-292d748fb8a5)


## Licencia

Este proyecto es propiedad del autor y no puede ser utilizado, modificado ni distribuido sin el permiso explícito por escrito. Todos los derechos reservados.
