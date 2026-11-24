#!/usr/bin/env python3
"""Valida los CSV de data/ contra los vocabularios controlados.

Solo usa la biblioteca estándar. Sale con código 1 si hay errores.
"""
import csv
import re
import sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

CAB_OBRAS = ["id", "tipo_obra", "titulo", "autor", "anio", "lengua",
             "referencia_edicion", "zotero_key", "derechos", "capa_tei", "notas"]
CAB_RELACIONES = ["id", "origen", "destino", "tipo_relacion", "loc_origen",
                  "loc_destino", "evidencia", "motivos", "certeza",
                  "mediada_por", "anotador", "fecha", "notas"]
CAB_TIPOS_OBRA = ["id", "etiqueta", "descripcion"]
CAB_TIPOS_RELACION = ["id", "etiqueta", "familia", "cito", "genette", "descripcion"]
CAB_MOTIVOS = ["id", "etiqueta", "versiculo", "descripcion"]
CAB_PERSONAJES = ["id", "nombre", "variantes", "descripcion"]

DERECHOS = {"dominio_publico", "con_derechos", "desconocido"}
CAPA_TEI = {"si", "no"}
CERTEZA = {"alta", "media", "baja"}
FAMILIAS = {"literaria", "academica"}
RE_ID_OBRA = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_ID_REL = re.compile(r"^r\d{4,}$")
RE_ID_VOC = re.compile(r"^[a-z0-9]+(_[a-z0-9]+)*$")
UMBRAL_EVIDENCIA = 300


def leer(ruta: Path, cabecera: list, errores: list) -> list:
    """Lee un CSV comprobando la cabecera; devuelve lista de dicts."""
    nombre = ruta.name
    if not ruta.exists():
        errores.append(f"{nombre}: archivo no encontrado")
        return []
    with ruta.open(encoding="utf-8", newline="") as f:
        lector = csv.reader(f)
        try:
            cab = next(lector)
        except StopIteration:
            errores.append(f"{nombre}: archivo vacío")
            return []
        if cab and cab[0].startswith("﻿"):
            cab[0] = cab[0].lstrip("﻿")
        if cab != cabecera:
            errores.append(f"{nombre}: cabecera incorrecta. Esperada {cabecera}, encontrada {cab}")
            return []
        filas = []
        for n, fila in enumerate(lector, start=2):
            if not fila:
                continue
            if len(fila) != len(cabecera):
                errores.append(f"{nombre}:{n}: {len(fila)} columnas en lugar de {len(cabecera)}")
                continue
            d = dict(zip(cabecera, fila))
            d["_linea"] = n
            filas.append(d)
        return filas


def comprobar_ids(filas, nombre, regex, errores):
    vistos = set()
    for f in filas:
        i = f["id"]
        if not regex.match(i):
            errores.append(f"{nombre}:{f['_linea']}: id con formato inválido '{i}'")
        if i in vistos:
            errores.append(f"{nombre}:{f['_linea']}: id duplicado '{i}'")
        vistos.add(i)
    return vistos


