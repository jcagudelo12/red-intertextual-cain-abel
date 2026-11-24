# Red intertextual Caín y Abel

Grafo de relaciones entre textos que retoman, citan, comentan o transforman el relato de Caín y Abel (Génesis 4,1-16), y método replicable de anotación. El corpus es heterogéneo: textos bíblicos, religiosos (Corán, midrash), patrística, literatura, filosofía y estudios académicos.

> **Advertencia:** los datos semilla (obras y relaciones) son **ilustrativos** y están marcados "EJEMPLO – verificar". No son resultados de investigación. La obra `plantilla-articulo` solo muestra el formato.

## Modelo híbrido

1. Capa principal: tablas CSV (`data/obras.csv`, `data/relaciones.csv`), editables en LibreOffice o Excel.
2. Vocabularios controlados (`data/vocabularios/`) y validación por script.
3. Cada relación lleva evidencia breve (localización y fragmento) para no guardar textos con derechos.
4. Capa opcional TEI XML, solo para textos de dominio público que requieran lectura cercana; un script extrae sus `<link>` al mismo formato.
5. Tipos de relación basados en Genette (literarias) y CiTO (académicas), con columna de mapeo.

Más detalle en `docs/decisiones-modelo.md`.

## Estructura

```
data/            obras.csv, relaciones.csv y vocabularios/
docs/            metodologia.md, manual-anotacion.md, decisiones-modelo.md
tei/             capa TEI opcional (ODD y textos)
scripts/         validar.py, construir_grafo.py, tei_a_relaciones.py
tests/           pruebas con pytest
salidas/         resultados generados (ignorados por git)
```

## Instalación

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Flujo de trabajo

1. Editar los CSV de `data/`.
2. `python scripts/validar.py`
3. `python scripts/construir_grafo.py` (opciones: `--min-certeza {baja,media,alta}`, `--incluir-motivos`, `--incluir-tei`)
4. Abrir `salidas/grafo.html` en el navegador (carga vis-network desde CDN) o `salidas/grafo.gexf` en Gephi. También se generan `grafo.graphml`, `nodos.csv`, `aristas.csv` e `informe.md`.

## Añadir una obra o una relación

Ver el paso a paso en `docs/manual-anotacion.md`. Resumen: añade la fila en `obras.csv` o `relaciones.csv` con ids válidos, motivos de `motivos.csv` y evidencia breve, y ejecuta el validador.

## Replicar el método con otro relato

1. Sustituye `data/vocabularios/motivos.csv` y `personajes.csv` por los del nuevo relato.
2. Cambia la fuente: nueva fila en `obras.csv` (tipo `fuente_biblica` u otro) y, si procede, su TEI en `tei/textos/`.
3. Vacía `obras.csv` y `relaciones.csv` y anota el nuevo corpus siguiendo `docs/metodologia.md`.
4. Ajusta las localizaciones (`loc_destino`) al sistema de citación de la nueva fuente.

## Pendiente

- **Licencia:** sugerencia de CC BY 4.0 para los datos y MIT para el código. No se ha creado ningún archivo LICENSE.
- **Cómo citar el proyecto:** por completar (autoría, título, año, URL o DOI).
