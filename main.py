"""
Proyecto para Simulación y Modelos, números pseudoaleatorios.
Omar Zabala y Cristian González
"""

"""
Algoritmo 1: Cuadrados medios.
Este algoritmo no congruencial requiere un número entero (semilla) de D dígitos, el cual se eleva al cuadrado
para extraer los D dígitos del centro. El primer número pseudoaleatorio r[1] se obtiene anteponiendo "0." A
esos dígitos centrados. El proceso se repite elevando al cuadrado los dígitos centrales obtenidos
anteriormente hasta generar los n números requeridos.

Pasos:
1. Seleccionar la semilla X[0] con D dígitos (D > 3).
2. Calcular Y[0] = (X[0])^2, extraer los D dígitos del centro para X[1] y formar r[1] = 0.X[1].
3. Para cada paso i, calcular Y[i] = (X[i])^2, extraer los D dígitos del centro para X[i+1] y definir
r[i+1] = 0.X[i+1].
4. Repetir hasta obtener los n números requeridos.

Nota: Si el resultado Y[i] no alcanza la cantidad suficiente de dígitos para extraer los D del centro,
se completan con ceros a la izquierda.

Ejemplo simplificado (X[0] = 5735, D = 4):
Y[0] = (5735)^2 = 32890225 -> X[1] = 8902 -> r[1] = 0.8902
Y[1] = (8902)^2 = 79245604 -> X[2] = 2456 -> r[2] = 0.2456
Y[2] = (2456)^2 = 06031936 -> X[3] = 0319 -> r[3] = 0.0319
Y[3] = (0319)^2 = 00101761 -> X[4] = 0176 -> r[4] = 0.0176
Y[4] = (0176)^2 = 00030976 -> X[5] = 3097 -> r[5] = 0.3097

Desventaja: Este algoritmo tiende a degradarse rápidamente si se eligen semillas donde el centro se vuelve cero
(por ejemplo, con X[0] = 1000, X[1] = 0000 y r[1] = 0.0000).
"""

def cuadrados_medios():
    pass

"""
Algoritmo 2: Productos medios.
Este algoritmo no congruencial requiere dos semillas enteras de D dígitos. En lugar de elevar al cuadrado,
se multiplican ambas semillas y del producto obtenido se extraen los D dígitos del centro para formar el
primer numero pseudoaleatorio r[1]. Luego se descarta la semilla mas antigua y se multiplica la segunda
semilla por el nuevo valor de D dígitos para obtener r[2], repitiendo el proceso secuencialmente.

Pasos:
1. Seleccionar la primera semilla X[0] con D dígitos (D > 3).
2. Seleccionar la segunda semilla X[1] con D dígitos (D > 3).
3. Calcular Y[0] = X[0] * X[1], extraer los D dígitos del centro para X[2] y formar r[1] = 0.X[2].
4. Para cada paso i (iniciando en i = 0), calcular Y[i+1] = X[i+1] * X[i+2], extraer los D dígitos del
centro para X[i+3] y definir r[i+2] = 0.X[i+3].
5. Repetir hasta obtener los n números requeridos.

Nota: Si el resultado Y[i] no alcanza la cantidad suficiente de dígitos para extraer los D del centro,
se completan con ceros a la izquierda.

Ejemplo simplificado (X[0] = 5015, X[1] = 5734, D = 4):
Y[0] = (5015)(5734) = 28756010 -> X[2] = 7560 -> r[1] = 0.7560
Y[1] = (5734)(7560) = 43349040 -> X[3] = 3490 -> r[2] = 0.3490
Y[2] = (7560)(3490) = 26384400 -> X[4] = 3844 -> r[3] = 0.3844
Y[3] = (3490)(3844) = 13415560 -> X[5] = 4155 -> r[4] = 0.4155
Y[4] = (3844)(4155) = 15971820 -> X[6] = 9718 -> r[5] = 0.9718
"""

def productos_medios():
    pass

