# Resultados de la simulación

Un técnico, jornada de 8 h, 200 réplicas con las mismas llegadas para todos los
escenarios. Llegada media cada 4 min, servicio medio 3,6 min (sala al ~90 %).
20 % urgentes, 30 % normales, 50 % bajas. Envejecimiento: sube un nivel cada 30 min.
Se ejecuta con `python simulacion.py`.

| Escenario | Espera media (min) | Peor espera, promedio de réplicas (min) | Peor espera absoluta (min) |
|---|---|---|---|
| FIFO | 18,0 | 49,2 | 162,1 |
| Prioridad + envejecimiento | 17,9 | 59,2 | 162,1 |
| Prioridad estricta (referencia, sin envejecimiento) | 17,9 | 82,3 | 242,4 |

Por nivel (media / peor caso promedio, en min):

| Escenario | Urgente | Normal | Baja |
|---|---|---|---|
| FIFO | 18,1 / 44,3 | 17,8 / 45,9 | 18,1 / 47,4 |
| Prioridad + envejecimiento | 7,7 / 28,7 | 14,3 / 43,5 | 24,2 / 59,0 |
| Prioridad estricta | 3,6 / 13,9 | 6,3 / 26,4 | 30,8 / 82,2 |

## Análisis

**La media no cambia; la prioridad solo reparte la espera.** Con un solo técnico
que nunca se queda ocioso mientras hay cola, el trabajo total es el mismo sin
importar el orden. Por eso la espera media es ~18 min en los tres escenarios.
Lo que cambia es *quién* espera: los urgentes pasan de 18,1 a 7,7 min (con
envejecimiento), y esa mejora se paga con las solicitudes bajas, que pasan de
18,1 a 24,2 min.

**El peor caso sí empeora, y es el hallazgo.** Con envejecimiento, la peor espera
promedio sube de 49,2 a 59,2 min respecto a FIFO. En FIFO nadie es adelantado,
así que la espera de cada uno depende solo de la cola que encontró. Con
prioridad, una solicitud baja puede ser adelantada por varias urgentes que llegan
después, y el envejecimiento solo la protege hasta cierto punto.

**Sin envejecimiento la cola de prioridad es peligrosa.** La prioridad estricta
da los mejores números a los urgentes (3,6 min), pero las bajas esperan 30,8 min
de media y hasta 242 min en el peor caso: una persona esperó cuatro horas en una
jornada de ocho. Es la espera indefinida que el mecanismo debe evitar.

**El umbral es una perilla.** Con 10 min el envejecimiento era tan rápido que la
cola se comportaba casi como FIFO (urgentes 15,4 min, nada que ganar). Con 30 min
se conserva casi toda la ventaja de los urgentes y el peor caso queda 23 min por
debajo de la prioridad estricta. Un umbral mayor acerca el comportamiento a la
prioridad estricta; uno menor, a FIFO.

**Conclusión.** Si el objetivo es que exámenes y entregas urgentes no esperen,
prioridad con envejecimiento es mejor que FIFO, aceptando que el peor caso de
las bajas empeora ~10 min. Si el objetivo fuera minimizar el peor caso de
cualquiera, FIFO gana. Prioridad estricta no es aceptable por la inanición.

Nota: el peor caso absoluto de FIFO y de envejecimiento coincide (162,1 min) porque
ocurre en la misma réplica (la 93, con una ráfaga de llegadas) y en ambos casos
lo sufre una solicitud de nivel baja que sale exactamente en el mismo instante;
en esa réplica la prioridad estricta llega a 230,8 min. Una sola réplica extrema
no define el resultado: por eso se reporta también el promedio de las 200 réplicas.
