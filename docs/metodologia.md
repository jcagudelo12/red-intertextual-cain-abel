# Metodología

Fases del proyecto. El flujo es iterativo: lo aprendido en las fases 5 a 7 puede obligar a revisar el esquema (fase 6) y el corpus (fase 2).

## 1. Pregunta de investigación

Formular con precisión qué se quiere saber del grafo. Ejemplos: qué motivos del relato (Gn 4,1-16) se transmiten con más frecuencia, qué obras actúan como puentes entre tradiciones (bíblica, coránica, literaria), cómo cambia la recepción por épocas. La pregunta determina qué relaciones y qué motivos hay que anotar.

## 2. Criterios de inclusión del corpus

- Criterio explícito de entrada: la obra retoma, comenta o transforma el relato (no basta con mencionar un nombre).
- Equilibrio entre tipos de obra (ver `data/vocabularios/tipos_obra.csv`), épocas y lenguas, o justificación del desequilibrio.
- Derechos: textos con derechos solo se registran con evidencia breve; la capa TEI se reserva para dominio público.
- Registrar la edición exacta (`referencia_edicion`) y, si procede, la clave de Zotero.
- Documentar los criterios de exclusión para que el corpus sea replicable.

## 3. Exploración con lingüística de corpus

Estas técnicas **generan candidatos**; no producen relaciones. Cada candidato se valida a mano antes de entrar en `relaciones.csv`.

- **Concordancias KWIC** de los nombres de personaje (`personajes.csv`, con sus variantes) y de expresiones clave.
- **Colocaciones**: qué palabras acompañan a Caín y Abel en cada subcorpus.
- **Keyness**: qué términos caracterizan a un subcorpus frente a otro (por ejemplo, textos que reescriben frente a textos que comentan).
- **Detección de reutilización textual** con Passim o TRACER para localizar citas y paráfrasis entre obras.
- **Embeddings multilingües** para proponer pasajes semánticamente próximos entre lenguas, útiles para alusiones y reescrituras.

Los resultados se guardan como listas de candidatos (fuera de `data/`) con su localización, y se marcan como aceptados, rechazados o dudosos.

## 4. Anotación piloto doble

Dos personas anotan de forma independiente una muestra del corpus con el manual (`docs/manual-anotacion.md`). Cada una usa su identificador de anotador (`anotadorA`, `anotadorB`). Se discuten los desacuerdos y se anotan las decisiones.

## 5. Acuerdo entre anotadores

- Sobre un 10 a 15 % del material anotado por ambos.
- **Kappa de Cohen** (dos anotadores, categorías nominales como `tipo_relacion`) o **alfa de Krippendorff** (más anotadores o datos incompletos).
- Calcular el acuerdo por separado para la existencia de la relación, el tipo y la certeza.
- Analizar la matriz de confusión: qué tipos se confunden indica qué definiciones hay que afinar.

## 6. Iteración del esquema

Revisar vocabularios y manual a partir de los desacuerdos: fusionar o dividir tipos, añadir motivos, aclarar criterios. Registrar cada cambio en `docs/decisiones-modelo.md` y repetir el piloto si el cambio es grande.

## 7. Construcción y análisis del grafo

Con `python scripts/construir_grafo.py`:

- **Grado** de entrada (obras muy retomadas) y de salida (obras que retoman mucho).
- **Betweenness**: obras que actúan de puente entre tradiciones.
- **Comunidades** con Louvain (semilla fija para replicar).
- **Capa temporal**: usar `anio` para ordenar los nodos y estudiar la recepción por periodos (la línea de tiempo de Gephi lee el atributo).
- Variante bipartita obra-motivo (`--incluir-motivos`).
- Filtrar por certeza (`--min-certeza`) para comprobar la robustez de los resultados.
