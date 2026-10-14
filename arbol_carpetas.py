"""Actividad 5 - Parte C: el árbol de carpetas.

Modelo: cada Nodo es una carpeta o una entrega (archivo).
- Una entrega es una hoja (es_entrega=True).
- Una carpeta tiene una lista de hijos.

Restricciones: conteo y profundidad por recursión; listado por niveles con
nuestra propia cola (sin collections.deque, sin heapq).
"""


class Nodo:
    def __init__(self, nombre, es_entrega=False):
        self.nombre = nombre
        self.es_entrega = es_entrega
        self.hijos = []

    def agregar(self, hijo):
        self.hijos.append(hijo)
        return hijo


# ---------- Cola FIFO propia (lista enlazada) ----------
# Si en la Parte A ya tienes una cola FIFO, impórtala en vez de esta.
class _NodoCola:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Cola:
    def __init__(self):
        self._frente = None
        self._final = None
        self._tam = 0

    def encolar(self, dato):
        nuevo = _NodoCola(dato)
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

    def esta_vacia(self):
        return self._tam == 0


class Pila:
    """Pila propia, solo para la Parte D (comparación)."""

    def __init__(self):
        self._items = []

    def apilar(self, dato):
        self._items.append(dato)

    def desapilar(self):
        if not self._items:
            raise IndexError("pila vacía")
        return self._items.pop()

    def esta_vacia(self):
        return not self._items


# ---------- Consulta 1: conteo (recursión) ----------
def contar_entregas(nodo):
    """Total de entregas bajo `nodo` (incluyéndolo si él mismo es entrega)."""
    if nodo is None:                         # caso base: árbol vacío
        return 0
    if nodo.es_entrega:                      # caso base: hoja que es entrega
        return 1
    total = 0
    for hijo in nodo.hijos:                  # caso recursivo
        total += contar_entregas(hijo)
    return total


# ---------- Consulta 2: ruta más profunda (recursión) ----------
def ruta_mas_profunda(nodo):
    """Lista de nombres desde `nodo` hasta la hoja más profunda.
    Si hay empate gana la primera encontrada (comparación estricta).
    Árbol vacío (None) -> []."""
    if nodo is None:                         # caso base: árbol vacío
        return []
    mejor = []
    for hijo in nodo.hijos:
        candidata = ruta_mas_profunda(hijo)
        if len(candidata) > len(mejor):
            mejor = candidata
    return [nodo.nombre] + mejor             # sin hijos: mejor == [] (caso base)


def profundidad_maxima(nodo):
    return len(ruta_mas_profunda(nodo))


# ---------- Consulta 3: listado por niveles (cola, sin recursión) ----------
def listar_por_niveles(raiz):
    """Devuelve una lista de niveles; cada nivel es una lista de nombres."""
    niveles = []
    if raiz is None:                         # árbol vacío
        return niveles
    cola = Cola()
    cola.encolar((raiz, 0))
    while not cola.esta_vacia():
        nodo, nivel = cola.desencolar()
        if nivel == len(niveles):
            niveles.append([])
        niveles[nivel].append(nodo.nombre)
        for hijo in nodo.hijos:
            cola.encolar((hijo, nivel + 1))
    return niveles


# ---------- Parte D: mismo recorrido, pero con pila ----------
def recorrer_con_pila(raiz):
    """Cambia la cola por una pila. Devuelve los nombres en orden de visita."""
    visita = []
    if raiz is None:
        return visita
    pila = Pila()
    pila.apilar(raiz)
    while not pila.esta_vacia():
        nodo = pila.desapilar()
        visita.append(nodo.nombre)
        for hijo in nodo.hijos:             # sin invertir: el último hijo sale primero
            pila.apilar(hijo)
    return visita


# ---------- Árbol de prueba ----------
def construir_arbol_prueba():
    ing = Nodo("Ingenieria")
    sw = ing.agregar(Nodo("Software"))
    sis = ing.agregar(Nodo("Sistemas"))

    ed = sw.agregar(Nodo("EstructurasDatos"))
    ed1 = ed.agregar(Nodo("2026-1"))
    ed1.agregar(Nodo("ana.py", True))
    ed1.agregar(Nodo("luis.py", True))
    ed.agregar(Nodo("2026-2")).agregar(Nodo("marta.py", True))

    bd = sw.agregar(Nodo("BasesDatos"))
    bd1 = bd.agregar(Nodo("2026-1"))
    bd1.agregar(Nodo("pedro.py", True))
    bd1.agregar(Nodo("sofia.py", True))
    bd1.agregar(Nodo("correcciones")).agregar(Nodo("juan.py", True))

    sis.agregar(Nodo("Redes")).agregar(Nodo("2026-1")).agregar(Nodo("carla.py", True))
    return ing


if __name__ == "__main__":
    raiz = construir_arbol_prueba()
    print("Entregas:", contar_entregas(raiz))
    print("Ruta más profunda:", "/".join(ruta_mas_profunda(raiz)))
    print("Profundidad:", profundidad_maxima(raiz))
    for i, nivel in enumerate(listar_por_niveles(raiz)):
        print(f"Nivel {i}:", nivel)
    print("Con pila:", recorrer_con_pila(raiz))
