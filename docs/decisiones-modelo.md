# Registro de decisiones del modelo

## Decisión 1: CSV con vocabularios como núcleo, TEI opcional

**Fecha:** 2026-11-24. **Estado:** adoptada.

### Contexto

Corpus heterogéneo (bíblico, religioso, patrístico, literario, filosófico, académico), muchas obras con derechos de autor, un único investigador que debe poder editar los datos sin herramientas especializadas, y dos productos finales: un grafo y un método replicable.

### Decisión

- Núcleo: tablas CSV (`obras`, `relaciones`) con vocabularios controlados, validadas por script. Cada relación lleva evidencia breve (localización y fragmento), sin guardar textos protegidos.
- Capa opcional: TEI XML solo para textos de dominio público que requieran lectura cercana. Un script extrae sus `<link>` al formato de `relaciones.csv`, de modo que ambas capas alimentan el mismo grafo.
- Tipos de relación: Genette para las literarias y CiTO para las académicas, con una columna `cito` de mapeo.

### Alternativas consideradas

| Alternativa | Ventajas | Desventajas |
|---|---|---|
| TEI completo para todo el corpus | Estándar de las humanidades digitales; granularidad fina | Imposible con textos con derechos; coste alto de codificación; curva de aprendizaje |
| Anotación standoff W3C Web Annotation (CATMA, INCEpTION, Recogito) | Anotación sobre el texto, colaborativa, estándar | Requiere tener el texto cargado (derechos); dependencia de plataforma; exportación y esquema distintos según la herramienta |
| Zotero solo | Ya se usa para la bibliografía | No modela relaciones tipadas entre obras |
| RDF y datos enlazados (CiTO, CIDOC-CRM, ontología INTRO) | Interoperable; semántica formal; consultas SPARQL | Barrera técnica alta para el anotador; tooling pesado para un corpus pequeño |
| Obsidian o markdown | Cómodo de escribir; enlaces naturales | Sin validación ni vocabularios controlados; difícil de analizar |
| Neo4j | Consultas de grafos potentes | Servidor que mantener; menos reproducible; excesivo para el tamaño |

### Consecuencias

- Se pueden editar los datos en LibreOffice o Excel y validarlos automáticamente.
- El grafo es reproducible desde los CSV con un script.
- Se pierde granularidad de pasaje en las obras sin capa TEI, y se compensa con la evidencia breve.

### Ruta de migración futura a RDF

La columna `cito` de `tipos_relacion.csv` da el mapeo a la ontología CiTO. Una migración consistiría en:

1. Convertir cada obra en un recurso (por ejemplo, con una URI base del proyecto).
2. Convertir cada fila de `relaciones.csv` en una tripleta con la propiedad CiTO de la columna `cito`.
3. Reificar o anotar la evidencia, la certeza y el anotador (por ejemplo, con `rdf:Statement` o PROV-O).
4. Si se necesita más precisión, mapear los tipos literarios a INTRO o a CIDOC-CRM.

Los vocabularios de `motivos.csv` y `personajes.csv` se pueden publicar como SKOS.
