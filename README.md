# Red intertextual Caín y Abel

Este proyecto reúne, en un mapa de conexiones, los textos que retoman, citan, comentan o transforman el relato de Caín y Abel (Génesis 4,1-16). Cada texto es un punto y cada relación entre dos textos (una cita, una reescritura, una crítica) es una línea que los une. El corpus es heterogéneo: textos bíblicos, religiosos (Corán, midrash), patrística, literatura, filosofía y estudios académicos.

Forma parte de una tesis doctoral en filosofía. La pregunta de investigación, **provisional**, es: *¿Cómo circula y se transforma el relato de Caín y Abel en la tradición textual (religiosa, literaria, filosófica y académica) y qué textos funcionan como puentes entre tradiciones?*

El proyecto produce dos cosas:

- **Un grafo** de relaciones intertextuales, que se puede explorar en el navegador o analizar en Gephi.
- **Un método replicable** de anotación (tablas, vocabularios controlados y validación automática) que sirve también para otros relatos.

> **Advertencia:** los datos semilla (obras y relaciones) son **ilustrativos** y están marcados "EJEMPLO – verificar". No son resultados de investigación. La obra `plantilla-articulo` solo muestra el formato.

## Empieza aquí

Elige el perfil que más se parezca al tuyo.

### Investigador/a o anotador/a (sin programar)

