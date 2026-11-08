import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import messagebox, simpledialog
from tkinter import ttk

from PIL import Image, ImageTk

from src.config_manager import load_config, save_config

from src.agenda import (
    agregar_contacto,
    buscar_contacto,
    modificar_contacto,
    campos,
    tamaño_registro,
    archivo_contactos,
    archivo_indice,
    archivo_hash
)
from src.exportaciones import exportar_json, exportar_pdf
from src.herramientas import (
    crear_respaldo,
    obtener_informacion_archivo,
    archivo_respaldo
)
from src.integridad import obtener_estado_integridad


config = {}

root = None
ventana_settings = None

entrada_nombre = None
combo_tema = None
combo_idioma = None
entrada_fuente = None

etiqueta_foto = None

barra_menu = None

color_barra = ""
foto_perfil = ""

imagen_perfil = None

panel_izquierdo = None
panel_derecho = None

boton_settings = None
boton_archivo = None
boton_edicion = None
boton_ver = None

etiqueta_usuario = None
etiqueta_nombre = None
etiqueta_bienvenida = None
etiqueta_descripcion = None

combo_elemento = None
spin_tamano = None
boton_color_texto = None
check_negrita = None
check_cursiva = None
boton_color_barra = None

elemento_seleccionado = "bienvenida"
color_texto_seleccionado = "#ffffff"


ESTILOS_DEFAULT = {
    "bienvenida": {
        "fuente": "Arial",
        "tamano": 19,
        "color": "#5865f2",
        "negrita": True,
        "cursiva": False
    },
    "descripcion": {
        "fuente": "Arial",
        "tamano": 11,
        "color": "#777f95",
        "negrita": False,
        "cursiva": False
    },
    "nombre_usuario": {
        "fuente": "Helvetica",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    },
    "configuracion": {
        "fuente": "Arial",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    },
    "archivo": {
        "fuente": "Arial",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    },
    "edicion": {
        "fuente": "Arial",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    },
    "ver": {
        "fuente": "Arial",
        "tamano": 10,
        "color": "#ffffff",
        "negrita": True,
        "cursiva": False
    }
}


class ToolTip:

    def __init__(self, widget, text, delay=500):

        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip = None
        self._job = None

        widget.bind(
            "<Enter>",
            self._schedule,
            add="+"
        )

        widget.bind(
            "<Leave>",
            self._hide,
            add="+"
        )

        widget.bind(
            "<ButtonPress>",
            self._hide,
            add="+"
        )

    def _schedule(self, _event=None):

        self._cancel()

        self._job = self.widget.after(
            self.delay,
            self._show
        )

    def _cancel(self):

        if self._job is not None:

            self.widget.after_cancel(
                self._job
            )

            self._job = None

    def _show(self):

        if self.tip is not None:
            return

        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6

        self.tip = tk.Toplevel(self.widget)

        self.tip.wm_overrideredirect(True)
        self.tip.wm_geometry(f"+{x}+{y}")

        tk.Label(
            self.tip,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padx=6,
            pady=3
        ).pack()

    def _hide(self, _event=None):

        self._cancel()

        if self.tip is not None:

            self.tip.destroy()
            self.tip = None


