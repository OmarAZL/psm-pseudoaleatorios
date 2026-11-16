"""
Proyecto para Simulación y Modelos, validación de números pseudoaleatorios.
Omar Zabala y Cristian González
"""
import math
from scipy import stats

# =============================================================================
# VALIDADOR 1: PRUEBA DE LA MEDIA
# =============================================================================
"""
Algoritmo 1: Prueba de la media.
Verifica si los números pseudoaleatorios generados tienen una media estadísticamente
igual a 0.5, que es el valor esperado para una distribución uniforme en (0,1).

Hipótesis:
H0: x̄ = 0.5 (los números son uniformes en (0,1))
H1: x̄ ≠ 0.5

Estadístico de prueba:
Z = (x̄ - 0.5) / sqrt(1 / (12 * n))

Donde:
- x̄ = (1/n) * Σ r[i] (media muestral de los números pseudoaleatorios)
- n = cantidad de números pseudoaleatorios
- 1/12 = varianza teórica de la distribución uniforme en (0,1)

Criterio de decisión:
Si |Z| ≤ Z_{α/2}, no se rechaza H0 (los números tienen media 0.5)
Si |Z| > Z_{α/2}, se rechaza H0

Ejemplo (r = [0.36, 0.17, 0.56, 0.97, 0.23], α = 0.05):
x̄ = (0.36 + 0.17 + 0.56 + 0.97 + 0.23) / 5 = 0.458
Z = (0.458 - 0.5) / sqrt(1 / (12 * 5)) = -0.042 / 0.1291 = -0.3253
Z_{0.025} = 1.96
|-0.3253| < 1.96 → No se rechaza H0
"""
def prueba_media(aleatorios, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 2:
        return "Se requiere una lista con al menos 2 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    n = len(aleatorios)
    x_barra = sum(aleatorios) / n
    var_teorica = 1 / 12
    desv_estandar = math.sqrt(var_teorica / n)
    z = (x_barra - 0.5) / desv_estandar
    z_critico = stats.norm.ppf(1 - alfa / 2)

    return {
        "n": n,
        "x_barra": round(x_barra, 4),
        "Z_calculado": round(z, 4),
        "Z_critico": round(z_critico, 4),
        "alfa": alfa,
        "decision": "No se rechaza H0" if abs(z) <= z_critico else "Se rechaza H0"
    }


# =============================================================================
# VALIDADOR 2: PRUEBA DE LA VARIANZA
# =============================================================================
"""
Algoritmo 2: Prueba de la varianza.
Verifica si los números pseudoaleatorios generados tienen una varianza estadísticamente
igual a 1/12, que es el valor esperado para una distribución uniforme en (0,1).

Hipótesis:
H0: S² = 1/12
H1: S² ≠ 1/12

Estadístico de prueba:
χ² = (n - 1) * S² / (1/12)

Donde:
- S² = (1/(n-1)) * Σ (r[i] - x̄)² (varianza muestral)
- n = cantidad de números pseudoaleatorios
- 1/12 = varianza teórica de la distribución uniforme en (0,1)

Criterio de decisión:
Si χ²_{1-α/2, n-1} ≤ χ² ≤ χ²_{α/2, n-1}, no se rechaza H0
En otro caso, se rechaza H0

Ejemplo (r = [0.36, 0.17, 0.56, 0.97, 0.23], α = 0.05):
x̄ = 0.458
S² = ((0.36-0.458)² + (0.17-0.458)² + (0.56-0.458)² + (0.97-0.458)² + (0.23-0.458)²) / 4
S² = 0.0923
χ² = 4 * 0.0923 / (1/12) = 4.4304
χ²_{0.975, 4} = 0.484, χ²_{0.025, 4} = 11.143
0.484 ≤ 4.4304 ≤ 11.143 → No se rechaza H0
"""
def prueba_varianza(aleatorios, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 2:
        return "Se requiere una lista con al menos 2 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    n = len(aleatorios)
    x_barra = sum(aleatorios) / n
    s_cuadrada = sum((r - x_barra) ** 2 for r in aleatorios) / (n - 1)
    var_teorica = 1 / 12
    chi_cuadrado = (n - 1) * s_cuadrada / var_teorica
    chi_inf = stats.chi2.ppf(alfa / 2, n - 1)
    chi_sup = stats.chi2.ppf(1 - alfa / 2, n - 1)

    return {
        "n": n,
        "x_barra": round(x_barra, 4),
        "S_cuadrada": round(s_cuadrada, 4),
        "chi_cuadrado_calculado": round(chi_cuadrado, 4),
        "chi_cuadrado_inferior": round(chi_inf, 4),
        "chi_cuadrado_superior": round(chi_sup, 4),
        "alfa": alfa,
        "decision": "No se rechaza H0" if chi_inf <= chi_cuadrado <= chi_sup else "Se rechaza H0"
    }


# =============================================================================
# VALIDADOR 3.1: PRUEBA DE UNIFORMIDAD - CHI-CUADRADO
# =============================================================================
"""
Algoritmo 3.1: Prueba de uniformidad Chi-Cuadrado.
Verifica si los números pseudoaleatorios siguen una distribución uniforme en (0,1)
dividiendo el intervalo en k subintervalos de igual longitud y comparando las
frecuencias observadas con las esperadas.

Hipótesis:
H0: Los números siguen una distribución uniforme en (0,1)
H1: Los números no siguen una distribución uniforme

Estadístico de prueba:
χ² = Σ_{i=1}^{k} (O[i] - E[i])² / E[i]

Donde:
- k = número de intervalos (clases)
- O[i] = frecuencia observada en el intervalo i
- E[i] = n / k (frecuencia esperada en cada intervalo, uniforme)
- n = cantidad total de números pseudoaleatorios

Criterio de decisión:
Si χ² ≤ χ²_{α, k-1}, no se rechaza H0
Si χ² > χ²_{α, k-1}, se rechaza H0

Ejemplo (n=40, k=4, α=0.05):
Intervalos: [0,0.25), [0.25,0.5), [0.5,0.75), [0.75,1]
O = [12, 8, 11, 9], E = [10, 10, 10, 10]
χ² = (12-10)²/10 + (8-10)²/10 + (11-10)²/10 + (9-10)²/10 = 1.1
χ²_{0.05, 3} = 7.815
1.1 < 7.815 → No se rechaza H0
"""
def prueba_chi_cuadrado(aleatorios, k=10, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 2:
        return "Se requiere una lista con al menos 2 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(k, int) and k >= 2):
        return "El número de intervalos (k) debe ser un entero mayor o igual a 2"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    n = len(aleatorios)
    amplitud = 1 / k
    esperada = n / k
    observadas = [0] * k

    for r in aleatorios:
        i = min(int(r / amplitud), k - 1)
        observadas[i] += 1

    chi_cuadrado = sum((o - esperada) ** 2 / esperada for o in observadas)
    chi_critico = stats.chi2.ppf(1 - alfa, k - 1)

    return {
        "n": n,
        "k": k,
        "frecuencias_observadas": observadas,
        "frecuencia_esperada": round(esperada, 4),
        "chi_cuadrado_calculado": round(chi_cuadrado, 4),
        "chi_cuadrado_critico": round(chi_critico, 4),
        "alfa": alfa,
        "grados_libertad": k - 1,
        "decision": "No se rechaza H0" if chi_cuadrado <= chi_critico else "Se rechaza H0"
    }


# =============================================================================
# VALIDADOR 3.2: PRUEBA DE UNIFORMIDAD - KOLMOGOROV-SMIRNOV
# =============================================================================
"""
Algoritmo 3.2: Prueba de uniformidad Kolmogorov-Smirnov.
Verifica si los números pseudoaleatorios siguen una distribución uniforme en (0,1)
comparando la función de distribución acumulada empírica con la teórica.

Hipótesis:
H0: Los números siguen una distribución uniforme en (0,1)
H1: Los números no siguen una distribución uniforme

Estadístico de prueba:
D = max |F_n(x) - F(x)|

Donde:
- F_n(x) = frecuencia acumulada observada (i/n para el i-ésimo valor ordenado)
- F(x) = x (distribución acumulada teórica uniforme en (0,1))
- Se calcula D+ = max(i/n - r[i]) y D- = max(r[i] - (i-1)/n)
- D = max(D+, D-)

Criterio de decisión:
Si D ≤ D_{α, n}, no se rechaza H0
Si D > D_{α, n}, se rechaza H0
D_{α, n} ≈ sqrt(-ln(α/2) / (2n)) para n grande, o tabla crítica.

Ejemplo (r = [0.12, 0.36, 0.52, 0.71, 0.89], α = 0.05):
Ordenados: [0.12, 0.36, 0.52, 0.71, 0.89]
i/n: [0.2, 0.4, 0.6, 0.8, 1.0]
(i-1)/n: [0.0, 0.2, 0.4, 0.6, 0.8]
D+ = max(0.2-0.12, 0.4-0.36, 0.6-0.52, 0.8-0.71, 1.0-0.89) = max(0.08, 0.04, 0.08, 0.09, 0.11) = 0.11
D- = max(0.12-0.0, 0.36-0.2, 0.52-0.4, 0.71-0.6, 0.89-0.8) = max(0.12, 0.16, 0.12, 0.11, 0.09) = 0.16
D = max(0.11, 0.16) = 0.16
D_{0.05, 5} ≈ 0.565
0.16 < 0.565 → No se rechaza H0
"""
def prueba_ks(aleatorios, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 2:
        return "Se requiere una lista con al menos 2 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    n = len(aleatorios)
    ordenados = sorted(aleatorios)
    d_positivas = [i / n - ordenados[i - 1] for i in range(1, n + 1)]
    d_negativas = [ordenados[i - 1] - (i - 1) / n for i in range(1, n + 1)]
    d_mas = max(d_positivas)
    d_menos = max(d_negativas)
    d = max(d_mas, d_menos)

    # Valor crítico aproximado para KS
    d_critico = stats.kstest.rvs if False else math.sqrt(-math.log(alfa / 2) / (2 * n))
    # Usando valor crítico exacto de la tabla KS
    d_critico_tabla = stats.kstwo.ppf(1 - alfa, n)

    return {
        "n": n,
        "D_positiva": round(d_mas, 4),
        "D_negativa": round(d_menos, 4),
        "D_calculado": round(d, 4),
        "D_critico": round(d_critico_tabla, 4),
        "alfa": alfa,
        "decision": "No se rechaza H0" if d <= d_critico_tabla else "Se rechaza H0"
    }


# =============================================================================
# VALIDADOR 4.1: PRUEBA DE CORRIDAS ARRIBA Y ABAJO
# =============================================================================
"""
Algoritmo 4.1: Prueba de corridas arriba y abajo.
Verifica la independencia de los números pseudoaleatorios analizando la secuencia
de valores crecientes (arriba) y decrecientes (abajo).

Hipótesis:
H0: Los números son independientes
H1: Los números no son independientes

Procedimiento:
1. Se comparan números consecutivos: si r[i+1] > r[i] se marca "+", si r[i+1] < r[i] se marca "-"
2. Se cuenta el número total de corridas "a" (grupos de signos iguales consecutivos)
3. Se calcula el estadístico Z

Estadístico de prueba:
μ_a = (2n - 1) / 3
σ²_a = (16n - 29) / 90
Z = (a - μ_a) / σ_a

Donde:
- n = cantidad de números pseudoaleatorios
- a = número de corridas observadas

Criterio de decisión:
Si |Z| ≤ Z_{α/2}, no se rechaza H0
Si |Z| > Z_{α/2}, se rechaza H0

Ejemplo (r = [0.12, 0.36, 0.52, 0.41, 0.23, 0.67, 0.89, 0.71], α = 0.05):
Signos: + + - - + + -
Corridas: a = 4
μ_a = (2*8 - 1) / 3 = 5
σ²_a = (16*8 - 29) / 90 = 1.1
σ_a = 1.049
Z = (4 - 5) / 1.049 = -0.953
Z_{0.025} = 1.96
|-0.953| < 1.96 → No se rechaza H0
"""
def prueba_corridas_arriba_abajo(aleatorios, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 3:
        return "Se requiere una lista con al menos 3 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    n = len(aleatorios)
    signos = []
    for i in range(n - 1):
        if aleatorios[i + 1] > aleatorios[i]:
            signos.append("+")
        elif aleatorios[i + 1] < aleatorios[i]:
            signos.append("-")
        else:
            signos.append("=")

    # Contar corridas
    a = 1
    for i in range(1, len(signos)):
        if signos[i] != signos[i - 1]:
            a += 1

    mu_a = (2 * n - 1) / 3
    var_a = (16 * n - 29) / 90
    sigma_a = math.sqrt(var_a)
    z = (a - mu_a) / sigma_a
    z_critico = stats.norm.ppf(1 - alfa / 2)

    return {
        "n": n,
        "signos": signos,
        "corridas_observadas": a,
        "mu_a": round(mu_a, 4),
        "sigma_a": round(sigma_a, 4),
        "Z_calculado": round(z, 4),
        "Z_critico": round(z_critico, 4),
        "alfa": alfa,
        "decision": "No se rechaza H0" if abs(z) <= z_critico else "Se rechaza H0"
    }


# =============================================================================
# VALIDADOR 4.2: PRUEBA DE CORRIDAS ARRIBA Y ABAJO DE LA MEDIA
# =============================================================================
"""
Algoritmo 4.2: Prueba de corridas arriba y abajo de la media.
Verifica la independencia comparando cada número con la media muestral (o 0.5)
y analizando las corridas de valores consecutivos por encima o por debajo.

Hipótesis:
H0: Los números son independientes
H1: Los números no son independientes

Procedimiento:
1. Se calcula la media x̄ de los números (o se usa 0.5)
2. Se marca "+" si r[i] ≥ x̄, "-" si r[i] < x̄
3. Se cuenta el número de corridas "b"
4. Se cuentan n1 (números ≥ x̄) y n2 (números < x̄)

Estadístico de prueba:
μ_b = (2 * n1 * n2) / n + 0.5
σ²_b = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n² * (n - 1))
Z = (b - μ_b) / σ_b

Criterio de decisión:
Si |Z| ≤ Z_{α/2}, no se rechaza H0
Si |Z| > Z_{α/2}, se rechaza H0

Ejemplo (r = [0.12, 0.36, 0.52, 0.41, 0.23, 0.67, 0.89, 0.71], x̄ = 0.48875, α = 0.05):
Signos: - - + - - + + +
n1 = 4 (≥ x̄), n2 = 4 (< x̄)
Corridas: b = 4
μ_b = (2 * 4 * 4) / 8 + 0.5 = 4.5
σ²_b = (2 * 4 * 4 * (2 * 4 * 4 - 8)) / (64 * 7) = 1.714
σ_b = 1.309
Z = (4 - 4.5) / 1.309 = -0.382
Z_{0.025} = 1.96
|-0.382| < 1.96 → No se rechaza H0
"""
def prueba_corridas_media(aleatorios, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 3:
        return "Se requiere una lista con al menos 3 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    n = len(aleatorios)
    x_barra = sum(aleatorios) / n
    signos = []
    n1 = 0
    n2 = 0
    for r in aleatorios:
        if r >= x_barra:
            signos.append("+")
            n1 += 1
        else:
            signos.append("-")
            n2 += 1

    # Contar corridas
    b = 1
    for i in range(1, len(signos)):
        if signos[i] != signos[i - 1]:
            b += 1

    mu_b = (2 * n1 * n2) / n + 0.5
    var_b = (2 * n1 * n2 * (2 * n1 * n2 - n)) / (n ** 2 * (n - 1))
    sigma_b = math.sqrt(var_b) if var_b > 0 else 0
    z = (b - mu_b) / sigma_b if sigma_b > 0 else 0
    z_critico = stats.norm.ppf(1 - alfa / 2)

    return {
        "n": n,
        "x_barra": round(x_barra, 4),
        "n1": n1,
        "n2": n2,
        "signos": signos,
        "corridas_observadas": b,
        "mu_b": round(mu_b, 4),
        "sigma_b": round(sigma_b, 4),
        "Z_calculado": round(z, 4),
        "Z_critico": round(z_critico, 4),
        "alfa": alfa,
        "decision": "No se rechaza H0" if abs(z) <= z_critico else "Se rechaza H0"
    }


# =============================================================================
# VALIDADOR 4.3: PRUEBA POKER
# =============================================================================
"""
Algoritmo 4.3: Prueba Poker.
Verifica la independencia analizando los dígitos de los números pseudoaleatorios
agrupados en combinaciones de k dígitos y clasificándolos según patrones.

Hipótesis:
H0: Los números son independientes
H1: Los números no son independientes

Procedimiento:
1. Se extraen los primeros k dígitos decimales de cada número
2. Se clasifica cada combinación en categorías según el patrón de dígitos:
   - Todos diferentes (D)
   - Un par (1P)
   - Dos pares (2P)
   - Tres iguales (3I)
   - Tres iguales y un par (3I1P)
   - Cuatro iguales (4I)
3. Se comparan las frecuencias observadas con las esperadas (probabilidades teóricas)

Estadístico de prueba:
χ² = Σ (O[i] - E[i])² / E[i]

Probabilidades teóricas (para k=4 dígitos, 10 valores posibles):
P(D) = 10*9*8*7 / 10^4 = 0.504
P(1P) = C(4,2) * 10 * 9 * 8 / 10^4 = 0.432
P(2P) = C(4,2) * C(2,2) * 10 * 9 / (2 * 10^4) = 0.027
P(3I) = C(4,3) * 10 * 9 / 10^4 = 0.036
P(4I) = 10 / 10^4 = 0.001

Criterio de decisión:
Si χ² ≤ χ²_{α, c-1}, no se rechaza H0 (c = número de categorías)
Si χ² > χ²_{α, c-1}, se rechaza H0

Ejemplo (n=100, k=4, α=0.05):
O = [48, 45, 3, 3, 1], E = [50.4, 43.2, 2.7, 3.6, 0.1]
χ² = (48-50.4)²/50.4 + (45-43.2)²/43.2 + ... = 0.52
χ²_{0.05, 4} = 9.488
0.52 < 9.488 → No se rechaza H0
"""
def prueba_poker(aleatorios, k=4, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 2:
        return "Se requiere una lista con al menos 2 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(k, int) and 2 <= k <= 5):
        return "k debe ser un entero entre 2 y 5"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    n = len(aleatorios)
    
    # Función para clasificar un número según sus dígitos
    def clasificar_poker(r):
        str_r = f"{r:.{k}f}".split('.')[1][:k]
        conteo = {}
        for digito in str_r:
            conteo[digito] = conteo.get(digito, 0) + 1
        frecuencias = sorted(conteo.values(), reverse=True)
        return tuple(frecuencias)

    # Clasificar todos los números
    categorias = {}
    for r in aleatorios:
        cat = clasificar_poker(r)
        categorias[cat] = categorias.get(cat, 0) + 1

    # Calcular probabilidades teóricas
    def probabilidad_patron(patron, k):
        from math import comb, factorial
        n_grupos = len(patron)
        num_formas = comb(k, *patron) if len(patron) > 1 else 1
        if len(patron) == 1:
            return 10 / (10 ** k)
        elif len(patron) == 2 and patron[0] == 2 and patron[1] == 2:
            return (10 * 9 * comb(k, 2)) / (2 * (10 ** k))
        elif len(patron) == 2:
            return (10 * 9 * comb(k, patron[0])) / (10 ** k)
        else:
            return (10 * 9 * 8 * comb(k, patron[0]) * comb(k - patron[0], patron[1])) / (10 ** k)

    # Para simplificar, usamos categorías estándar
    categorias_estandar = {
        "todos_diferentes": 0,
        "un_par": 0,
        "dos_pares": 0,
        "tres_iguales": 0,
        "full": 0,
        "cuatro_iguales": 0,
        "cinco_iguales": 0
    }

    for patron, conteo in categorias.items():
        if len(patron) == k:
            categorias_estandar["todos_diferentes"] += conteo
        elif len(patron) == 1 and patron[0] == k:
            if k == 5:
                categorias_estandar["cinco_iguales"] += conteo
            elif k == 4:
                categorias_estandar["cuatro_iguales"] += conteo
            elif k == 3:
                categorias_estandar["tres_iguales"] += conteo
            elif k == 2:
                categorias_estandar["un_par"] += conteo
        elif len(patron) == 2:
            if patron[0] == 3 and patron[1] == 2:
                categorias_estandar["full"] += conteo
            elif patron[0] == 3:
                categorias_estandar["tres_iguales"] += conteo
            elif patron[0] == 2 and patron[1] == 2:
                categorias_estandar["dos_pares"] += conteo
            else:
                categorias_estandar["un_par"] += conteo

    # Probabilidades teóricas para k=4
    if k == 4:
        probabilidades = {
            "todos_diferentes": 0.504,
            "un_par": 0.432,
            "dos_pares": 0.027,
            "tres_iguales": 0.036,
            "cuatro_iguales": 0.001
        }
        categorias_usar = ["todos_diferentes", "un_par", "dos_pares", "tres_iguales", "cuatro_iguales"]
    elif k == 3:
        probabilidades = {
            "todos_diferentes": 0.72,
            "un_par": 0.27,
            "tres_iguales": 0.01
        }
        categorias_usar = ["todos_diferentes", "un_par", "tres_iguales"]
    else:  # k=2
        probabilidades = {
            "todos_diferentes": 0.9,
            "un_par": 0.1
        }
        categorias_usar = ["todos_diferentes", "un_par"]

    observadas = [categorias_estandar[cat] for cat in categorias_usar]
    esperadas = [n * probabilidades[cat] for cat in categorias_usar]

    chi_cuadrado = sum((o - e) ** 2 / e for o, e in zip(observadas, esperadas) if e > 0)
    grados_libertad = len(categorias_usar) - 1
    chi_critico = stats.chi2.ppf(1 - alfa, grados_libertad)

    return {
        "n": n,
        "k": k,
        "frecuencias_observadas": {cat: categorias_estandar[cat] for cat in categorias_usar},
        "frecuencias_esperadas": {cat: round(n * probabilidades[cat], 4) for cat in categorias_usar},
        "chi_cuadrado_calculado": round(chi_cuadrado, 4),
        "chi_cuadrado_critico": round(chi_critico, 4),
        "alfa": alfa,
        "grados_libertad": grados_libertad,
        "decision": "No se rechaza H0" if chi_cuadrado <= chi_critico else "Se rechaza H0"
    }


# =============================================================================
# VALIDADOR 4.4: PRUEBA DE SERIES
# =============================================================================
"""
Algoritmo 4.4: Prueba de series.
Verifica la independencia analizando pares consecutivos de números y su distribución
en una matriz de k×k celdas.

Hipótesis:
H0: Los números son independientes
H1: Los números no son independientes

Procedimiento:
1. Se forman pares consecutivos: (r[0], r[1]), (r[2], r[3]), ...
2. Se divide el intervalo (0,1) en k subintervalos
3. Se cuenta cuántos pares caen en cada celda (i,j) de la matriz k×k
4. Se comparan las frecuencias observadas con las esperadas

Estadístico de prueba:
χ² = Σ_{i=1}^{k} Σ_{j=1}^{k} (O[i,j] - E[i,j])² / E[i,j]

Donde:
- O[i,j] = frecuencia observada en la celda (i,j)
- E[i,j] = n_pares / k² (frecuencia esperada bajo independencia)
- n_pares = n/2 (número de pares formados)

Criterio de decisión:
Si χ² ≤ χ²_{α, k²-1}, no se rechaza H0
Si χ² > χ²_{α, k²-1}, se rechaza H0

Ejemplo (n=20, k=2, α=0.05):
Pares: (r1,r2), (r3,r4), ..., (r19,r20)
Matriz 2×2:
       [0,0.5)  [0.5,1]
[0,0.5)   5        3
[0.5,1]   4        3
E = 10/4 = 2.5 en cada celda
χ² = (5-2.5)²/2.5 + (3-2.5)²/2.5 + (4-2.5)²/2.5 + (3-2.5)²/2.5 = 4.0
χ²_{0.05, 3} = 7.815
4.0 < 7.815 → No se rechaza H0
"""
def prueba_series(aleatorios, k=2, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 4:
        return "Se requiere una lista con al menos 4 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(k, int) and k >= 2):
        return "El número de intervalos (k) debe ser un entero mayor o igual a 2"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    n = len(aleatorios)
    n_pares = n // 2
    amplitud = 1 / k
    matriz = [[0] * k for _ in range(k)]

    for i in range(0, n_pares * 2, 2):
        r1 = aleatorios[i]
        r2 = aleatorios[i + 1]
        fila = min(int(r1 / amplitud), k - 1)
        columna = min(int(r2 / amplitud), k - 1)
        matriz[fila][columna] += 1

    esperada = n_pares / (k ** 2)
    chi_cuadrado = sum((matriz[i][j] - esperada) ** 2 / esperada 
                       for i in range(k) for j in range(k))
    grados_libertad = k ** 2 - 1
    chi_critico = stats.chi2.ppf(1 - alfa, grados_libertad)

    return {
        "n": n,
        "n_pares": n_pares,
        "k": k,
        "matriz_observada": matriz,
        "frecuencia_esperada": round(esperada, 4),
        "chi_cuadrado_calculado": round(chi_cuadrado, 4),
        "chi_cuadrado_critico": round(chi_critico, 4),
        "alfa": alfa,
        "grados_libertad": grados_libertad,
        "decision": "No se rechaza H0" if chi_cuadrado <= chi_critico else "Se rechaza H0"
    }


# =============================================================================
# VALIDADOR 4.5: PRUEBA DE HUECOS
# =============================================================================
"""
Algoritmo 4.5: Prueba de huecos.
Verifica la independencia analizando los espacios (huecos) entre apariciones
consecutivas de números dentro de un rango específico.

Hipótesis:
H0: Los números son independientes
H1: Los números no son independientes

Procedimiento:
1. Se define un rango [a, b] ⊂ (0,1)
2. Se recorren los números contando los huecos (números fuera del rango)
   entre apariciones consecutivas de números dentro del rango
3. Se clasifican los huecos por longitud: 0, 1, 2, ..., k-1, ≥k
4. Se comparan las frecuencias observadas con las esperadas

Estadístico de prueba:
χ² = Σ (O[i] - E[i])² / E[i]

Donde:
- O[i] = frecuencia observada de huecos de longitud i
- E[i] = n_apariciones * P(hueco de longitud i)
- P(hueco de longitud i) = p * (1-p)^i para i < k
- P(hueco de longitud ≥ k) = (1-p)^k
- p = b - a (probabilidad de caer en el rango)

Criterio de decisión:
Si χ² ≤ χ²_{α, k-1}, no se rechaza H0
Si χ² > χ²_{α, k-1}, se rechaza H0

Ejemplo (r = [0.12, 0.36, 0.52, 0.41, 0.23, 0.67, 0.89, 0.71], rango=[0.3, 0.7], α=0.05):
Números en rango: 0.36, 0.52, 0.41, 0.67
Huecos: 0 (entre 0.36 y 0.52), 0 (entre 0.52 y 0.41), 1 (entre 0.41 y 0.67)
p = 0.7 - 0.3 = 0.4
n_apariciones = 4
E[0] = 4 * 0.4 = 1.6
E[1] = 4 * 0.4 * 0.6 = 0.96
E[≥2] = 4 * 0.6² = 1.44
O = [2, 1, 1]
χ² = (2-1.6)²/1.6 + (1-0.96)²/0.96 + (1-1.44)²/1.44 = 0.31
χ²_{0.05, 2} = 5.991
0.31 < 5.991 → No se rechaza H0
"""
def prueba_huecos(aleatorios, a=0.3, b=0.7, k=5, alfa=0.05):
    if not isinstance(aleatorios, list) or len(aleatorios) < 2:
        return "Se requiere una lista con al menos 2 números pseudoaleatorios"
    if not all(isinstance(r, (int, float)) and 0 <= r <= 1 for r in aleatorios):
        return "Todos los números deben estar en el intervalo [0, 1]"
    if not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and 0 <= a < b <= 1):
        return "El rango [a, b] debe cumplir 0 ≤ a < b ≤ 1"
    if not (isinstance(k, int) and k >= 2):
        return "k debe ser un entero mayor o igual a 2"
    if not (isinstance(alfa, (int, float)) and 0 < alfa < 1):
        return "El nivel de significancia (alfa) debe estar entre 0 y 1"

    p = b - a
    q = 1 - p
    
    # Contar huecos
    huecos = []
    contador_hueco = 0
    n_apariciones = 0
    
    for r in aleatorios:
        if a <= r <= b:
            huecos.append(contador_hueco)
            n_apariciones += 1
            contador_hueco = 0
        else:
            contador_hueco += 1

    if n_apariciones == 0:
        return "No hay números en el rango especificado"

    # Clasificar huecos
    observadas = [0] * k
    for hueco in huecos:
        if hueco < k - 1:
            observadas[hueco] += 1
        else:
            observadas[k - 1] += 1

    # Calcular esperadas
    esperadas = []
    for i in range(k):
        if i < k - 1:
            esperadas.append(n_apariciones * p * (q ** i))
        else:
            esperadas.append(n_apariciones * (q ** i))

    chi_cuadrado = sum((o - e) ** 2 / e for o, e in zip(observadas, esperadas) if e > 0)
    grados_libertad = k - 1
    chi_critico = stats.chi2.ppf(1 - alfa, grados_libertad)

    return {
        "n": len(aleatorios),
        "rango": f"[{a}, {b}]",
        "p": round(p, 4),
        "n_apariciones": n_apariciones,
        "k": k,
        "frecuencias_observadas": observadas,
        "frecuencias_esperadas": [round(e, 4) for e in esperadas],
        "chi_cuadrado_calculado": round(chi_cuadrado, 4),
        "chi_cuadrado_critico": round(chi_critico, 4),
        "alfa": alfa,
        "grados_libertad": grados_libertad,
        "decision": "No se rechaza H0" if chi_cuadrado <= chi_critico else "Se rechaza H0"
    }


# =============================================================================
# BLOQUE DE PRUEBAS
# =============================================================================
if __name__ == "__main__":
    # Números pseudoaleatorios de ejemplo
    aleatorios_ejemplo = [
        0.3636, 0.1717, 0.5656, 0.9797, 0.2323, 0.2121, 0.2424, 0.9393,
        0.2727, 0.5050, 0.4545, 0.8181, 0.1515, 0.6363, 0.7272, 0.3434,
        0.5858, 0.4242, 0.7676, 0.8989
    ]

    print("=" * 80)
    print("VALIDADOR 1: PRUEBA DE LA MEDIA")
    print("=" * 80)
    resultado = prueba_media(aleatorios_ejemplo, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()

    print("=" * 80)
    print("VALIDADOR 2: PRUEBA DE LA VARIANZA")
    print("=" * 80)
    resultado = prueba_varianza(aleatorios_ejemplo, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()

    print("=" * 80)
    print("VALIDADOR 3.1: PRUEBA CHI-CUADRADO (UNIFORMIDAD)")
    print("=" * 80)
    resultado = prueba_chi_cuadrado(aleatorios_ejemplo, k=5, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()

    print("=" * 80)
    print("VALIDADOR 3.2: PRUEBA KOLMOGOROV-SMIRNOV (UNIFORMIDAD)")
    print("=" * 80)
    resultado = prueba_ks(aleatorios_ejemplo, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()

    print("=" * 80)
    print("VALIDADOR 4.1: PRUEBA DE CORRIDAS ARRIBA Y ABAJO")
    print("=" * 80)
    resultado = prueba_corridas_arriba_abajo(aleatorios_ejemplo, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()

    print("=" * 80)
    print("VALIDADOR 4.2: PRUEBA DE CORRIDAS ARRIBA Y ABAJO DE LA MEDIA")
    print("=" * 80)
    resultado = prueba_corridas_media(aleatorios_ejemplo, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()

    print("=" * 80)
    print("VALIDADOR 4.3: PRUEBA POKER")
    print("=" * 80)
    resultado = prueba_poker(aleatorios_ejemplo, k=4, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()

    print("=" * 80)
    print("VALIDADOR 4.4: PRUEBA DE SERIES")
    print("=" * 80)
    resultado = prueba_series(aleatorios_ejemplo, k=2, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()

    print("=" * 80)
    print("VALIDADOR 4.5: PRUEBA DE HUECOS")
    print("=" * 80)
    resultado = prueba_huecos(aleatorios_ejemplo, a=0.3, b=0.7, k=5, alfa=0.05)
    for clave, valor in resultado.items():
        print(f"{clave}: {valor}")
    print()