"""
Algoritmo 3: Multiplicador constante.
Este algoritmo no congruencial es similar al de productos medios. En lugar de multiplicar dos semillas variables,
utiliza una constante fija "a" y una semilla X[0], ambas de D dígitos. Se multiplican "a" por la semilla actual
para obtener Y[i], se extraen los D dígitos del centro para formar X[i+1], y se calcula r[i+1] = 0.X[i+1].

Pasos:
1. Seleccionar una semilla X[0] con D dígitos (D > 3).
2. Seleccionar una constante a con D dígitos (D > 3).
3. Calcular Y[0] = a * X[0], extraer los D dígitos del centro para X[1] y formar r[1] = 0.X[1].
4. Para cada paso i (iniciando en i = 0), calcular Y[i+1] = a * X[i+1], extraer los D dígitos del centro para
X[i+2] y definir r[i+2] = 0.X[i+2].
5. Repetir hasta obtener los n números requeridos.

Nota: Si Y[i] no alcanza los dígitos necesarios para extraer los D del centro, se completan con ceros a la
izquierda.

Ejemplo simplificado (X[0] = 9803, a = 6965, D = 4):
Y[0] = (6965)(9803) = 68277895 -> X[1] = 2778 -> r[1] = 0.2778
Y[1] = (6965)(2778) = 19348770 -> X[2] = 3487 -> r[2] = 0.3487
Y[2] = (6965)(3487) = 24286955 -> X[3] = 2869 -> r[3] = 0.2869
Y[3] = (6965)(2869) = 19982585 -> X[4] = 9825 -> r[4] = 0.9825
Y[4] = (6965)(9825) = 68431125 -> X[5] = 4311 -> r[5] = 0.4311
"""

def multiplicador_constante():
    pass

"""
Algoritmo 4: Congruencial lineal.
Este algoritmo genera una secuencia de números enteros mediante la ecuación recursiva:
    X[i+1] = (a * X[i] + c) mod m
Para obtener números pseudoaleatorios en el intervalo (0,1) se utiliza:
    r[i+1] = X[i+1] / (m - 1)

Parámetros:
* X[0]: Semilla inicial (X[0] > 0)
* a: Constante multiplicativa (a > 0)
* c: Constante aditiva (c > 0)
* m: Modulo (m > 0)

Condiciones para periodo de vida máximo (N = m = 2^g):
* m = 2^g (g entero)
* a = 1 + 4k (k entero)
* c debe ser relativamente primo a m

Pasos:
1. Seleccionar los parámetros X[0], a, c y m.
2. Calcular X[i+1] = (a * X[i] + c) mod m.
3. Calcular r[i+1] = X[i+1] / (m - 1).
4. Repetir hasta obtener la cantidad deseada de números o hasta repetir la semilla X[0].

Ejemplo simplificado (X[0] = 37, a = 19, c = 33, m = 100):
X[1] = (19 * 37 + 33) mod 100 = 36 -> r[1] = 36 / 99 = 0.3636
X[2] = (19 * 36 + 33) mod 100 = 17 -> r[2] = 17 / 99 = 0.1717
X[3] = (19 * 17 + 33) mod 100 = 56 -> r[3] = 56 / 99 = 0.5656
X[4] = (19 * 56 + 33) mod 100 = 97 -> r[4] = 97 / 99 = 0.9797
"""
"""
Algoritmo 5: Congruencial multiplicativo
Deriva del algoritmo congruencial lineal al establecer c = 0. Su ecuación recursiva es:
 X[i+1] = (a * X[i]) mod m
Para obtener números entre (0,1) se utiliza:
 r[i+1] = X[i+1] / (m - 1)

Condiciones para periodo de vida máximo (N = m / 4 = 2^(g-2)):
* m = 2^g (g entero)
* a = 3 + 8k  o  a = 5 + 8k (k entero)
* X[0] debe ser un numero impar

Pasos:
1. Definir los parámetros de entrada X[0] (impar), a y m.
2. Calcular X[i+1] = (a * X[i]) mod m.
3. Calcular r[i+1] = X[i+1] / (m - 1).
4. Repetir el proceso hasta completar el periodo de vida.

Ejemplo simplificado (X[0] = 17, k = 2, g = 5 -> a = 21, m = 32):
X[1] = (21 * 17) mod 32 = 5  -> r[1] = 5 / 31  = 0.1612
X[2] = (21 * 5)  mod 32 = 9  -> r[2] = 9 / 31  = 0.2903
X[3] = (21 * 9)  mod 32 = 29 -> r[3] = 29 / 31 = 0.9354
X[4] = (21 * 29) mod 32 = 1  -> r[4] = 1 / 31  = 0.0322
X[5] = (21 * 1)  mod 32 = 21 -> r[5] = 21 / 31 = 0.6774
X[6] = (21 * 21) mod 32 = 25 -> r[6] = 25 / 31 = 0.8064
X[7] = (21 * 25) mod 32 = 13 -> r[7] = 13 / 31 = 0.4193
X[8] = (21 * 13) mod 32 = 17 -> r[8] = 17 / 31 = 0.5483
"""