1. Lee el [manual de anotación](docs/manual-anotacion.md).
2. Abre los CSV de [data/](data/) con LibreOffice. Al guardar, elige "CSV (UTF-8), separado por comas".
3. Añade filas siguiendo los [vocabularios controlados](data/vocabularios/) (ver [Añadir una obra o una relación](#añadir-una-obra-o-una-relación)).
4. Pide a alguien del equipo que ejecute la validación, o revisa el resultado de la comprobación automática en la pestaña Actions de GitHub (GitHub Actions).

### Desarrollador/a

1. Sigue la [Instalación](#instalación).
2. Valida los datos y construye el grafo como indica el [Flujo de trabajo](#flujo-de-trabajo).
3. Ejecuta las pruebas con `.venv/bin/python -m pytest`.
4. Lee [docs/decisiones-modelo.md](docs/decisiones-modelo.md) para entender el diseño.

### Solo quiero ver resultados

1. Construye el grafo siguiendo la [Instalación](#instalación) y el [Flujo de trabajo](#flujo-de-trabajo).
2. Abre `salidas/grafo.html` en el navegador, o `salidas/grafo.gexf` en Gephi.

## Un ejemplo

Un **nodo** es una obra: una fila de [data/obras.csv](data/obras.csv). Una **arista** es una relación entre dos obras: una fila de [data/relaciones.csv](data/relaciones.csv), dirigida desde el texto de origen (el que retoma) hacia el texto de destino (el retomado). Esta es una fila real de `relaciones.csv`:

```csv
r0009,steinbeck-east-of-eden-1952,genesis-4,cita,,Gen.4.7,timshel,m_pecado_acecha,alta,,anotadorA,2026-11-24,EJEMPLO – verificar
```

| Columna | Valor | Qué significa |
|---|---|---|
| `id` | `r0009` | Identificador único de la relación. |
| `origen` | `steinbeck-east-of-eden-1952` | Id de la obra que retoma el relato (*East of Eden*, de John Steinbeck, 1952), tal como figura en `obras.csv`. |
| `destino` | `genesis-4` | Id de la obra retomada (Génesis 4, Caín y Abel). |
| `tipo_relacion` | `cita` | Tipo de relación, del vocabulario [tipos_relacion.csv](data/vocabularios/tipos_relacion.csv): reproducción literal y reconocible de un fragmento del destino. |
| `loc_origen` | (vacío) | Dónde aparece en la obra de origen (capítulo o página). Opcional. |
| `loc_destino` | `Gen.4.7` | Pasaje del destino, en formato OSIS: Génesis, capítulo 4, versículo 7. |
| `evidencia` | `timshel` | Fragmento o descripción breve que respalda la relación. |
| `motivos` | `m_pecado_acecha` | Motivo del vocabulario [motivos.csv](data/vocabularios/motivos.csv): "El pecado acecha" (incluye el tema de *timshel*). |
| `certeza` | `alta` | Confianza en la relación (`alta`, `media` o `baja`): aquí es explícita. |
| `mediada_por` | (vacío) | Id de una obra intermediaria, si la hubo. Opcional. |
| `anotador` | `anotadorA` | Quién registró la relación. |
| `fecha` | `2026-11-24` | Fecha de la anotación. |
| `notas` | `EJEMPLO – verificar` | Comentarios libres; aquí marca que el dato es ilustrativo. |

Leída en lenguaje natural: *East of Eden*, de Steinbeck, cita (con certeza alta) a Génesis 4,7 mediante la palabra "timshel", ligada al motivo de que el pecado acecha a Caín.

## Modelo híbrido

1. Capa principal: tablas CSV ([data/obras.csv](data/obras.csv), [data/relaciones.csv](data/relaciones.csv)), editables en LibreOffice o Excel.
2. Vocabularios controlados ([data/vocabularios/](data/vocabularios/)) y validación por script.
3. Cada relación lleva evidencia breve (localización y fragmento) para no guardar textos con derechos.
4. Capa opcional TEI XML, solo para textos de dominio público que requieran lectura cercana; un script extrae sus `<link>` al mismo formato.
5. Tipos de relación basados en Genette (literarias) y CiTO (académicas), con columna de mapeo.

Más detalle en [docs/decisiones-modelo.md](docs/decisiones-modelo.md).

## Estructura

```
data/            obras.csv, relaciones.csv y vocabularios/
docs/            metodologia.md, manual-anotacion.md, decisiones-modelo.md
tei/             capa TEI opcional (ODD y textos)
scripts/         validar.py, construir_grafo.py, tei_a_relaciones.py
tests/           pruebas con pytest
salidas/         resultados generados (ignorados por git)
```

Enlaces rápidos:

- [data/](data/): [obras.csv](data/obras.csv), [relaciones.csv](data/relaciones.csv) y [vocabularios/](data/vocabularios/) ([motivos.csv](data/vocabularios/motivos.csv), [personajes.csv](data/vocabularios/personajes.csv), [tipos_obra.csv](data/vocabularios/tipos_obra.csv), [tipos_relacion.csv](data/vocabularios/tipos_relacion.csv)).
- [docs/](docs/): [metodologia.md](docs/metodologia.md), [manual-anotacion.md](docs/manual-anotacion.md), [decisiones-modelo.md](docs/decisiones-modelo.md).
- [tei/](tei/): [README.md](tei/README.md), [ODD](tei/odd/red-intertextual.odd.xml) y textos ([genesis-4.xml](tei/textos/genesis-4.xml), [plantilla.xml](tei/textos/plantilla.xml)).
- [scripts/](scripts/): [validar.py](scripts/validar.py), [construir_grafo.py](scripts/construir_grafo.py), [tei_a_relaciones.py](scripts/tei_a_relaciones.py).
- [tests/](tests/): [test_validar.py](tests/test_validar.py).
- `salidas/`: resultados generados.
- [requirements.txt](requirements.txt) y el flujo de CI en [.github/workflows/validar.yml](.github/workflows/validar.yml).

## Instalación

Dependencias en [requirements.txt](requirements.txt).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Debian/Ubuntu el comando `python` puede no existir (solo `python3`); dentro del entorno virtual activado sí está disponible `python`. Si prefieres no activar el entorno, llama directamente a su intérprete:

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/validar.py
```

## Flujo de trabajo

1. Editar los CSV de [data/](data/).
2. Validar:

   ```bash
   python scripts/validar.py
   ```

3. Construir el grafo (opciones: `--min-certeza {baja,media,alta}`, `--incluir-motivos`, `--incluir-tei`):

   ```bash
   python scripts/construir_grafo.py
   ```

4. Abrir `salidas/grafo.html` en el navegador (carga vis-network desde CDN) o `salidas/grafo.gexf` en Gephi. También se generan `salidas/grafo.graphml`, `salidas/nodos.csv`, `salidas/aristas.csv` y `salidas/informe.md`. Estos archivos se crean en tu copia local al ejecutar el paso 3 y no se suben a GitHub (están ignorados por git).

Con `.venv/bin/python` en lugar de `python` los comandos funcionan sin activar el entorno. Las pruebas se ejecutan con `python -m pytest`.

## Añadir una obra o una relación

Ver el paso a paso en [docs/manual-anotacion.md](docs/manual-anotacion.md). Resumen: añade la fila en [obras.csv](data/obras.csv) o [relaciones.csv](data/relaciones.csv) con ids válidos, motivos de [motivos.csv](data/vocabularios/motivos.csv) y evidencia breve, y ejecuta el validador.

## Replicar el método con otro relato

1. Sustituye [data/vocabularios/motivos.csv](data/vocabularios/motivos.csv) y [personajes.csv](data/vocabularios/personajes.csv) por los del nuevo relato.
2. Cambia la fuente: nueva fila en [obras.csv](data/obras.csv) (tipo `fuente_biblica` u otro) y, si procede, su TEI en [tei/textos/](tei/textos/).
3. Vacía [obras.csv](data/obras.csv) y [relaciones.csv](data/relaciones.csv) y anota el nuevo corpus siguiendo [docs/metodologia.md](docs/metodologia.md).
4. Ajusta las localizaciones (`loc_destino`) al sistema de citación de la nueva fuente.

## Pendiente

- **Licencia:** sugerencia de CC BY 4.0 para los datos y MIT para el código. No se ha creado ningún archivo LICENSE.
- **Cómo citar el proyecto:** por completar (autoría, título, año, URL o DOI).
