from simulacion import (generar_llegadas, simular, ColaFIFO, ColaPrioridad,
                        UMBRAL)


def test_llegadas_reproducibles():
    a = [(s.llegada, s.nivel, sv) for s, sv in generar_llegadas(1)]
    b = [(s.llegada, s.nivel, sv) for s, sv in generar_llegadas(1)]
    assert a == b and len(a) > 0


def test_se_atienden_todas_y_esperas_no_negativas():
    for fabrica in (ColaFIFO, lambda: ColaPrioridad(umbral=UMBRAL)):
        ll = generar_llegadas(3)
        esperas = simular(fabrica(), ll)
        assert len(esperas) == len(ll)
        assert all(e >= -1e-9 for _, e in esperas)


def test_prioridad_favorece_urgentes():
    ll1, ll2 = generar_llegadas(5), generar_llegadas(5)
    fifo = [e for n, e in simular(ColaFIFO(), ll1) if n == 0]
    prio = [e for n, e in simular(ColaPrioridad(umbral=UMBRAL), ll2) if n == 0]
    assert sum(prio) / len(prio) < sum(fifo) / len(fifo)
