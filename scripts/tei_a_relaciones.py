#!/usr/bin/env python3
"""Extrae los <link> de tei/textos/*.xml al formato de relaciones.csv.

Convenciones:
- El id de la obra de origen es el xml:id del elemento <TEI>.
- El destino se deduce del archivo del segundo target (genesis-4.xml -> genesis-4)
  y loc_destino del fragmento (#Gen.4.10 -> Gen.4.10).
- Los motivos salen del @ana del <seg> de origen (sin '#').
"""
import csv
import sys
from pathlib import Path

from lxml import etree

RAIZ = Path(__file__).resolve().parent.parent
NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
CERTEZA = {"high": "alta", "medium": "media", "low": "baja"}
CAMPOS = ["id", "origen", "destino", "tipo_relacion", "loc_origen", "loc_destino",
          "evidencia", "motivos", "certeza", "mediada_por", "anotador", "fecha", "notas"]


def extraer(raiz: Path = RAIZ) -> list[dict]:
    """Devuelve una lista de dicts con las columnas de relaciones.csv."""
    filas = []
    n = 0
    for ruta in sorted((Path(raiz) / "tei" / "textos").glob("*.xml")):
        arbol = etree.parse(str(ruta))
        tei = arbol.getroot()
        origen = tei.get(XML_ID, ruta.stem)
        for link in arbol.xpath("//tei:linkGrp[@type='intertextual']/tei:link", namespaces=NS):
            targets = (link.get("target") or "").split()
            if len(targets) < 2:
                continue
            n += 1
            loc_origen = targets[0].split("#")[-1]
            archivo_dest, _, frag = targets[1].partition("#")
            destino = Path(archivo_dest).stem if archivo_dest else origen
            motivos = []
            seg = arbol.xpath(f"//*[@xml:id='{loc_origen}']")
            if seg:
                motivos = [m.lstrip("#") for m in (seg[0].get("ana") or "").split()]
            filas.append({
                "id": f"t{n:04d}",
                "origen": origen,
                "destino": destino,
                "tipo_relacion": link.get("type") or "",
                "loc_origen": loc_origen,
                "loc_destino": frag,
                "evidencia": "",
                "motivos": ";".join(motivos),
                "certeza": CERTEZA.get(link.get("cert") or "", ""),
                "mediada_por": "",
                "anotador": (link.get("resp") or "").lstrip("#"),
                "fecha": "",
                "notas": f"extraída de {ruta.name}",
            })
    return filas


def escribir(filas: list[dict], destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)


def main() -> int:
    filas = extraer(RAIZ)
    salida = RAIZ / "salidas" / "relaciones_tei.csv"
    escribir(filas, salida)
    print(f"{len(filas)} relaciones TEI escritas en {salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