def obtener_texto(clave):

    if config["idioma"] == "en-US":

        textos = {
            "titulo": "Welcome!",
            "usuario": "User: ",
            "configuracion": "Settings",
            "nombre": "Username:",
            "tema": "Theme:",
            "idioma": "Language:",
            "fuente": "Font size:",
            "color_barra": "Menu bar color:",
            "color_letra": "Text color:",
            "foto": "Profile photo:",
            "seleccionar_foto": "Select picture",
            "guardar": "Save configuration",
            "claro": "light",
            "oscuro": "dark",
            "descripcion": "With this application you can manage your settings and customize your experience",
            "archivo": "Contacts",
            "edicion": "Export",
            "ver": "Tools",
            "personalizacion": "Text customization",
            "elemento": "Element:",
            "tamano": "Size:",
            "color": "Text color:",
            "negrita": "Bold",
            "cursiva": "Italic",
            "aplicar": "Apply style",
            "bienvenida": "Welcome text",
            "descripcion_elemento": "Description",
            "nombre_elemento": "Username",
            "configuracion_elemento": "Settings button",
            "archivo_elemento": "Contacts button",
            "edicion_elemento": "Export button",
            "ver_elemento": "Tools button",
            "error": "Error",

            "agregar": "Add contact",
            "buscar": "Search by ID",
            "modificar": "Modify contact",
            "exportar_json": "Export to JSON",
            "exportar_pdf": "Export to PDF",
            "salir": "Exit",
            "verificar": "Verify integrity",
            "respaldo": "Create ZIP backup",
            "informacion": "File information",
            "ayuda": "Help",
            "datos_contacto": "Contact information",
            "campo_id": "ID",
            "campo_nombre": "Name",
            "campo_telefono": "Phone",
            "campo_email": "Email",
            "campo_ciudad": "City",
            "guardar_contacto": "Save",
            "datos_incompletos": "Incomplete information",
            "completar_campos": "Please complete all fields.",
            "campo_largo": "Field too long",
            "id_largo": "ID too long",
            "agenda": "Contacts",
            "guardado": "The contact was saved successfully.",
            "modificado": "The contact was modified successfully.",
            "posicion": "Record position",
            "error_guardar": "Could not save the contact.",
            "buscar_contacto": "Search contact",
            "ingresar_id": "Enter the contact ID:",
            "contacto_encontrado": "Contact found",
            "busqueda": "Search",
            "exportacion_json": "JSON export",
            "exportacion_pdf": "PDF export",
            "json_correcto": "Contacts were exported successfully.",
            "pdf_correcto": "The PDF was generated successfully.",
            "archivo_texto": "File",
            "integridad": "Integrity",
            "advertencia_integridad": "WARNING: An integrity issue was detected.",
            "integridad_correcta": "The integrity check was completed successfully.",
            "error_integridad": "Could not verify data integrity.",
            "respaldo_zip": "ZIP backup",
            "respaldo_correcto": "The backup was created successfully.",
            "tamano_original": "Original size",
            "tamano_comprimido": "Compressed size",
            "informacion_archivos": "File information",
            "ultima_modificacion": "Last modified",
            "lectura": "Read access",
            "escritura": "Write access",
            "si": "Yes",
            "no": "No",
            "ayuda_titulo": "Random-access contact manager",
            "ayuda_descripcion": (
                "You can add, search for, and modify contacts using their ID. "
                "You can also export the contact list to JSON or PDF, verify "
                "data integrity, and create ZIP backups."
            ),
            "tamano_registro": "Record size",
            "tamano_campos": "Field sizes",
            "bytes": "bytes",
            "error": "Error",
        }

    else:

        textos = {
            "titulo": "¡Bienvenido!",
            "usuario": "Usuario: ",
            "configuracion": "Configuración",
            "nombre": "Nombre de usuario:",
            "tema": "Tema:",
            "idioma": "Idioma:",
            "fuente": "Tamaño de fuente:",
            "color_barra": "Color de barra de menú:",
            "color_letra": "Color de letra:",
            "foto": "Foto de perfil:",
            "seleccionar_foto": "Seleccionar foto",
            "guardar": "Guardar configuración",
            "claro": "claro",
            "oscuro": "oscuro",
            "descripcion": "Con esta aplicación puedes gestionar tu configuración y personalizar tu experiencia",
            "archivo": "Contactos",
            "edicion": "Exportar",
            "ver": "Herramientas",
            "personalizacion": "Personalización de textos",
            "elemento": "Elemento:",
            "tamano": "Tamaño:",
            "color": "Color de texto:",
            "negrita": "Negrita",
            "cursiva": "Cursiva",
            "aplicar": "Aplicar estilo",
            "bienvenida": "Texto de bienvenida",
            "descripcion_elemento": "Descripción",
            "nombre_elemento": "Nombre de usuario",
            "configuracion_elemento": "Botón Configuración",
            "archivo_elemento": "Botón Contactos",
            "edicion_elemento": "Botón Exportar",
            "ver_elemento": "Botón Herramientas",

            "agregar": "Agregar contacto",
            "buscar": "Buscar por ID",
            "modificar": "Modificar contacto",
            "exportar_json": "Exportar a JSON",
            "exportar_pdf": "Exportar a PDF",
            "salir": "Salir",
            "verificar": "Verificar integridad",
            "respaldo": "Crear respaldo ZIP",
            "informacion": "Información de archivos",
            "ayuda": "Ayuda",
            "datos_contacto": "Datos del contacto",
            "campo_id": "ID",
            "campo_nombre": "Nombre",
            "campo_telefono": "Teléfono",
            "campo_email": "Correo electrónico",
            "campo_ciudad": "Ciudad",
            "guardar_contacto": "Guardar",
            "datos_incompletos": "Datos incompletos",
            "completar_campos": "Completa todos los campos.",
            "campo_largo": "Campo demasiado largo",
            "id_largo": "ID demasiado largo",
            "agenda": "Agenda",
            "guardado": "El contacto se guardó correctamente.",
            "modificado": "El contacto se modificó correctamente.",
            "posicion": "Posición del registro",
            "error_guardar": "No se pudo guardar el contacto.",
            "buscar_contacto": "Buscar contacto",
            "ingresar_id": "Ingresa el ID del contacto:",
            "contacto_encontrado": "Contacto encontrado",
            "busqueda": "Búsqueda",
            "exportacion_json": "Exportación JSON",
            "exportacion_pdf": "Exportación PDF",
            "json_correcto": "Los contactos se exportaron correctamente.",
            "pdf_correcto": "El PDF se generó correctamente.",
            "archivo_texto": "Archivo",
            "integridad": "Integridad",
            "advertencia_integridad": "ADVERTENCIA: Se detectó un problema de integridad.",
            "integridad_correcta": "La comprobación de integridad finalizó correctamente.",
            "error_integridad": "No se pudo comprobar la integridad.",
            "respaldo_zip": "Respaldo ZIP",
            "respaldo_correcto": "El respaldo se creó correctamente.",
            "tamano_original": "Tamaño original",
            "tamano_comprimido": "Tamaño comprimido",
            "informacion_archivos": "Información de archivos",
            "ultima_modificacion": "Última modificación",
            "lectura": "Lectura",
            "escritura": "Escritura",
            "si": "Sí",
            "no": "No",
            "ayuda_titulo": "Agenda de contactos con acceso aleatorio",
            "ayuda_descripcion": (
                "Puedes agregar, buscar y modificar contactos mediante su ID. "
                "También puedes exportar la agenda a JSON o PDF, comprobar la "
                "integridad de los datos y crear respaldos ZIP."
            ),
            "tamano_registro": "Tamaño de cada registro",
            "tamano_campos": "Tamaño de los campos",
            "bytes": "bytes",
            "error": "Error"
        }

    return textos[clave]


