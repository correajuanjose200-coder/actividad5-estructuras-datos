# Recorridos del árbol de carpetas

## Árbol de prueba

```
Ingenieria
├── Software
│   ├── EstructurasDatos
│   │   ├── 2026-1
│   │   │   ├── ana.py
│   │   │   └── luis.py
│   │   └── 2026-2
│   │       └── marta.py
│   └── BasesDatos
│       └── 2026-1
│           ├── pedro.py
│           ├── sofia.py
│           └── correcciones
│               └── juan.py
└── Sistemas
    └── Redes
        └── 2026-1
            └── carla.py
```

Resultados a mano: 7 entregas; ruta más profunda
`Ingenieria/Software/BasesDatos/2026-1/correcciones/juan.py` (6 nodos).

## Recorrido por niveles (con cola)

```
Nivel 0: ['Ingenieria']
Nivel 1: ['Software', 'Sistemas']
Nivel 2: ['EstructurasDatos', 'BasesDatos', 'Redes']
Nivel 3: ['2026-1', '2026-2', '2026-1', '2026-1']
Nivel 4: ['ana.py', 'luis.py', 'marta.py', 'pedro.py', 'sofia.py', 'correcciones', 'carla.py']
Nivel 5: ['juan.py']
```

## Mismo recorrido con pila

```
Ingenieria, Sistemas, Redes, 2026-1, carla.py, Software, BasesDatos, 2026-1,
correcciones, juan.py, sofia.py, pedro.py, EstructurasDatos, 2026-2, marta.py,
2026-1, luis.py, ana.py
```

## ¿Por qué difieren?

Una cola es FIFO: el primero que entra es el primero que sale. Al visitar un
nodo encolamos sus hijos *al final*, detrás de todo lo que ya esperaba, así que
ningún nodo del nivel k+1 se visita antes de terminar el nivel k. Eso produce
el listado nivel por nivel.

Una pila es LIFO: el último que entra es el primero que sale. Los hijos recién
apilados quedan *encima* de lo que esperaba, así que se visitan de inmediato:
el recorrido se mete a fondo por una rama (Ingenieria → Sistemas → Redes →
2026-1 → carla.py) y solo después regresa a las ramas pendientes. Es un
recorrido en profundidad, no por niveles. Además, como el último hijo apilado
sale primero, los hermanos salen en orden inverso (Sistemas antes que
Software).

Por eso el informe por niveles necesita una cola: la política FIFO es la que
garantiza que se agoten los nodos cercanos a la raíz antes que los lejanos.
