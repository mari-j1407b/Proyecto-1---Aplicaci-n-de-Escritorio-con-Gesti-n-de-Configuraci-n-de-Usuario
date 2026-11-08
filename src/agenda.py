
import json
import hashlib
from pathlib import Path

carpeta = Path(__file__).resolve().parent.parent / "datos_agenda"
archivo_contactos = carpeta / "contactos.dat"
archivo_indice = carpeta / "indice.json"
archivo_hash = carpeta / "contactos.sha256"

# Tamaño de cada campo en bytes.
campos = {
    "id": 8,
    "nombre": 40,
    "telefono": 15,
    "email": 45,
    "ciudad": 20
}

tamaño_registro = sum(campos.values())


def preparar_archivos():
    carpeta.mkdir(parents=True, exist_ok=True)

    if not archivo_contactos.exists():
        archivo_contactos.write_bytes(b"")

    if not archivo_indice.exists():
        archivo_indice.write_text("{}", encoding="utf-8")




def codificar_campo(valor, tamaño):
    resultado = ""

    for caracter in str(valor):
        if len((resultado + caracter).encode("utf-8")) > tamaño:
            break
        resultado += caracter

    return resultado.encode("utf-8").ljust(tamaño, b" ")


def decodificar_campo(datos):
    return datos.decode("utf-8").rstrip()


def guardar_hash():
    contenido = archivo_contactos.read_bytes()
    resultado = hashlib.sha256(contenido).hexdigest()
    archivo_hash.write_text(resultado, encoding="utf-8")


def verificar_integridad():
    if not archivo_hash.exists():
        return False

    hash_guardado = archivo_hash.read_text(
        encoding="utf-8"
    ).strip()

    hash_actual = hashlib.sha256(
        archivo_contactos.read_bytes()
    ).hexdigest()

    return hash_guardado == hash_actual


def cargar_indice():
    try:
        return json.loads(
            archivo_indice.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError):
        raise ValueError(
            "El índice está dañado o no se puede leer."
        )


def guardar_indice(indice):
    archivo_indice.write_text(
        json.dumps(indice, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )


def codificar_contacto(contacto):
    registro = b""

    for campo, tamaño in campos.items():
        registro += codificar_campo(contacto[campo], tamaño)

    return registro


def decodificar_contacto(registro):
    contacto = {}
    inicio = 0

    for campo, tamaño in campos.items():
        datos = registro[inicio:inicio + tamaño]
        contacto[campo] = decodificar_campo(datos)
        inicio += tamaño

    contacto["id"] = int(contacto["id"])
    return contacto


def agregar_contacto(contacto):
    preparar_archivos()
    indice = cargar_indice()
    identificador = str(int(contacto["id"]))

    if identificador in indice:
        raise ValueError("Ya existe un contacto con ese ID.")

    registro = codificar_contacto(contacto)

    with open(archivo_contactos, "ab") as archivo:
        archivo.seek(0, 2)
        posicion = archivo.tell()
        numero_registro = posicion // tamaño_registro
        archivo.write(registro)
        posicion_final = archivo.tell()

    indice[identificador] = numero_registro
    guardar_indice(indice)
    guardar_hash()

    return posicion


def buscar_contacto(identificador):
    preparar_archivos()
    indice = cargar_indice()
    clave = str(int(identificador))

    if clave not in indice:
        raise ValueError("No existe un contacto con ese ID.")

    numero_registro = int(indice[clave])

    with open(archivo_contactos, "rb") as archivo:
        archivo.seek(numero_registro * tamaño_registro)
        posicion = archivo.tell()
        registro = archivo.read(tamaño_registro)

    if len(registro) != tamaño_registro:
        raise ValueError("El registro está incompleto o dañado.")

    contacto = decodificar_contacto(registro)
    return contacto, posicion


def modificar_contacto(identificador, datos):
    preparar_archivos()
    indice = cargar_indice()
    clave = str(int(identificador))

    if clave not in indice:
        raise ValueError("No existe un contacto con ese ID.")

    numero_registro = int(indice[clave])

    with open(archivo_contactos, "r+b") as archivo:
        archivo.seek(numero_registro * tamaño_registro)
        posicion = archivo.tell()

        registro_actual = archivo.read(tamaño_registro)

        if len(registro_actual) != tamaño_registro:
            raise ValueError("El registro está incompleto o dañado.")

        contacto = decodificar_contacto(registro_actual)
        contacto.update(datos)
        contacto["id"] = int(identificador)

        archivo.seek(posicion)
        archivo.write(codificar_contacto(contacto))

    guardar_hash()
    return posicion


preparar_archivos()
