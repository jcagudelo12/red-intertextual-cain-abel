# Manual de anotación

Dirección de la relación: **origen** es el texto que retoma, cita o comenta; **destino** es el retomado.

## Tipos de relación

Los tipos literarios se basan en Genette y los académicos en CiTO. La tabla completa está en `data/vocabularios/tipos_relacion.csv`. Todos los ejemplos son ilustrativos.

### Literarias

| Tipo | Definición | Positivo | Negativo |
|---|---|---|---|
| `cita` | Fragmento literal y reconocible del destino | Una novela reproduce literalmente las palabras de Gn 4,7 | Un texto que solo coincide en el nombre Caín |
| `parafrasis` | Reformulación cercana con coincidencia léxica parcial | Una frase que reformula la pregunta "¿soy yo guarda de mi hermano?" | Una frase que trata del mismo tema sin correspondencia con el pasaje |
| `alusion` | Referencia indirecta que exige reconocer el destino | "La marca en su frente" para evocar a Caín | Mención explícita del nombre (es `mencion`) |
| `mencion` | Nombra al personaje o al relato sin desarrollarlo | Un ensayo que dice "como Caín" de pasada | Una escena que desarrolla el fratricidio (es `reescritura`) |
| `reescritura` | Transforma el relato entero en una obra nueva | Una novela que reelabora la historia de dos hermanos | Una cita aislada |
| `inversion_parodia` | Invierte valores o imita con distancia crítica | Un poema donde el linaje de Caín triunfa | Una reescritura que mantiene los valores del original |
| `comentario_exegesis` | Explica o interpreta el relato | Un comentario que explica por qué Dios acepta la ofrenda de Abel | Una obra que usa el relato como trama |
| `version_paralela` | Relato de la misma tradición sin dependencia demostrada | Versión de otra tradición con episodios distintos | Una versión que depende demostradamente del texto (usar el tipo que corresponda) |

### Académicas

| Tipo | Definición |
|---|---|
| `cita_academica` | Cita bibliográfica formal sin valoración |
| `discute` | Analiza o debate ampliamente el destino |
| `critica` | Valora críticamente el destino |
| `apoya` | Respalda sus tesis |
| `refuta` | Rechaza sus tesis |
| `extiende` | Amplía o desarrolla su trabajo |
| `usa_como_fuente` | Se apoya en él como fuente de datos o argumentos |
| `interpreta` | Ofrece una lectura interpretativa de una obra (típico de artículos sobre literatura) |

Ejemplo positivo de `refuta`: un artículo que sostiene que otro malinterpreta el pasaje. Negativo: un artículo que solo lo cita en la bibliografía (`cita_academica`).

## Árbol de decisión

1. ¿El origen es un artículo o libro académico? Sí: usa los tipos académicos (`cita_academica`, `discute`, `critica`, `apoya`, `refuta`, `extiende`, `usa_como_fuente`, `interpreta`). No: sigue.
2. ¿Hay coincidencia léxica con el destino?
   - Literal: `cita`.
   - Parcial con el mismo contenido: `parafrasis`.
3. ¿Transforma el relato entero?
   - Mantiene sus valores: `reescritura`.
   - Los invierte o los parodia: `inversion_parodia`.
4. ¿Explica o interpreta el relato como tal? `comentario_exegesis`.
5. ¿Es un relato de la misma tradición sin dependencia demostrada? `version_paralela`.
6. ¿Evoca el relato sin citarlo? `alusion`. ¿Solo lo nombra? `mencion`.
7. Si nada encaja, no registres la relación y anota la duda en un archivo de pendientes.

## Certeza

- **alta**: la relación es explícita (cita, mención, título, declaración del autor) o la evidencia es inequívoca.
- **media**: la relación es muy probable por indicios textuales o contextuales, pero no explícita o está debatida.
- **baja**: hipótesis plausible que falta verificar. Anótalo en `notas` ("hipótesis a verificar").

## Evidencia

- `loc_origen` y `loc_destino`: capítulo, página, verso o id OSIS (`Gen.4.10`). `loc_destino` usa OSIS.
- `evidencia`: descripción propia breve o fragmento literal de **una o dos frases como máximo**. Para obras con derechos, prefiere describir con tus palabras; el validador avisa si pasa de 300 caracteres.
- No copies capítulos, páginas ni citas largas.
- `mediada_por`: id de la obra que sirvió de intermediaria (opcional).

## Convenciones de ids

- Obras: slug en minúsculas con guiones, `autor-titulo-año` (`byron-cain-1821`). Para fuentes anónimas, `nombre-capitulo` (`genesis-4`).
- Relaciones: `r0001`, `r0002`, siguiente número libre. Las extraídas de TEI llevan prefijo `t`.
- Vocabularios: minúsculas con guion bajo (`m_envidia`).
- Anotadores: `anotadorA`, `anotadorB`.
- Fechas: AAAA-MM-DD. `anio`: entero, negativo para a. C.

## Cómo agregar una obra

1. Añade una fila en `data/obras.csv` con id nuevo, `tipo_obra` válido y `derechos`.
2. Si hay texto TEI, `capa_tei = si` (solo dominio público).
3. Ejecuta `python scripts/validar.py`.

## Cómo agregar una relación

1. Comprueba que origen y destino están en `obras.csv`.
2. Añade una fila en `data/relaciones.csv` con el siguiente id libre.
3. Elige el tipo con el árbol de decisión y la certeza.
4. Escribe localizaciones y evidencia breve; añade motivos de `motivos.csv`, separados por `;`.
5. Pon tu anotador y la fecha.
6. Ejecuta `python scripts/validar.py` y corrige errores.