def obtener_estilos():

    if "estilos_textos" not in config:

        config["estilos_textos"] = {}

    for clave, estilo in ESTILOS_DEFAULT.items():

        if clave not in config["estilos_textos"]:

            config["estilos_textos"][clave] = estilo.copy()

        else:

            for propiedad, valor in estilo.items():

                if propiedad not in config["estilos_textos"][clave]:

                    config["estilos_textos"][clave][propiedad] = valor

    return config["estilos_textos"]


def crear_fuente(elemento):

    estilos = obtener_estilos()
    estilo = estilos[elemento]

    tipo = estilo["fuente"]
    tamano = estilo["tamano"]

    if estilo["negrita"] and estilo["cursiva"]:

        tipo_estilo = "bold italic"

    elif estilo["negrita"]:

        tipo_estilo = "bold"

    elif estilo["cursiva"]:

        tipo_estilo = "italic"

    else:

        tipo_estilo = "normal"

    return (
        tipo,
        tamano,
        tipo_estilo
    )


def aplicar_estilo_widget(widget, elemento):

    estilos = obtener_estilos()
    estilo = estilos[elemento]

    widget.configure(
        font=crear_fuente(elemento),
        fg=estilo["color"]
    )


def cargar_foto_perfil():

    global imagen_perfil

    if foto_perfil:

        try:

            imagen = Image.open(foto_perfil)
            imagen = imagen.resize((60, 60))

            imagen_perfil = ImageTk.PhotoImage(imagen)

            etiqueta_usuario.configure(
                image=imagen_perfil,
                text=""
            )

            return

        except Exception:
            pass

    try:

        imagen = Image.open("image.png")
        imagen = imagen.resize((60, 60))

        imagen_perfil = ImageTk.PhotoImage(imagen)

        etiqueta_usuario.configure(
            image=imagen_perfil,
            text=""
        )

    except Exception:

        etiqueta_usuario.configure(
            image="",
            text="👤",
            font=("Arial", 25)
        )


def aplicar_configuracion():

    estilos = obtener_estilos()

    if config["tema_interfaz"] == "oscuro":

        color_fondo = "#222222"

    else:

        color_fondo = "#ffffff"

    panel_derecho.configure(
        bg=color_fondo
    )

    panel_izquierdo.configure(
        bg=color_barra
    )

    etiqueta_usuario.configure(
        bg=color_barra
    )

    etiqueta_nombre.configure(
        bg=color_barra
    )

    etiqueta_bienvenida.configure(
        bg=color_fondo
    )

    etiqueta_descripcion.configure(
        bg=color_fondo
    )

    boton_settings.configure(
        bg=color_barra,
        activebackground=color_barra
    )

    boton_archivo.configure(
        bg=color_barra,
        activebackground=color_barra
    )

    boton_edicion.configure(
        bg=color_barra,
        activebackground=color_barra
    )

    boton_ver.configure(
        bg=color_barra,
        activebackground=color_barra
    )

    aplicar_estilo_widget(
        etiqueta_bienvenida,
        "bienvenida"
    )

    aplicar_estilo_widget(
        etiqueta_descripcion,
        "descripcion"
    )

    aplicar_estilo_widget(
        etiqueta_nombre,
        "nombre_usuario"
    )

    aplicar_estilo_widget(
        boton_settings,
        "configuracion"
    )

    aplicar_estilo_widget(
        boton_archivo,
        "archivo"
    )

    aplicar_estilo_widget(
        boton_edicion,
        "edicion"
    )

    aplicar_estilo_widget(
        boton_ver,
        "ver"
    )


def actualizar_textos():

    etiqueta_bienvenida.configure(
        text=obtener_texto("titulo")
    )

    etiqueta_nombre.configure(
        text=config["nombre_usuario"]
    )

    etiqueta_descripcion.configure(
        text=obtener_texto("descripcion")
    )

    boton_settings.configure(
        text=obtener_texto("configuracion")
    )

    boton_archivo.configure(
        text=obtener_texto("archivo")
    )

    boton_edicion.configure(
        text=obtener_texto("edicion")
    )

    boton_ver.configure(
        text=obtener_texto("ver")
    )


def guardar_configuracion():
    global config

    try:
        # Guardar los datos generales
        config["nombre_usuario"] = entrada_nombre.get()
        config["tema_interfaz"] = combo_tema.get()
        config["idioma"] = combo_idioma.get()
        config["color_barra_menu"] = color_barra
        config["foto_perfil"] = foto_perfil

        # Guardar el estilo que se esté editando actualmente
        guardar_estilo_actual()

        # Guardar todos los cambios en el archivo JSON
        save_config(config)

        # Aplicar los cambios a la ventana principal
        aplicar_configuracion()
        actualizar_textos()
        cargar_foto_perfil()

        messagebox.showinfo(
            "Configuración",
            "Todos los cambios se guardaron correctamente."
        )

        cerrar_settings()

    except ValueError:
        messagebox.showerror(
            "Error",
            "Verifica que los valores ingresados sean correctos."
        )

    except tk.TclError:
        messagebox.showerror(
            "Error",
            "La ventana de configuración ya no está disponible."
        )

