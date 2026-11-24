import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))

import tei_a_relaciones  # noqa: E402
import validar  # noqa: E402


def copiar_datos(tmp_path: Path) -> Path:
    shutil.copytree(RAIZ / "data", tmp_path / "data")
    return tmp_path


def reemplazar(ruta: Path, viejo: str, nuevo: str, veces: int = 1):
    texto = ruta.read_text(encoding="utf-8")
    assert viejo in texto
    ruta.write_text(texto.replace(viejo, nuevo, veces), encoding="utf-8")


def test_datos_del_repo_validan():
    errores, _ = validar.validar(RAIZ)
    assert errores == []


def test_id_duplicado(tmp_path):
    raiz = copiar_datos(tmp_path)
    reemplazar(raiz / "data" / "relaciones.csv", "r0002,", "r0001,")
    errores, _ = validar.validar(raiz)
    assert any("duplicado" in e for e in errores)


def test_tipo_relacion_inexistente(tmp_path):
    raiz = copiar_datos(tmp_path)
    reemplazar(raiz / "data" / "relaciones.csv", ",cita,", ",tipo_falso,")
    errores, _ = validar.validar(raiz)
    assert any("tipo_relacion" in e for e in errores)


def test_destino_inexistente(tmp_path):
    raiz = copiar_datos(tmp_path)
    reemplazar(raiz / "data" / "relaciones.csv", "hebreos-11,genesis-4", "hebreos-11,no-existe")
    errores, _ = validar.validar(raiz)
    assert any("destino" in e for e in errores)


def test_extraer_plantilla():
    filas = tei_a_relaciones.extraer(RAIZ)
    assert isinstance(filas, list)
    fila = next(f for f in filas if f["origen"] == "plantilla-tei")
    assert set(fila) == set(tei_a_relaciones.CAMPOS)
    assert fila["destino"] == "genesis-4"
    assert fila["loc_destino"] == "Gen.4.10"
    assert fila["certeza"] == "alta"
    assert fila["motivos"] == "m_sangre_clama"
    assert fila["anotador"] == "anotadorA"
