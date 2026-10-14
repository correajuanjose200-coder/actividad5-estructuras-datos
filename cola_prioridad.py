"""Actividad 5 - Parte A: cola de prioridad con tres niveles y envejecimiento.

Sin heapq. Se construye con tres colas FIFO (listas enlazadas propias).

NIVELES (0 = más urgente):
    0 = URGENTE  (exámenes, entregas con fecha límite hoy)
    1 = NORMAL   (clases y prácticas programadas)
    2 = BAJA     (uso libre, consultas)

PROBLEMA: con prioridad estricta, si siempre llegan solicitudes urgentes,
las de nivel BAJA nunca se atienden (espera indefinida / inanición).

MECANISMO ELEGIDO: ENVEJECIMIENTO.
    prioridad_efectiva = max(0, nivel - espera // UMBRAL)
Cada UMBRAL minutos de espera, la solicitud "sube" un nivel. Una solicitud de
nivel 2 llega a prioridad efectiva 0 tras 2 * UMBRAL minutos; desde ahí solo
compite por orden de llegada, así que su espera queda acotada.

POR QUÉ SOLO SE COMPARAN LOS FRENTES DE LAS TRES COLAS: dentro de cada cola
las solicitudes están en orden de llegada, así que la más antigua (el frente)
es también la de menor prioridad efectiva de esa cola. Basta comparar tres
candidatos: costo O(1) por desencolar y sin mover elementos entre colas.
Desempate: gana la que llegó primero (justo y determinista).

JUSTIFICACIÓN FRENTE A OTRAS OPCIONES: la reserva de turnos (cada k urgentes,
atender una baja) es más simple pero ignora cuánto lleva esperando cada
solicitud; el envejecimiento sí mide la espera real.
"""

NIVELES = 3
UMBRAL_DEFECTO = 30  # minutos de espera para subir un nivel


class Solicitud:
    def __init__(self, nombre, nivel, llegada):
        if nivel < 0 or nivel >= NIVELES:
            raise ValueError("nivel debe estar entre 0 y %d" % (NIVELES - 1))
        self.nombre = nombre
        self.nivel = nivel
        self.llegada = llegada

    def __repr__(self):
        return "Solicitud(%s, nivel=%d, llegada=%s)" % (
            self.nombre, self.nivel, self.llegada)


class _Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    """Cola FIFO propia (lista enlazada). Sin collections.deque."""

    def __init__(self):
        self._frente = None
        self._final = None
        self._tam = 0

    def encolar(self, dato):
        nuevo = _Nodo(dato)
        if self._final is None:
            self._frente = self._final = nuevo
        else:
            self._final.siguiente = nuevo
            self._final = nuevo
        self._tam += 1

    def desencolar(self):
        if self._frente is None:
            raise IndexError("cola vacía")
        dato = self._frente.dato
        self._frente = self._frente.siguiente
        if self._frente is None:
            self._final = None
        self._tam -= 1
        return dato

    def ver_frente(self):
        if self._frente is None:
            raise IndexError("cola vacía")
        return self._frente.dato

    def esta_vacia(self):
        return self._tam == 0

    def __len__(self):
        return self._tam


class ColaPrioridad:
    """Tres niveles + envejecimiento. umbral=None desactiva el envejecimiento
    (prioridad estricta), útil solo para demostrar la inanición."""

    def __init__(self, umbral=UMBRAL_DEFECTO):
        self.umbral = umbral
        self._colas = [Cola() for _ in range(NIVELES)]

    def encolar(self, solicitud):
        self._colas[solicitud.nivel].encolar(solicitud)

    def esta_vacia(self):
        return all(c.esta_vacia() for c in self._colas)

    def __len__(self):
        return sum(len(c) for c in self._colas)

    def prioridad_efectiva(self, solicitud, ahora):
        if self.umbral is None:
            return solicitud.nivel
        subidas = (ahora - solicitud.llegada) // self.umbral
        return max(0, solicitud.nivel - subidas)

    def desencolar(self, ahora):
        """Saca la solicitud con menor (prioridad efectiva, llegada)."""
        mejor_nivel = None
        mejor_clave = None
        for nivel in range(NIVELES):
            if self._colas[nivel].esta_vacia():
                continue
            frente = self._colas[nivel].ver_frente()
            clave = (self.prioridad_efectiva(frente, ahora), frente.llegada)
            if mejor_clave is None or clave < mejor_clave:
                mejor_clave, mejor_nivel = clave, nivel
        if mejor_nivel is None:
            raise IndexError("cola vacía")
        return self._colas[mejor_nivel].desencolar()
