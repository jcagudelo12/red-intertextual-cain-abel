# Capa TEI (opcional)

## Cuándo usarla

Solo para textos de **dominio público** que necesiten lectura cercana a nivel de pasaje (por ejemplo, varios pasajes de una obra que retoman distintos versículos). Para todo lo demás basta con `data/relaciones.csv`.

No transcribas textos con derechos de autor: usa evidencia breve en el CSV.

## Cómo

1. Copia `textos/plantilla.xml` a `textos/<id-de-obra>.xml`, con el mismo id que en `data/obras.csv`.
2. Pon ese id en `xml:id` del elemento `<TEI>` y marca `capa_tei = si` en `obras.csv`.
3. Marca los pasajes con `<seg xml:id="..." ana="#m_motivo">` (motivos de `motivos.csv`).
4. Declara las relaciones en `<linkGrp type="intertextual">`:
   `<link type="reescritura" target="#seg_1 genesis-4.xml#Gen.4.10" cert="high" resp="#anotadorA"/>`
   El primer target es el origen; el segundo, `archivo.xml#versículo`, el destino.
5. Extrae las relaciones: `python scripts/tei_a_relaciones.py` (escribe `salidas/relaciones_tei.csv`).
6. Incorpora al grafo: `python scripts/construir_grafo.py --incluir-tei`. Las relaciones cuyo origen o destino no estén en `obras.csv` se ignoran con aviso (es lo que ocurre con `plantilla.xml`).

## Esquema

`odd/red-intertextual.odd.xml` restringe `@type` de `<link>` a los tipos literarios. Para generar RelaxNG, consulta el comentario del propio ODD (TEI Roma o TEIGarage).
