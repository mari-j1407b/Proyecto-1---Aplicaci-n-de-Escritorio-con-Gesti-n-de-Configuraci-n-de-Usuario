
from src.agenda import (
    carpeta,
    archivo_contactos,
    archivo_hash,
    guardar_hash,
    verificar_integridad
)


def comprobar_integridad_inicio():
    carpeta.mkdir(parents=True, exist_ok=True)

    if not archivo_contactos.exists():
        archivo_contactos.write_bytes(b"")

    if not archivo_hash.exists():
        if archivo_contactos.stat().st_size == 0:
            guardar_hash()
            return True

        return False

    return verificar_integridad()


def obtener_estado_integridad():
    if comprobar_integridad_inicio():
        return "Los archivos de contactos mantienen su integridad."

    return (
        "ADVERTENCIA: No se pudo verificar la integridad. "
        "El archivo pudo haber sido modificado o el hash no existe."
    )
