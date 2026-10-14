import pytest
from cola_prioridad import Cola, ColaPrioridad, Solicitud


def test_cola_fifo():
    c = Cola()
    for x in (1, 2, 3):
        c.encolar(x)
    assert [c.desencolar() for _ in range(3)] == [1, 2, 3]
    with pytest.raises(IndexError):
        c.desencolar()


def test_tres_niveles_en_orden():
    q = ColaPrioridad()
    q.encolar(Solicitud("baja", 2, 0))
    q.encolar(Solicitud("normal", 1, 0))
    q.encolar(Solicitud("urgente", 0, 0))
    assert [q.desencolar(0).nombre for _ in range(3)] == ["urgente", "normal", "baja"]


def test_fifo_dentro_del_nivel():
    q = ColaPrioridad()
    q.encolar(Solicitud("a", 1, 0))
    q.encolar(Solicitud("b", 1, 1))
    assert q.desencolar(1).nombre == "a"
    assert q.desencolar(1).nombre == "b"


def test_nivel_invalido_y_cola_vacia():
    with pytest.raises(ValueError):
        Solicitud("x", 3, 0)
    with pytest.raises(IndexError):
        ColaPrioridad().desencolar(0)


def test_inanicion_sin_envejecimiento():
    """Sin envejecimiento, la baja nunca sale mientras lleguen urgentes."""
    q = ColaPrioridad(umbral=None)
    q.encolar(Solicitud("baja", 2, 0))
    for t in range(1, 200):
        q.encolar(Solicitud("urg%d" % t, 0, t))
        assert q.desencolar(t).nombre != "baja"
    assert len(q) == 1  # la baja sigue esperando


def test_envejecimiento_evita_espera_indefinida():
    """Con envejecimiento, la baja sale como máximo tras 2*umbral minutos
    aun con urgentes llegando sin parar."""
    umbral = 10
    q = ColaPrioridad(umbral=umbral)
    q.encolar(Solicitud("baja", 2, 0))
    salida = None
    for t in range(1, 200):
        q.encolar(Solicitud("urg%d" % t, 0, t))
        if q.desencolar(t).nombre == "baja":
            salida = t
            break
    assert salida is not None
    assert salida <= 2 * umbral + 1