def seleccionar_color_barra():

    global color_barra

    resultado = colorchooser.askcolor(
        title="Seleccionar color de barra"
    )

    if resultado[1]:

        color_barra = resultado[1]

        barra_menu.configure(
            background=color_barra
        )

        aplicar_configuracion()


def seleccionar_color_texto():

    global color_texto_seleccionado

    resultado = colorchooser.askcolor(
        title="Seleccionar color de texto"
    )

    if resultado[1]:

        color_texto_seleccionado = resultado[1]

        boton_color_texto.configure(
            bg=color_texto_seleccionado
        )


def seleccionar_foto():

    global foto_perfil

    ruta = filedialog.askopenfilename(
        title="Seleccionar foto de perfil",
        filetypes=[
            ("Imagenes", "*.png *.gif"),
            ("Todos los archivos", "*.*")
        ]
    )

    if ruta:

        foto_perfil = ruta

        if etiqueta_foto is not None:

            try:

                if etiqueta_foto.winfo_exists():

                    etiqueta_foto.configure(
                        text="Foto seleccionada:\n" + ruta
                    )

            except tk.TclError:

                pass


def actualizar_tema():
    tema = combo_tema.get()

    if tema == "oscuro":
        config["color_fondo"] = "#202124"
        config["color_panel"] = "#292a2d"
        config["color_tarjeta"] = "#303134"
    else:
        config["color_fondo"] = "#f4f6fb"
        config["color_panel"] = "#ffffff"
        config["color_tarjeta"] = "#ffffff"

    aplicar_configuracion()

def nombres_elementos():

    return [
        obtener_texto("bienvenida"),
        obtener_texto("descripcion_elemento"),
        obtener_texto("nombre_elemento"),
        obtener_texto("configuracion_elemento"),
        obtener_texto("archivo_elemento"),
        obtener_texto("edicion_elemento"),
        obtener_texto("ver_elemento")
    ]


def claves_elementos():

    return [
        "bienvenida",
        "descripcion",
        "nombre_usuario",
        "configuracion",
        "archivo",
        "edicion",
        "ver"
    ]


def cargar_estilo_seleccionado():

    global elemento_seleccionado
    global color_texto_seleccionado

    posicion = combo_elemento.current()

    if posicion < 0:
        return

    elemento_seleccionado = claves_elementos()[posicion]

    estilo = obtener_estilos()[elemento_seleccionado]

    spin_tamano.delete(
        0,
        "end"
    )

    spin_tamano.insert(
        0,
        estilo["tamano"]
    )

    color_texto_seleccionado = estilo["color"]

    boton_color_texto.configure(
        bg=color_texto_seleccionado
    )

    check_negrita.set(
        estilo["negrita"]
    )

    check_cursiva.set(
        estilo["cursiva"]
    )


def guardar_estilo_actual():

    if combo_elemento is None:
        return

    try:

        tamano = int(spin_tamano.get())

    except ValueError:

        return

    estilos = obtener_estilos()

    estilos[elemento_seleccionado]["tamano"] = tamano
    estilos[elemento_seleccionado]["color"] = color_texto_seleccionado
    estilos[elemento_seleccionado]["negrita"] = check_negrita.get()
    estilos[elemento_seleccionado]["cursiva"] = check_cursiva.get()


def aplicar_estilo_seleccionado():

    guardar_estilo_actual()

    aplicar_configuracion()

    messagebox.showinfo(
        "Configuración",
        "El estilo se aplicó correctamente."
    )

def cerrar_settings():

    global ventana_settings

    if ventana_settings is not None:

        ventana_settings.grab_release()
        ventana_settings.destroy()
        ventana_settings = None
        

