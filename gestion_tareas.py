import sqlite3
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DB_FILE = "tareas.db"
JSON_FILE = "tareas.json"

# ------------------ Funciones de Base de Datos ------------------

def crear_tabla():
    """Crea la tabla de tareas si no existe."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            estado TEXT NOT NULL DEFAULT 'pendiente'
        )
        """)

def agregar_tarea(titulo, descripcion):
    """Agrega una nueva tarea."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tareas (titulo, descripcion) VALUES (?, ?)", (titulo, descripcion))
    messagebox.showinfo("Éxito", "Tarea agregada con éxito.")
    refrescar_lista()

def listar_tareas():
    """Lista todas las tareas desde la base de datos."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, descripcion, estado FROM tareas")
        tareas = cursor.fetchall()
    return tareas

def marcar_completada(id_tarea):
    """Marca una tarea como completada."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET estado = 'completada' WHERE id = ?", (id_tarea,))
    messagebox.showinfo("Éxito", f"Tarea {id_tarea} marcada como completada.")
    refrescar_lista()

def desmarcar_tarea(id_tarea):
    """Desmarca una tarea como completada."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET estado = 'pendiente' WHERE id = ?", (id_tarea,))
    messagebox.showinfo("Éxito", f"Tarea {id_tarea} desmarcada.")
    refrescar_lista()

def eliminar_tarea(id_tarea):
    """Elimina una tarea."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (id_tarea,))
    reiniciar_ids()
    messagebox.showinfo("Éxito", f"Tarea {id_tarea} eliminada.")
    refrescar_lista()

def reiniciar_ids():
    """Reinicia los IDs de las tareas."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("VACUUM")  #SQLite automáticamente reasigna los IDs

def exportar_tareas():
    """Exporta las tareas a un archivo JSON."""
    tareas = listar_tareas()
    tareas_dict = [
        {"id": tarea[0], "titulo": tarea[1], "descripcion": tarea[2], "estado": tarea[3]}
        for tarea in tareas
    ]
    with open(JSON_FILE, "w") as f:
        json.dump(tareas_dict, f, indent=4)
    messagebox.showinfo("Éxito", f"Tareas exportadas a {JSON_FILE}")

def importar_tareas():
    """Importa tareas desde un archivo JSON."""
    if not os.path.exists(JSON_FILE):
        messagebox.showerror("Error", "No se encontró el archivo JSON.")
        return
    with open(JSON_FILE, "r") as f:
        tareas = json.load(f)
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        for tarea in tareas:
            cursor.execute("INSERT OR IGNORE INTO tareas (id, titulo, descripcion, estado) VALUES (?, ?, ?, ?)",
                           (tarea["id"], tarea["titulo"], tarea["descripcion"], tarea["estado"]))
    messagebox.showinfo("Éxito", "Tareas importadas desde el archivo JSON.")
    refrescar_lista()

def refrescar_lista():
    """Refresca la lista de tareas en el Treeview."""
    for row in treeview.get_children():
        treeview.delete(row)
    tareas = listar_tareas()
    for tarea in tareas:
        treeview.insert("", "end", values=(tarea[0], tarea[1], tarea[2], tarea[3]))

def agregar_tarea_desde_gui():
    """Obtiene los datos del usuario y agrega una tarea."""
    titulo = entry_titulo.get()
    descripcion = entry_descripcion.get()
    if titulo.strip() == "":
        messagebox.showerror("Error", "El título no puede estar vacío.")
        return
    agregar_tarea(titulo, descripcion)
    entry_titulo.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)

# ------------------ Configuración de la Interfaz ------------------

crear_tabla()

root = tk.Tk()
root.title("Gestor de Tareas")

#Frame principal
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

#Entrada de datos
tk.Label(frame, text="Título:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_titulo = tk.Entry(frame, width=40)
entry_titulo.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Descripción:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_descripcion = tk.Entry(frame, width=40)
entry_descripcion.grid(row=1, column=1, padx=5, pady=5)

#Botones de agregar y gestión de datos
action_button_frame = tk.Frame(frame)
action_button_frame.grid(row=2, column=0, columnspan=2, pady=10)

tk.Button(action_button_frame, text="Agregar Tarea", width=15, command=agregar_tarea_desde_gui).grid(row=0, column=0, padx=10)
tk.Button(action_button_frame, text="Exportar Tareas", width=15, command=exportar_tareas).grid(row=0, column=1, padx=10)
tk.Button(action_button_frame, text="Importar Tareas", width=15, command=importar_tareas).grid(row=0, column=2, padx=10)

#Treeview para mostrar tareas
treeview = ttk.Treeview(frame, columns=("ID", "Título", "Descripción", "Estado"), show="headings", height=10)
treeview.grid(row=3, column=0, columnspan=2, pady=10)

treeview.heading("ID", text="ID")
treeview.heading("Título", text="Título")
treeview.heading("Descripción", text="Descripción")
treeview.heading("Estado", text="Estado")

treeview.column("ID", anchor="center", width=50)
treeview.column("Título", anchor="center", width=150)
treeview.column("Descripción", anchor="center", width=200)
treeview.column("Estado", anchor="center", width=100)

#Scrollbar
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
scrollbar.grid(row=3, column=2, sticky="ns")
treeview.configure(yscrollcommand=scrollbar.set)

#Botones para acciones específicas
action_button_frame2 = tk.Frame(frame)
action_button_frame2.grid(row=4, column=0, columnspan=2, pady=10)

tk.Button(action_button_frame2, text="Marcar Completada", width=20, command=lambda: marcar_completada(treeview.item(treeview.selection())["values"][0])).grid(row=0, column=0, padx=10)
tk.Button(action_button_frame2, text="Desmarcar", width=20, command=lambda: desmarcar_tarea(treeview.item(treeview.selection())["values"][0])).grid(row=0, column=1, padx=10)
tk.Button(action_button_frame2, text="Eliminar Tarea", width=20, command=lambda: eliminar_tarea(treeview.item(treeview.selection())["values"][0])).grid(row=0, column=2, padx=10)

# ------------------ Inicio del Programa ------------------
refrescar_lista()
root.mainloop()
