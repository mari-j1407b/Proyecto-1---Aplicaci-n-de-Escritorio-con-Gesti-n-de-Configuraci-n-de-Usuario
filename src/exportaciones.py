
import json
from datetime import datetime
from pathlib import Path
from fpdf import FPDF

from src.agenda import (
    archivo_contactos,
    cargar_indice,
    buscar_contacto
)

carpeta = Path(__file__).resolve().parent.parent / "datos_agenda"
archivo_json = carpeta / "contactos_exportados.json"
archivo_pdf = carpeta / "contactos.pdf"


def exportar_json():
    indice = cargar_indice()
    contactos = []

    for identificador in sorted(indice, key=lambda clave: int(clave)):
        contacto, posicion = buscar_contacto(identificador)
        contactos.append(contacto)

    with open(archivo_json, "w", encoding="utf-8") as archivo:
        json.dump(contactos, archivo, ensure_ascii=False, indent=4)

    return archivo_json



def exportar_pdf():
    indice = cargar_indice()
    contactos = []

    for identificador in sorted(indice, key=lambda clave: int(clave)):
        contacto, posicion = buscar_contacto(identificador)
        contactos.append(contacto)

    documento = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    documento.set_margins(15, 15, 15)
    documento.set_auto_page_break(auto=True, margin=15)
    documento.add_page()

    documento.set_font("Arial", size=16)
    documento.cell(
        w=180,
        h=10,
        text="Agenda de contactos",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    documento.set_font("Arial", size=10)
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    documento.cell(
        w=180,
        h=8,
        text=f"Fecha de exportacion: {fecha}",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    documento.ln(5)


    for contacto in contactos:
        documento.set_font("Arial", style="B", size=11)

        documento.cell(
            w=180,
            h=8,
            text=f"ID: {contacto['id']}",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        documento.set_font("Arial", size=10)

        campos = [
            ("Nombre", contacto["nombre"]),
            ("Teléfono", contacto["telefono"]),
            ("Email", contacto["email"]),
            ("Ciudad", contacto["ciudad"])
        ]

        ancho_separacion = 5
        ancho_columna = (documento.epw - ancho_separacion) / 2

        columna_izquierda = documento.l_margin
        columna_derecha = columna_izquierda + ancho_columna + ancho_separacion

        for i in range(0, len(campos), 2):
            campo_izquierdo, valor_izquierdo = campos[i]
            campo_derecho, valor_derecho = campos[i + 1]

            posicion_y = documento.get_y()

            documento.set_xy(columna_izquierda, posicion_y)

            documento.multi_cell(
                w=ancho_columna,
                h=6,
                text=f"{campo_izquierdo}: {valor_izquierdo}",
                wrapmode="CHAR"
            )

            posicion_izquierda = documento.get_y()

            documento.set_xy(columna_derecha, posicion_y)

            documento.multi_cell(
                w=ancho_columna,
                h=6,
                text=f"{campo_derecho}: {valor_derecho}",
                wrapmode="CHAR"
            )

            posicion_derecha = documento.get_y()

            documento.set_xy(
                columna_izquierda,
                max(posicion_izquierda, posicion_derecha)
            )

        documento.ln(4)


    documento.output(str(archivo_pdf))

    return archivo_pdf
