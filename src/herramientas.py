
import os
import zipfile
from datetime import datetime
from pathlib import Path

from src.agenda import (
    carpeta,
    archivo_contactos,
    archivo_indice,
    archivo_hash
)


archivo_respaldo = carpeta / "respaldo_agenda.zip"


def crear_respaldo():
    carpeta.mkdir(parents=True, exist_ok=True)

    archivos = [
        archivo_contactos,
        archivo_indice
    ]

    if archivo_hash.exists():
        archivos.append(archivo_hash)

    for archivo in archivos:
        if not archivo.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo: {archivo.name}"
            )

    tamaño_original = sum(
        archivo.stat().st_size for archivo in archivos
    )

    with zipfile.ZipFile(
        archivo_respaldo,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as respaldo:

        for archivo in archivos:
            respaldo.write(archivo, arcname=archivo.name)

    tamaño_comprimido = archivo_respaldo.stat().st_size

    return {
        "ruta": archivo_respaldo,
        "tamaño_original": tamaño_original,
        "tamaño_comprimido": tamaño_comprimido
    }


def obtener_informacion_archivo(ruta):
    ruta = Path(ruta)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta.name}"
        )

    informacion = ruta.stat()

    return {
        "nombre": ruta.name,
        "tamaño": informacion.st_size,
        "ultima_modificacion": datetime.fromtimestamp(
            informacion.st_mtime
        ).strftime("%d/%m/%Y %H:%M:%S"),
        "lectura": os.access(ruta, os.R_OK),
        "escritura": os.access(ruta, os.W_OK)
    }