def validar(raiz: Path) -> tuple[list[str], list[str]]:
    """Valida el repositorio en `raiz`. Devuelve (errores, avisos)."""
    raiz = Path(raiz)
    errores: list[str] = []
    avisos: list[str] = []
    voc = raiz / "data" / "vocabularios"
    tipos_obra = leer(voc / "tipos_obra.csv", CAB_TIPOS_OBRA, errores)
    tipos_rel = leer(voc / "tipos_relacion.csv", CAB_TIPOS_RELACION, errores)
    motivos = leer(voc / "motivos.csv", CAB_MOTIVOS, errores)
    personajes = leer(voc / "personajes.csv", CAB_PERSONAJES, errores)
    obras = leer(raiz / "data" / "obras.csv", CAB_OBRAS, errores)
    rels = leer(raiz / "data" / "relaciones.csv", CAB_RELACIONES, errores)

    ids_tipo_obra = comprobar_ids(tipos_obra, "tipos_obra.csv", RE_ID_VOC, errores)
    ids_tipo_rel = comprobar_ids(tipos_rel, "tipos_relacion.csv", RE_ID_VOC, errores)
    ids_motivos = comprobar_ids(motivos, "motivos.csv", RE_ID_VOC, errores)
    comprobar_ids(personajes, "personajes.csv", RE_ID_VOC, errores)
    for t in tipos_rel:
        if t["familia"] not in FAMILIAS:
            errores.append(f"tipos_relacion.csv:{t['_linea']}: familia inválida '{t['familia']}'")

    ids_obras = comprobar_ids(obras, "obras.csv", RE_ID_OBRA, errores)
    for o in obras:
        ln = f"obras.csv:{o['_linea']}"
        if o["tipo_obra"] not in ids_tipo_obra:
            errores.append(f"{ln}: tipo_obra desconocido '{o['tipo_obra']}'")
        if o["anio"].strip():
            if not re.fullmatch(r"-?\d+", o["anio"].strip()):
                errores.append(f"{ln}: anio no es entero '{o['anio']}'")
        if o["derechos"] not in DERECHOS:
            errores.append(f"{ln}: derechos inválido '{o['derechos']}'")
        if o["capa_tei"] not in CAPA_TEI:
            errores.append(f"{ln}: capa_tei inválido '{o['capa_tei']}'")

    derechos = {o["id"]: o["derechos"] for o in obras}
    con_relacion = set()
    comprobar_ids(rels, "relaciones.csv", RE_ID_REL, errores)
    for r in rels:
        ln = f"relaciones.csv:{r['_linea']}"
        for campo in ("origen", "destino"):
            if r[campo] not in ids_obras:
                errores.append(f"{ln}: {campo} inexistente en obras.csv '{r[campo]}'")
        if r["mediada_por"] and r["mediada_por"] not in ids_obras:
            errores.append(f"{ln}: mediada_por inexistente en obras.csv '{r['mediada_por']}'")
        if r["origen"] == r["destino"]:
            errores.append(f"{ln}: origen y destino son iguales '{r['origen']}'")
        if r["tipo_relacion"] not in ids_tipo_rel:
            errores.append(f"{ln}: tipo_relacion desconocido '{r['tipo_relacion']}'")
        for m in filter(None, (x.strip() for x in r["motivos"].split(";"))):
            if m not in ids_motivos:
                errores.append(f"{ln}: motivo desconocido '{m}'")
        if r["certeza"] not in CERTEZA:
            errores.append(f"{ln}: certeza inválida '{r['certeza']}'")
        try:
            date.fromisoformat(r["fecha"])
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["fecha"]):
                raise ValueError
        except ValueError:
            errores.append(f"{ln}: fecha no ISO (AAAA-MM-DD) '{r['fecha']}'")
        con_relacion.update((r["origen"], r["destino"], r["mediada_por"]))
        for lado in ("origen", "destino"):
            if derechos.get(r[lado]) == "con_derechos" and len(r["evidencia"]) > UMBRAL_EVIDENCIA:
                avisos.append(f"{ln}: evidencia de {len(r['evidencia'])} caracteres sobre obra con_derechos '{r[lado]}' (> {UMBRAL_EVIDENCIA})")
                break

    for o in obras:
        if o["id"] not in con_relacion:
            avisos.append(f"obras.csv:{o['_linea']}: la obra '{o['id']}' no tiene ninguna relación")
    validar.conteo = (len(obras), len(rels))
    return errores, avisos


def main() -> int:
    errores, avisos = validar(RAIZ)
    n_obras, n_rels = getattr(validar, "conteo", (0, 0))
    for e in errores:
        print(f"ERROR: {e}")
    for a in avisos:
        print(f"AVISO: {a}")
    print(f"\nResumen: {n_obras} obras, {n_rels} relaciones, "
          f"{len(errores)} errores, {len(avisos)} avisos")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
