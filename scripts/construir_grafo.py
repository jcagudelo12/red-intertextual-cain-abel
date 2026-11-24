#!/usr/bin/env python3
"""Construye el grafo intertextual a partir de data/ y escribe salidas/.

Salidas: grafo.gexf, grafo.graphml, nodos.csv, aristas.csv, informe.md, grafo.html
"""
import argparse
import csv
import html
import json
import sys
from collections import Counter
from pathlib import Path

import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tei_a_relaciones  # noqa: E402
import validar  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
ORDEN_CERTEZA = {"baja": 0, "media": 1, "alta": 2}
COLORES_TIPO = {
    "fuente_biblica": "#8c564b", "texto_biblico": "#bc8f6f", "texto_religioso": "#2ca02c",
    "exegesis_comentario": "#17becf", "patristica": "#1f77b4", "literatura_narrativa": "#ff7f0e",
    "literatura_poesia": "#e377c2", "literatura_teatro": "#d62728", "filosofia": "#9467bd",
    "articulo_academico": "#7f7f7f", "libro_academico": "#bcbd22", "otro": "#c7c7c7",
    "motivo": "#f2e394",
}
COLORES_FAMILIA = {"literaria": "#d62728", "academica": "#1f77b4", "motivo": "#aaaaaa"}


def leer_csv(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def construir(raiz: Path, min_certeza: str, incluir_motivos: bool, incluir_tei: bool):
    obras = leer_csv(raiz / "data" / "obras.csv")
    rels = leer_csv(raiz / "data" / "relaciones.csv")
    tipos = {t["id"]: t for t in leer_csv(raiz / "data" / "vocabularios" / "tipos_relacion.csv")}
    motivos = {m["id"]: m for m in leer_csv(raiz / "data" / "vocabularios" / "motivos.csv")}
    ids_obras = {o["id"] for o in obras}

    if incluir_tei:
        for r in tei_a_relaciones.extraer(raiz):
            if r["origen"] not in ids_obras or r["destino"] not in ids_obras:
                print(f"AVISO: relación TEI {r['id']} ignorada: origen '{r['origen']}' "
                      f"o destino '{r['destino']}' no está en obras.csv")
                continue
            if r["tipo_relacion"] not in tipos or r["certeza"] not in ORDEN_CERTEZA:
                print(f"AVISO: relación TEI {r['id']} ignorada: tipo o certeza no válidos")
                continue
            rels.append(r)

    g = nx.MultiDiGraph()
    for o in obras:
        g.add_node(o["id"], titulo=o["titulo"], autor=o["autor"], anio=o["anio"],
                   tipo_obra=o["tipo_obra"], lengua=o["lengua"])
    vistos_motivo = set()
    for r in rels:
        if ORDEN_CERTEZA[r["certeza"]] < ORDEN_CERTEZA[min_certeza]:
            continue
        lista = [m for m in r["motivos"].split(";") if m]
        g.add_edge(r["origen"], r["destino"], key=r["id"],
                   tipo_relacion=r["tipo_relacion"],
                   familia=tipos[r["tipo_relacion"]]["familia"],
                   certeza=r["certeza"], motivos=";".join(lista),
                   evidencia=r["evidencia"])
        if incluir_motivos:
            for m in lista:
                nid = f"motivo:{m}"
                if nid not in g:
                    g.add_node(nid, titulo=motivos[m]["etiqueta"], autor="", anio="",
                               tipo_obra="motivo", lengua="")
                if (r["origen"], m) not in vistos_motivo:
                    vistos_motivo.add((r["origen"], m))
                    g.add_edge(r["origen"], nid, key=f"{r['origen']}->{m}",
                               tipo_relacion="tiene_motivo", familia="motivo",
                               certeza=r["certeza"], motivos="", evidencia="")
    return g


def escribir_tablas(g, salidas: Path):
    with (salidas / "nodos.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Id", "Label", "autor", "anio", "tipo_obra", "lengua"])
        for n, d in g.nodes(data=True):
            w.writerow([n, d["titulo"], d["autor"], d["anio"], d["tipo_obra"], d["lengua"]])
    with (salidas / "aristas.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Source", "Target", "Type", "Id", "tipo_relacion", "familia",
                    "certeza", "motivos", "evidencia"])
        for u, v, k, d in g.edges(keys=True, data=True):
            w.writerow([u, v, "Directed", k, d["tipo_relacion"], d["familia"],
                        d["certeza"], d["motivos"], d["evidencia"]])


def top(pares, n=10):
    return sorted(pares, key=lambda x: (-x[1], x[0]))[:n]


def escribir_informe(g, salidas: Path, args):
    obras_g = g.subgraph([n for n, d in g.nodes(data=True) if d["tipo_obra"] != "motivo"])
    simple = nx.DiGraph()
    simple.add_nodes_from(obras_g.nodes)
    simple.add_edges_from((u, v) for u, v in obras_g.edges())
    L = ["# Informe del grafo", "",
         f"Parámetros: `--min-certeza {args.min_certeza}`"
         f"{' --incluir-motivos' if args.incluir_motivos else ''}"
         f"{' --incluir-tei' if args.incluir_tei else ''}", "",
         f"Nodos: {g.number_of_nodes()} | Aristas: {g.number_of_edges()}", "",
         "Las métricas se calculan solo sobre las obras y sus relaciones (sin nodos de motivo).", "",
         "## Obras por tipo", ""]
    for k, v in sorted(Counter(d["tipo_obra"] for _, d in obras_g.nodes(data=True)).items()):
        L.append(f"- {k}: {v}")
    L += ["", "## Relaciones por tipo", ""]
    for k, v in sorted(Counter(d["tipo_relacion"] for _, _, d in obras_g.edges(data=True)).items()):
        L.append(f"- {k}: {v}")

    def tabla(titulo, pares, cab):
        L.extend(["", f"## {titulo}", "", f"| Obra | {cab} |", "|---|---|"])
        for n, val in pares:
            L.append(f"| {n} | {val} |")

    tabla("Grado de entrada (top 10)", top(simple.in_degree()), "Grado")
    tabla("Grado de salida (top 10)", top(simple.out_degree()), "Grado")
    bet = nx.betweenness_centrality(simple)
    tabla("Betweenness (top 10)", [(n, f"{v:.4f}") for n, v in top(bet.items())], "Valor")
    comunidades = nx.community.louvain_communities(simple.to_undirected(), seed=42)
    L += ["", "## Comunidades (Louvain, seed=42, grafo no dirigido)", ""]
    for i, c in enumerate(sorted(comunidades, key=lambda c: (-len(c), sorted(c)[0])), 1):
        L.append(f"{i}. {', '.join(sorted(c))}")
    (salidas / "informe.md").write_text("\n".join(L) + "\n", encoding="utf-8")


