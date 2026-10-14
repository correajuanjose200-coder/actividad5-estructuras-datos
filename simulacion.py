"""Actividad 5 - Parte B: simulación de la sala de cómputo.

Un solo puesto de atención (un técnico). Tiempo en minutos, jornada de 8 h.
Llegadas: proceso de Poisson (tiempos entre llegadas exponenciales).
Mezcla de solicitudes: 20 % urgentes (0), 30 % normales (1), 50 % bajas (2).
Servicio: exponencial. La sala está muy cargada (~90 % de utilización),
que es cuando las estrategias se diferencian.

ESCENARIOS
  1. FIFO: una sola cola, se atiende por orden de llegada.
  2. PRIORIDAD + ENVEJECIMIENTO: ColaPrioridad de la Parte A (umbral 30 min).
  (3. PRIORIDAD ESTRICTA, sin envejecimiento: solo como referencia para ver
      la inanición; no es una estrategia que se recomiende.)

Todos los escenarios usan EXACTAMENTE las mismas llegadas en cada réplica
(misma semilla), para que la comparación sea justa.
"""
import random

from cola_prioridad import Cola, ColaPrioridad, Solicitud

DURACION = 480
LLEGADA_MEDIA = 4.0
SERVICIO_MEDIO = 3.6
PROB_NIVEL = (0.2, 0.3, 0.5)
UMBRAL = 30
REPLICAS = 200


def generar_llegadas(semilla):
    rnd = random.Random(semilla)
    llegadas, t, n = [], 0.0, 0
    while True:
        t += rnd.expovariate(1.0 / LLEGADA_MEDIA)
        if t >= DURACION:
            return llegadas
        u = rnd.random()
        nivel = 0 if u < PROB_NIVEL[0] else (1 if u < PROB_NIVEL[0] + PROB_NIVEL[1] else 2)
        n += 1
        llegadas.append((Solicitud("s%d" % n, nivel, t), rnd.expovariate(1.0 / SERVICIO_MEDIO)))


class ColaFIFO:
    """Adaptador: misma interfaz que ColaPrioridad, pero ignora el nivel."""

    def __init__(self):
        self._c = Cola()

    def encolar(self, s):
        self._c.encolar(s)

    def desencolar(self, ahora):
        return self._c.desencolar()

    def esta_vacia(self):
        return self._c.esta_vacia()


def _servicio_por_solicitud(llegadas):
    return {id(s): sv for s, sv in llegadas}


def simular(cola, llegadas):
    """Atiende TODAS las solicitudes (también tras las 8 h, hasta vaciar la cola).
    Devuelve una lista de (nivel, espera en minutos)."""
    dur = _servicio_por_solicitud(llegadas)
    esperas = []
    i, n, ahora = 0, len(llegadas), 0.0
    while i < n or not cola.esta_vacia():
        while i < n and llegadas[i][0].llegada <= ahora:
            cola.encolar(llegadas[i][0])
            i += 1
        if cola.esta_vacia():
            ahora = llegadas[i][0].llegada
            continue
        s = cola.desencolar(ahora)
        esperas.append((s.nivel, ahora - s.llegada))
        ahora += dur[id(s)]
    return esperas


ESCENARIOS = [
    ("FIFO", lambda: ColaFIFO()),
    ("Prioridad + envejecimiento", lambda: ColaPrioridad(umbral=UMBRAL)),
    ("Prioridad estricta (referencia)", lambda: ColaPrioridad(umbral=None)),
]


def correr():
    acum = {nombre: {"media": [], "peor": [], "peor_por_nivel": [[], [], []],
                     "media_por_nivel": [[], [], []]} for nombre, _ in ESCENARIOS}
    for r in range(REPLICAS):
        for nombre, fabrica in ESCENARIOS:
            # Cada escenario necesita sus propias Solicitud: se regeneran con la misma semilla
            ll = generar_llegadas(r)
            esperas = simular(fabrica(), ll)
            todas = [e for _, e in esperas]
            a = acum[nombre]
            a["media"].append(sum(todas) / len(todas))
            a["peor"].append(max(todas))
            for nivel in range(3):
                es = [e for nv, e in esperas if nv == nivel]
                a["media_por_nivel"][nivel].append(sum(es) / len(es) if es else 0.0)
                a["peor_por_nivel"][nivel].append(max(es) if es else 0.0)
    return acum


def prom(xs):
    return sum(xs) / len(xs)


def imprimir_tabla(acum):
    print("Réplicas: %d | jornada %d min | llegada media %.1f | servicio medio %.1f"
          % (REPLICAS, DURACION, LLEGADA_MEDIA, SERVICIO_MEDIO))
    print()
    print("| Escenario | Espera media (min) | Peor espera, promedio de réplicas (min) | Peor espera absoluta (min) |")
    print("|---|---|---|---|")
    for nombre, _ in ESCENARIOS:
        a = acum[nombre]
        print("| %s | %.1f | %.1f | %.1f |" % (nombre, prom(a["media"]), prom(a["peor"]), max(a["peor"])))
    print()
    print("Por nivel (media / peor promedio, min):")
    print("| Escenario | Urgente | Normal | Baja |")
    print("|---|---|---|---|")
    for nombre, _ in ESCENARIOS:
        a = acum[nombre]
        celdas = ["%.1f / %.1f" % (prom(a["media_por_nivel"][k]), prom(a["peor_por_nivel"][k])) for k in range(3)]
        print("| %s | %s |" % (nombre, " | ".join(celdas)))


if __name__ == "__main__":
    imprimir_tabla(correr())
