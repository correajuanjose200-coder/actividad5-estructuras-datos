from arbol_carpetas import (Nodo, construir_arbol_prueba, contar_entregas,
                            ruta_mas_profunda, profundidad_maxima,
                            listar_por_niveles, recorrer_con_pila, Cola)
import pytest


def test_conteo_total():
    assert contar_entregas(construir_arbol_prueba()) == 7


def test_conteo_subarbol():
    raiz = construir_arbol_prueba()
    software = raiz.hijos[0]
    assert contar_entregas(software) == 6
    assert contar_entregas(raiz.hijos[1]) == 1


def test_conteo_carpeta_vacia_y_hoja():
    assert contar_entregas(Nodo("vacia")) == 0
    assert contar_entregas(Nodo("x.py", True)) == 1


def test_ruta_mas_profunda():
    raiz = construir_arbol_prueba()
    assert ruta_mas_profunda(raiz) == ["Ingenieria", "Software", "BasesDatos",
                                       "2026-1", "correcciones", "juan.py"]
    assert profundidad_maxima(raiz) == 6


def test_niveles():
    n = listar_por_niveles(construir_arbol_prueba())
    assert n[0] == ["Ingenieria"]
    assert n[1] == ["Software", "Sistemas"]
    assert n[2] == ["EstructurasDatos", "BasesDatos", "Redes"]
    assert n[3] == ["2026-1", "2026-2", "2026-1", "2026-1"]
    assert n[4] == ["ana.py", "luis.py", "marta.py", "pedro.py", "sofia.py",
                    "correcciones", "carla.py"]
    assert n[5] == ["juan.py"]


def test_pila_difiere_de_cola():
    raiz = construir_arbol_prueba()
    plano = [x for nivel in listar_por_niveles(raiz) for x in nivel]
    assert recorrer_con_pila(raiz) != plano


def test_cola_fifo_y_vacia():
    c = Cola()
    c.encolar(1); c.encolar(2)
    assert c.desencolar() == 1
    assert c.desencolar() == 2
    with pytest.raises(IndexError):
        c.desencolar()


# ---- casos límite pedidos por la rúbrica ----
def test_arbol_vacio():
    assert contar_entregas(None) == 0
    assert ruta_mas_profunda(None) == []
    assert profundidad_maxima(None) == 0
    assert listar_por_niveles(None) == []
    assert recorrer_con_pila(None) == []


def test_un_solo_nodo_entrega():
    n = Nodo("solo.py", True)
    assert contar_entregas(n) == 1
    assert ruta_mas_profunda(n) == ["solo.py"]
    assert profundidad_maxima(n) == 1
    assert listar_por_niveles(n) == [["solo.py"]]


def test_un_solo_nodo_carpeta_vacia():
    n = Nodo("vacia")
    assert contar_entregas(n) == 0
    assert profundidad_maxima(n) == 1
    assert listar_por_niveles(n) == [["vacia"]]