def congruencial_lineal():
    pass

"""
Algoritmo 5: Congruencial aditivo.
Requiere una secuencia previa de n números enteros (X[1], X[2], ..., X[n]) para generar nuevos elementos
a partir de X[n+1]. Su ecuación recursiva es:
 X[i] = (X[i-1] + X[i-n]) mod m   para i = n+1, n+2, ...
Los números r[i] se obtienen mediante:
 r[i] = X[i] / (m - 1)

Pasos:
1. Seleccionar la secuencia inicial de n números enteros y el modulo m.
2. Sumar el ultimo valor generado con el valor ubicado n posiciones atrás.
3. Aplicar el modulo m al resultado para obtener X[i].
4. Normalizar dividiendo entre (m - 1) para obtener r[i].

Ejemplo simplificado (Secuencia inicial n=5: X[1]=65, X[2]=89, X[3]=98, X[4]=03, X[5]=69; m=100):
X[6]  = (X[5]  + X[1]) mod 100 = (69 + 65) mod 100 = 34 -> r[1] = 34 / 99 = 0.3434
X[7]  = (X[6]  + X[2]) mod 100 = (34 + 89) mod 100 = 23 -> r[2] = 23 / 99 = 0.2323
X[8]  = (X[7]  + X[3]) mod 100 = (23 + 98) mod 100 = 21 -> r[3] = 21 / 99 = 0.2121
X[9]  = (X[8]  + X[4]) mod 100 = (21 + 03) mod 100 = 24 -> r[4] = 24 / 99 = 0.2424
X[10] = (X[9]  + X[5]) mod 100 = (24 + 69) mod 100 = 93 -> r[5] = 93 / 99 = 0.9393
X[11] = (X[10] + X[6]) mod 100 = (93 + 34) mod 100 = 27 -> r[6] = 27 / 99 = 0.2727
X[12] = (X[11] + X[7]) mod 100 = (27 + 23) mod 100 = 50 -> r[7] = 50 / 99 = 0.5050
"""

def congruencial_aditivo():
    pass

"""
Algoritmo 6: Congruenciales no lineales.
Sustituyen la relación lineal por expresiones polinomiales de mayor grado para generar secuencias no
lineales de enteros mod m.
"""

"""
Algoritmo 6.1: Congruencial cuadrático.
Ecuación recursiva:
X[i+1] = (a * (X[i])^2 + b * X[i] + c) mod m
Normalización: r[i+1] = X[i+1] / (m - 1)

Condiciones para periodo de vida máximo (N = m):
* m = 2^g (g entero)
* a debe ser un numero par
* c debe ser un numero impar
* (b - 1) mod 4 = 1

Ejemplo simplificado (X[0]=13, m=8, a=26, b=27, c=27):
X[1] = (26 * 13^2 + 27 * 13 + 27) mod 8 = 4
X[2] = (26 * 4^2  + 27 * 4  + 27) mod 8 = 7
X[3] = (26 * 7^2  + 27 * 7  + 27) mod 8 = 2
X[4] = (26 * 2^2  + 27 * 2  + 27) mod 8 = 1
X[5] = (26 * 1^2  + 27 * 1  + 27) mod 8 = 0
X[6] = (26 * 0^2  + 27 * 0  + 27) mod 8 = 3
X[7] = (26 * 3^2  + 27 * 3  + 27) mod 8 = 6
X[8] = (26 * 6^2  + 27 * 6  + 27) mod 8 = 5
X[9] = (26 * 5^2  + 27 * 5  + 27) mod 8 = 4
"""

def congruencial_cuadratico():
    pass

"""
Algoritmo 6.2: Blum, Blum y Shub.

Variación del algoritmo cuadrático cuando a = 1, b = 0 y c = 0. Su ecuación recursiva es:
X[i+1] = ((X[i])^2) mod m

Produce secuencias de enteros de comportamiento impredecible.
"""

def blum_blum_shub():
    pass

if __name__ == "__main__":
    cuadrados_medios()
    productos_medios()
    multiplicador_constante()
    congruencial_lineal()
    congruencial_aditivo()
    congruencial_cuadratico()
    blum_blum_shub()