def mostrar_settings():

    global ventana_settings
    global entrada_nombre
    global combo_tema
    global combo_idioma
    global entrada_fuente
    global etiqueta_foto
    global boton_color_barra

    global combo_elemento
    global spin_tamano
    global boton_color_texto
    global check_negrita
    global check_cursiva

    if ventana_settings is not None:

        if ventana_settings.winfo_exists():

            ventana_settings.lift()
            ventana_settings.focus_force()

            return

    ventana_settings = tk.Toplevel(root)

    ventana_settings.transient(root)
    ventana_settings.grab_set()

    ventana_settings.protocol(
        "WM_DELETE_WINDOW",
        cerrar_settings
    )

    ventana_settings.title(
        obtener_texto("configuracion")
    )

    # Mismo ancho que la ventana principal
    ventana_settings.geometry("520x520")
    ventana_settings.resizable(False, False)

    if config["tema_interfaz"] == "oscuro":

        color_fondo = "#222222"
        color_texto = "#ffffff"

    else:

        color_fondo = "#ffffff"
        color_texto = "#000000"

    ventana_settings.configure(
        bg=color_fondo
    )

    # titulo de la ventana de configuración

    tk.Label(
        ventana_settings,
        text=obtener_texto("configuracion"),
        font=("Arial", 20, "bold"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(18, 12)
    )

    # contenedor principal

    marco_principal = tk.Frame(
        ventana_settings,
        bg=color_fondo
    )

    marco_principal.pack(
        fill="x",
        padx=25
    )

    columna_izquierda = tk.Frame(
        marco_principal,
        bg=color_fondo
    )

    columna_izquierda.grid(
        row=0,
        column=0,
        padx=(0, 15),
        sticky="n"
    )

    columna_derecha = tk.Frame(
        marco_principal,
        bg=color_fondo
    )

    columna_derecha.grid(
        row=0,
        column=1,
        padx=(15, 0),
        sticky="n"
    )

    # CONFIGURACION GENERAL

    tk.Label(
        columna_izquierda,
        text=obtener_texto("nombre"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(5, 2)
    )

    entrada_nombre = tk.Entry(
        columna_izquierda,
        width=22
    )

    entrada_nombre.insert(
        0,
        config["nombre_usuario"]
    )

    entrada_nombre.pack(
        pady=4
    )

    # tema (claro u oscuro)

    tk.Label(
        columna_izquierda,
        text=obtener_texto("tema"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(8, 2)
    )

    combo_tema = ttk.Combobox(
        columna_izquierda,
        values=["claro", "oscuro"],
        state="readonly",
        width=19
    )

    combo_tema.set(
        config["tema_interfaz"]
    )

    combo_tema.pack()

    combo_tema.bind(
        "<<ComboboxSelected>>",
        lambda evento: actualizar_tema()
    )

    # cambiar idioma

    tk.Label(
        columna_izquierda,
        text=obtener_texto("idioma"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(8, 2)
    )

    combo_idioma = ttk.Combobox(
        columna_izquierda,
        values=["es-ES", "en-US"],
        state="readonly",
        width=19
    )

    combo_idioma.set(
        config["idioma"]
    )

    combo_idioma.pack()

    # personalizar color de la barra de menú

    tk.Label(
        columna_izquierda,
        text=obtener_texto("color_barra"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(10, 2)
    )

    boton_color_barra = tk.Button(
        columna_izquierda,
        text="      ",
        bg=color_barra,
        width=19,
        command=seleccionar_color_barra
    )

    boton_color_barra.pack(
        pady=4
    )

    # escoger foto de perfil

    tk.Label(
        columna_izquierda,
        text=obtener_texto("foto"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(10, 2)
    )

    if foto_perfil:

        texto_foto = (
            "Foto seleccionada:\n"
            + foto_perfil
        )

    else:

        texto_foto = (
            "No se ha seleccionado una foto"
        )

    etiqueta_foto = tk.Label(
        columna_izquierda,
        text=texto_foto,
        wraplength=180,
        bg=color_fondo,
        fg=color_texto
    )

    etiqueta_foto.pack(
        pady=4
    )

    tk.Button(
        columna_izquierda,
        text=obtener_texto("seleccionar_foto"),
        command=seleccionar_foto,
        width=19
    ).pack(
        pady=4
    )

    # Personalización de textos

    tk.Label(
        columna_derecha,
        text=obtener_texto("personalizacion"),
        font=("Arial", 14, "bold"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(5, 12)
    )

    # elementos de la combo box

    tk.Label(
        columna_derecha,
        text=obtener_texto("elemento"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=2
    )

    combo_elemento = ttk.Combobox(
        columna_derecha,
        values=nombres_elementos(),
        state="readonly",
        width=19
    )

    combo_elemento.pack(
        pady=4
    )

    combo_elemento.current(0)

    combo_elemento.bind(
        "<<ComboboxSelected>>",
        lambda evento: cargar_estilo_seleccionado()
    )

    # tamaño de fuente

    tk.Label(
        columna_derecha,
        text=obtener_texto("tamano"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(8, 2)
    )

    spin_tamano = tk.Spinbox(
        columna_derecha,
        from_=8,
        to=40,
        width=8
    )

    spin_tamano.pack(
        pady=4
    )

    # cambiar color del texto

    tk.Label(
        columna_derecha,
        text=obtener_texto("color"),
        bg=color_fondo,
        fg=color_texto
    ).pack(
        pady=(8, 2)
    )

    boton_color_texto = tk.Button(
        columna_derecha,
        text="      ",
        bg="#ffffff",
        width=10,
        command=seleccionar_color_texto
    )

    boton_color_texto.pack(
        pady=4
    )

    # negrita

    check_negrita = tk.BooleanVar()

    tk.Checkbutton(
        columna_derecha,
        text=obtener_texto("negrita"),
        variable=check_negrita,
        bg=color_fondo,
        fg=color_texto,
        selectcolor=color_fondo,
        activebackground=color_fondo,
        activeforeground=color_texto
    ).pack(
        pady=(8, 2)
    )

    #cursiva

    check_cursiva = tk.BooleanVar()

    tk.Checkbutton(
        columna_derecha,
        text=obtener_texto("cursiva"),
        variable=check_cursiva,
        bg=color_fondo,
        fg=color_texto,
        selectcolor=color_fondo,
        activebackground=color_fondo,
        activeforeground=color_texto
    ).pack(
        pady=2
    )

    #Aplicar estilo seleccionado

    tk.Button(
        columna_derecha,
        text=obtener_texto("aplicar"),
        command=aplicar_estilo_seleccionado,
        width=19
    ).pack(
        pady=12
    )

    cargar_estilo_seleccionado()

    
    # Guradar configuración
    

    tk.Button(
        ventana_settings,
        text=obtener_texto("guardar"),
        command=guardar_configuracion,
        width=28
    ).pack(
        pady=(12, 18)
    )



def colores_ventana():
    if config.get("tema_interfaz") == "oscuro":
        return "#222222", "#ffffff"

    return "#ffffff", "#222222"


def mostrar_formulario_contacto(contacto=None):

    nuevo = contacto is None
    fondo, texto = colores_ventana()

    ventana = tk.Toplevel(root)
    ventana.title(
        obtener_texto("agregar") if nuevo
        else obtener_texto("modificar")
    )
    ventana.geometry("420x390")
    ventana.resizable(False, False)
    ventana.configure(bg=fondo)
    ventana.transient(root)
    ventana.grab_set()

    tk.Label(
        ventana,
        text=obtener_texto("datos_contacto"),
        bg=fondo,
        fg=texto,
        font=("Arial", 14, "bold")
    ).pack(pady=(18, 12))

    campos_formulario = [
        ("id", "campo_id"),
        ("nombre", "campo_nombre"),
        ("telefono", "campo_telefono"),
        ("email", "campo_email"),
        ("ciudad", "campo_ciudad")
    ]

    entradas = {}

    marco = tk.Frame(ventana, bg=fondo)
    marco.pack(fill="x", padx=28)

    for clave, clave_texto in campos_formulario:

        fila = tk.Frame(marco, bg=fondo)
        fila.pack(fill="x", pady=5)

        tk.Label(
            fila,
            text=obtener_texto(clave_texto),
            bg=fondo,
            fg=texto,
            width=16,
            anchor="w"
        ).pack(side="left")

        entrada = tk.Entry(fila, width=29)
        entrada.pack(side="left", fill="x", expand=True)

        if contacto is not None:
            entrada.insert(0, str(contacto[clave]))

        if clave == "id" and not nuevo:
            entrada.configure(state="disabled")

        entradas[clave] = entrada

    def guardar():

        valores = {}

        for clave, entrada in entradas.items():

            if clave == "id" and not nuevo:
                valores[clave] = str(contacto["id"])
            else:
                valores[clave] = entrada.get().strip()

        if any(not valor for valor in valores.values()):

            messagebox.showwarning(
                obtener_texto("datos_incompletos"),
                obtener_texto("completar_campos"),
                parent=ventana
            )
            return

        try:

            valores["id"] = int(valores["id"])

            nombres_campos = {
                "nombre": obtener_texto("campo_nombre"),
                "telefono": obtener_texto("campo_telefono"),
                "email": obtener_texto("campo_email"),
                "ciudad": obtener_texto("campo_ciudad")
            }

            for clave in ("nombre", "telefono", "email", "ciudad"):

                if len(valores[clave].encode("utf-8")) > campos[clave]:

                    messagebox.showwarning(
                        obtener_texto("campo_largo"),
                        f"{nombres_campos[clave]}: "
                        f"{campos[clave]} {obtener_texto('bytes')} "
                        f"(UTF-8).",
                        parent=ventana
                    )
                    return

            if len(str(valores["id"]).encode("utf-8")) > campos["id"]:

                messagebox.showwarning(
                    obtener_texto("id_largo"),
                    f"{obtener_texto('campo_id')}: "
                    f"{campos['id']} {obtener_texto('bytes')}.",
                    parent=ventana
                )
                return

            if nuevo:

                posicion = agregar_contacto(valores)
                mensaje = obtener_texto("guardado")

            else:

                posicion = modificar_contacto(
                    valores["id"],
                    {
                        "nombre": valores["nombre"],
                        "telefono": valores["telefono"],
                        "email": valores["email"],
                        "ciudad": valores["ciudad"]
                    }
                )

                mensaje = obtener_texto("modificado")

            mensaje += (
                f"\n{obtener_texto('posicion')}: {posicion}"
            )

            messagebox.showinfo(
                obtener_texto("agenda"),
                mensaje,
                parent=ventana
            )

            ventana.destroy()

        except ValueError as error:

            messagebox.showerror(
                obtener_texto("error_guardar"),
                str(error),
                parent=ventana
            )

        except (OSError, KeyError) as error:

            messagebox.showerror(
                obtener_texto("error"),
                f"{obtener_texto('error_guardar')}\n{error}",
                parent=ventana
            )

    tk.Button(
        ventana,
        text=obtener_texto("guardar_contacto"),
        command=guardar,
        width=16,
        cursor="hand2"
    ).pack(pady=20)


def agregar_contacto_ui():

    mostrar_formulario_contacto()


def buscar_contacto_ui():

    identificador = simpledialog.askinteger(
        obtener_texto("buscar_contacto"),
        obtener_texto("ingresar_id"),
        parent=root,
        minvalue=0
    )

    if identificador is None:
        return

    try:

        contacto, posicion = buscar_contacto(identificador)

        detalle = (
            f"{obtener_texto('campo_id')}: {contacto['id']}\n"
            f"{obtener_texto('campo_nombre')}: {contacto['nombre']}\n"
            f"{obtener_texto('campo_telefono')}: {contacto['telefono']}\n"
            f"{obtener_texto('campo_email')}: {contacto['email']}\n"
            f"{obtener_texto('campo_ciudad')}: {contacto['ciudad']}\n\n"
            f"{obtener_texto('posicion')}: {posicion}"
        )

        messagebox.showinfo(
            obtener_texto("contacto_encontrado"),
            detalle,
            parent=root
        )

    except (ValueError, OSError) as error:

        messagebox.showerror(
            obtener_texto("busqueda"),
            str(error),
            parent=root
        )


def modificar_contacto_ui():

    identificador = simpledialog.askinteger(
        obtener_texto("modificar"),
        obtener_texto("ingresar_id"),
        parent=root,
        minvalue=0
    )

    if identificador is None:
        return

    try:

        contacto, posicion = buscar_contacto(identificador)
        mostrar_formulario_contacto(contacto)

    except (ValueError, OSError) as error:

        messagebox.showerror(
            obtener_texto("modificar"),
            str(error),
            parent=root
        )


def exportar_json_ui():

    try:

        ruta = exportar_json()

        messagebox.showinfo(
            obtener_texto("exportacion_json"),
            f"{obtener_texto('json_correcto')}\n\n"
            f"{obtener_texto('archivo_texto')}:\n{ruta}",
            parent=root
        )

    except (ValueError, OSError, KeyError) as error:

        messagebox.showerror(
            obtener_texto("exportacion_json"),
            str(error),
            parent=root
        )


def exportar_pdf_ui():

    try:

        ruta = exportar_pdf()

        messagebox.showinfo(
            obtener_texto("exportacion_pdf"),
            f"{obtener_texto('pdf_correcto')}\n\n"
            f"{obtener_texto('archivo_texto')}:\n{ruta}",
            parent=root
        )

    except (ValueError, OSError, KeyError) as error:

        messagebox.showerror(
            obtener_texto("exportacion_pdf"),
            str(error),
            parent=root
        )


def verificar_integridad_ui():

    try:

        estado = obtener_estado_integridad()

        if estado.startswith("ADVERTENCIA"):

            mensaje = obtener_texto("advertencia_integridad")

            messagebox.showwarning(
                obtener_texto("integridad"),
                mensaje,
                parent=root
            )

        else:

            mensaje = obtener_texto("integridad_correcta")

            messagebox.showinfo(
                obtener_texto("integridad"),
                mensaje,
                parent=root
            )

    except (OSError, ValueError) as error:

        messagebox.showerror(
            obtener_texto("integridad"),
            f"{obtener_texto('error_integridad')}\n{error}",
            parent=root
        )


def crear_respaldo_ui():

    try:

        resultado = crear_respaldo()

        mensaje = (
            f"{obtener_texto('respaldo_correcto')}\n\n"
            f"{obtener_texto('archivo_texto')}: {resultado['ruta']}\n"
            f"{obtener_texto('tamano_original')}: "
            f"{resultado['tamaño_original']} bytes\n"
            f"{obtener_texto('tamano_comprimido')}: "
            f"{resultado['tamaño_comprimido']} bytes"
        )

        messagebox.showinfo(
            obtener_texto("respaldo_zip"),
            mensaje,
            parent=root
        )

    except (OSError, ValueError) as error:

        messagebox.showerror(
            obtener_texto("respaldo_zip"),
            str(error),
            parent=root
        )


def mostrar_informacion_archivos_ui():

    archivos = [
        archivo_contactos,
        archivo_indice,
        archivo_hash
    ]

    if archivo_respaldo.exists():
        archivos.append(archivo_respaldo)

    lineas = []

    for ruta in archivos:

        try:

            informacion = obtener_informacion_archivo(ruta)

            lectura = (
                obtener_texto("si")
                if informacion["lectura"]
                else obtener_texto("no")
            )

            escritura = (
                obtener_texto("si")
                if informacion["escritura"]
                else obtener_texto("no")
            )

            lineas.append(
                f"{informacion['nombre']}\n"
                f"{obtener_texto('tamano')}: "
                f"{informacion['tamaño']} bytes\n"
                f"{obtener_texto('ultima_modificacion')}: "
                f"{informacion['ultima_modificacion']}\n"
                f"{obtener_texto('lectura')}: {lectura}\n"
                f"{obtener_texto('escritura')}: {escritura}"
            )

        except (OSError, FileNotFoundError) as error:

            lineas.append(f"{ruta.name}: {error}")

    messagebox.showinfo(
        obtener_texto("informacion_archivos"),
        "\n\n".join(lineas),
        parent=root
    )


def mostrar_ayuda_ui():

    ayuda = (
        f"{obtener_texto('ayuda_titulo')}\n\n"
        f"{obtener_texto('ayuda_descripcion')}\n\n"
        f"{obtener_texto('tamano_registro')}: "
        f"{tamaño_registro} bytes\n\n"
        f"{obtener_texto('tamano_campos')}:\n"
        f"{obtener_texto('campo_id')}: {campos['id']} bytes\n"
        f"{obtener_texto('campo_nombre')}: {campos['nombre']} bytes\n"
        f"{obtener_texto('campo_telefono')}: {campos['telefono']} bytes\n"
        f"{obtener_texto('campo_email')}: {campos['email']} bytes\n"
        f"{obtener_texto('campo_ciudad')}: {campos['ciudad']} bytes"
    )

    messagebox.showinfo(
        obtener_texto("ayuda"),
        ayuda,
        parent=root
    )


def mostrar_menu_archivo():

    menu = tk.Menu(root, tearoff=0)

    menu.add_command(
        label=obtener_texto("agregar"),
        command=agregar_contacto_ui
    )

    menu.add_command(
        label=obtener_texto("buscar"),
        command=buscar_contacto_ui
    )

    menu.add_command(
        label=obtener_texto("modificar"),
        command=modificar_contacto_ui
    )

    menu.post(
        boton_archivo.winfo_rootx(),
        boton_archivo.winfo_rooty() + boton_archivo.winfo_height()
    )


def mostrar_menu_edicion():

    menu = tk.Menu(root, tearoff=0)

    menu.add_command(
        label=obtener_texto("exportar_json"),
        command=exportar_json_ui
    )

    menu.add_command(
        label=obtener_texto("exportar_pdf"),
        command=exportar_pdf_ui
    )

    menu.post(
        boton_edicion.winfo_rootx(),
        boton_edicion.winfo_rooty() + boton_edicion.winfo_height()
    )


def mostrar_menu_ver():

    menu = tk.Menu(root, tearoff=0)

    menu.add_command(
        label=obtener_texto("verificar"),
        command=verificar_integridad_ui
    )

    menu.add_command(
        label=obtener_texto("respaldo"),
        command=crear_respaldo_ui
    )

    menu.add_command(
        label=obtener_texto("informacion"),
        command=mostrar_informacion_archivos_ui
    )

    menu.add_separator()

    menu.add_command(
        label=obtener_texto("ayuda"),
        command=mostrar_ayuda_ui
    )

    menu.add_separator()

    menu.add_command(
        label=obtener_texto("salir"),
        command=root.destroy
    )

    menu.post(
        boton_ver.winfo_rootx(),
        boton_ver.winfo_rooty() + boton_ver.winfo_height()
    )

def main():

    global root
    global config
    global color_barra
    global foto_perfil

    global panel_izquierdo
    global panel_derecho
    global barra_menu

    global boton_settings
    global boton_archivo
    global boton_edicion
    global boton_ver

    global etiqueta_usuario
    global etiqueta_nombre
    global etiqueta_bienvenida
    global etiqueta_descripcion

    config = load_config()

    obtener_estilos()

    color_barra = config.get("color_barra_menu", "#171c26")
    foto_perfil = config["foto_perfil"]

    root = tk.Tk()

    root.title("Main")
    root.geometry("520x380")
    root.resizable(False, False)

    panel_izquierdo = tk.Frame(
        root,
        bg=color_barra
    )

    panel_izquierdo.place(
        x=0,
        y=0,
        width=190,
        height=370
    )

    barra_menu = panel_izquierdo

    if config["tema_interfaz"] == "oscuro":

        color_fondo = "#222222"

    else:

        color_fondo = "#f8fafc"

    panel_derecho = tk.Frame(
        root,
        bg=color_fondo
    )

    panel_derecho.place(
        x=190,
        y=0,
        width=330,
        height=370
    )

    etiqueta_usuario = tk.Label(
        panel_izquierdo,
        text="👤",
        bg=color_barra,
        font=("Arial", 25)
    )

    etiqueta_usuario.place(
        x=30,
        y=50,
        width=60,
        height=60
    )

    ToolTip(
        etiqueta_usuario,
        "Bonita Foto ;3"
    )

    etiqueta_nombre = tk.Label(
        panel_izquierdo,
        text=config["nombre_usuario"],
        bg=color_barra
    )

    etiqueta_nombre.place(
        x=90,
        y=60,
        width=90,
        height=30
    )

    boton_settings = tk.Button(
        panel_izquierdo,
        text="Configuración",
        command=mostrar_settings,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    boton_settings.place(
        x=47,
        y=140,
        width=96,
        height=32
    )

    boton_archivo = tk.Button(
        panel_izquierdo,
        text="Archivo",
        command=mostrar_menu_archivo,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    boton_archivo.place(
        x=47,
        y=190,
        width=96,
        height=32
    )

    boton_edicion = tk.Button(
        panel_izquierdo,
        text="Edición",
        command=mostrar_menu_edicion,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    boton_edicion.place(
        x=47,
        y=240,
        width=96,
        height=32
    )

    boton_ver = tk.Button(
        panel_izquierdo,
        text="Ver",
        command=mostrar_menu_ver,
        relief="flat",
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )

    boton_ver.place(
        x=47,
        y=290,
        width=96,
        height=32
    )

    etiqueta_bienvenida = tk.Label(
        panel_derecho,
        text="¡Bienvenido!",
        bg=color_fondo
    )

    etiqueta_bienvenida.place(
        x=50,
        y=75,
        width=230,
        height=50
    )

    etiqueta_descripcion = tk.Label(
        panel_derecho,
        text="Con esta aplicación puedes gestionar tu configuración y personalizar tu experiencia",
        bg=color_fondo,
        wraplength=220
    )

    etiqueta_descripcion.place(
        x=50,
        y=112,
        width=230,
        height=60
    )

    cargar_foto_perfil()
    aplicar_configuracion()
    actualizar_textos()

    root.mainloop()


if __name__ == "__main__":
    main()