PLANTILLA_HTML = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><title>Red intertextual Caín y Abel</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
body{margin:0;font-family:sans-serif}#red{width:100vw;height:100vh}
#leyenda{position:absolute;top:8px;left:8px;background:#fffd;padding:8px;border:1px solid #ccc;font-size:12px;max-width:240px}
.c{display:inline-block;width:12px;height:12px;margin-right:4px;vertical-align:middle}
</style></head><body>
<div id="red"></div><div id="leyenda"></div>
<script>
var datos = __DATOS__;
var colT = __COLT__, colF = __COLF__;
var nodos = datos.nodes.map(function(n){
  return {id:n.id,label:n.label,title:n.title,color:colT[n.tipo]||"#ccc",shape:n.tipo==="motivo"?"diamond":"dot"};});
var aristas = datos.edges.map(function(e){
  return {from:e.from,to:e.to,arrows:"to",title:e.title,color:{color:colF[e.familia]||"#999"},
          dashes:e.certeza==="baja"};});
new vis.Network(document.getElementById("red"),
  {nodes:new vis.DataSet(nodos),edges:new vis.DataSet(aristas)},
  {physics:{stabilization:true},interaction:{hover:true}});
var h="<b>Nodos (tipo de obra)</b><br>";
datos.tipos.forEach(function(t){h+='<span class="c" style="background:'+colT[t]+'"></span>'+t+'<br>';});
h+="<br><b>Aristas (familia)</b><br>";
Object.keys(colF).forEach(function(f){h+='<span class="c" style="background:'+colF[f]+'"></span>'+f+'<br>';});
h+="<br>Línea discontinua: certeza baja";
document.getElementById("leyenda").innerHTML=h;
</script></body></html>
"""


def escribir_html(g, salidas: Path):
    def seguro(s):
        return s.replace("</", "<\\/")

    nodes = []
    for n, d in g.nodes(data=True):
        t = f"<b>{html.escape(d['titulo'])}</b><br>{html.escape(d['autor'])} {html.escape(d['anio'])}<br>{d['tipo_obra']}"
        nodes.append({"id": n, "label": d["titulo"][:40], "title": t, "tipo": d["tipo_obra"]})
    edges = []
    for u, v, k, d in g.edges(keys=True, data=True):
        t = f"{d['tipo_relacion']} (certeza {d['certeza']})<br>{html.escape(d['evidencia'])}"
        edges.append({"from": u, "to": v, "title": t, "familia": d["familia"], "certeza": d["certeza"]})
    tipos = sorted({d["tipo_obra"] for _, d in g.nodes(data=True)})
    datos = json.dumps({"nodes": nodes, "edges": edges, "tipos": tipos}, ensure_ascii=False)
    # vis-network interpreta "title" como texto plano si es string: se pasa como HTML vía elemento
    pagina = (PLANTILLA_HTML.replace("__DATOS__", seguro(datos))
              .replace("__COLT__", json.dumps(COLORES_TIPO))
              .replace("__COLF__", json.dumps(COLORES_FAMILIA)))
    pagina = pagina.replace(
        "var nodos = datos.nodes.map(function(n){",
        "function H(s){var d=document.createElement('div');d.innerHTML=s;return d;}\n"
        "var nodos = datos.nodes.map(function(n){n.title=H(n.title);")
    pagina = pagina.replace(
        "var aristas = datos.edges.map(function(e){",
        "var aristas = datos.edges.map(function(e){e.title=H(e.title);")
    (salidas / "grafo.html").write_text(pagina, encoding="utf-8")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--min-certeza", choices=list(ORDEN_CERTEZA), default="baja")
    p.add_argument("--incluir-motivos", action="store_true",
                   help="añade nodos de motivo y aristas obra->motivo")
    p.add_argument("--incluir-tei", action="store_true",
                   help="incorpora relaciones extraídas de tei/textos")
    args = p.parse_args(argv)

    errores, avisos = validar.validar(RAIZ)
    for a in avisos:
        print(f"AVISO: {a}")
    if errores:
        for e in errores:
            print(f"ERROR: {e}")
        print("Validación fallida: se aborta la construcción del grafo.")
        return 1

    g = construir(RAIZ, args.min_certeza, args.incluir_motivos, args.incluir_tei)
    salidas = RAIZ / "salidas"
    salidas.mkdir(exist_ok=True)
    nx.write_gexf(g, salidas / "grafo.gexf")
    nx.write_graphml(g, salidas / "grafo.graphml")
    escribir_tablas(g, salidas)
    escribir_informe(g, salidas, args)
    escribir_html(g, salidas)
    print(f"Grafo: {g.number_of_nodes()} nodos, {g.number_of_edges()} aristas. Salidas en {salidas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
