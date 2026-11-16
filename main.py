"""
Interfaz gráfica para generadores y validadores de números pseudoaleatorios.
Omar Zabala y Cristian González
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

# Importar módulos de generadores y validadores
from generadores import (
    cuadrados_medios, productos_medios, multiplicador_constante,
    congruencial_lineal, congruencial_multiplicativo, congruencial_aditivo,
    congruencial_cuadratico, blum_blum_shub
)
from validadores import (
    prueba_media, prueba_varianza, prueba_chi_cuadrado, prueba_ks,
    prueba_corridas_arriba_abajo, prueba_corridas_media, prueba_poker,
    prueba_series, prueba_huecos
)


class AplicacionPseudoaleatorios:
    def __init__(self, root):
        self.root = root
        self.root.title("Generadores y Validadores de Números Pseudoaleatorios")
        self.root.geometry("1400x900")
        self.root.minsize(900, 600)

        # Variables
        self.numeros_generados = []
        self.resultados_validacion = {}
        self.validadores_visibles = False

        # Crear interfaz
        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal con grid responsive
        self.root.columnconfigure(0, weight=0)  # Panel izquierdo tamaño fijo
        self.root.columnconfigure(1, weight=1)  # Panel derecho expandible
        self.root.rowconfigure(0, weight=1)

        # === PANEL IZQUIERDO ===
        panel_izquierdo = ttk.Frame(self.root, padding=10)
        panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        panel_izquierdo.columnconfigure(0, weight=1)

        # Sección de generadores
        frame_generadores = ttk.LabelFrame(panel_izquierdo, text="Generador de Números", padding=10)
        frame_generadores.grid(row=0, column=0, sticky="ew", pady=5)
        frame_generadores.columnconfigure(0, weight=1)

        ttk.Label(frame_generadores, text="Seleccionar generador:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.combo_generador = ttk.Combobox(frame_generadores, state="readonly", width=25)
        self.combo_generador['values'] = (
            "Cuadrados Medios",
            "Productos Medios",
            "Multiplicador Constante",
            "Congruencial Lineal",
            "Congruencial Multiplicativo",
            "Congruencial Aditivo",
            "Congruencial Cuadrático",
            "Blum, Blum y Shub"
        )
        self.combo_generador.current(0)
        self.combo_generador.grid(row=1, column=0, sticky="ew", pady=5)
        self.combo_generador.bind('<<ComboboxSelected>>', self.actualizar_parametros)

        # Frame para parámetros dinámicos
        self.frame_parametros = ttk.Frame(frame_generadores)
        self.frame_parametros.grid(row=2, column=0, sticky="ew", pady=5)
        self.frame_parametros.columnconfigure(0, weight=1)

        # Cantidad de números
        ttk.Label(frame_generadores, text="Cantidad de números (n):").grid(row=3, column=0, sticky="w", pady=(5, 0))
        self.entry_n = ttk.Entry(frame_generadores, width=25)
        self.entry_n.insert(0, "100")
        self.entry_n.grid(row=4, column=0, sticky="ew", pady=5)

        # Botón generar
        btn_generar = ttk.Button(frame_generadores, text="Generar Números", command=self.generar_numeros)
        btn_generar.grid(row=5, column=0, sticky="ew", pady=10)

        # Sección de validadores (colapsable)
        frame_validadores_container = ttk.Frame(panel_izquierdo)
        frame_validadores_container.grid(row=1, column=0, sticky="ew", pady=5)
        frame_validadores_container.columnconfigure(0, weight=1)

        # Botón para mostrar/ocultar validadores
        self.btn_toggle_validadores = ttk.Button(
            frame_validadores_container,
            text="▶ Modificar Validadores",
            command=self.toggle_validadores
        )
        self.btn_toggle_validadores.grid(row=0, column=0, sticky="ew")

        # Frame de validadores (inicialmente oculto)
        self.frame_validadores = ttk.LabelFrame(panel_izquierdo, text="Validadores", padding=10)
        self.frame_validadores.grid(row=2, column=0, sticky="ew", pady=5)
        self.frame_validadores.columnconfigure(0, weight=1)
        self.frame_validadores.grid_remove()  # Oculto inicialmente

        # Checkboxes para validadores
        self.var_media = tk.BooleanVar(value=True)
        self.var_varianza = tk.BooleanVar(value=True)
        self.var_chi_cuadrado = tk.BooleanVar(value=True)
        self.var_ks = tk.BooleanVar(value=True)
        self.var_corridas_aa = tk.BooleanVar(value=True)
        self.var_corridas_media = tk.BooleanVar(value=True)
        self.var_poker = tk.BooleanVar(value=True)
        self.var_series = tk.BooleanVar(value=True)
        self.var_huecos = tk.BooleanVar(value=True)

        validadores_info = [
            ("Prueba de Media", self.var_media),
            ("Prueba de Varianza", self.var_varianza),
            ("Prueba Chi-Cuadrado", self.var_chi_cuadrado),
            ("Prueba Kolmogorov-Smirnov", self.var_ks),
            ("Prueba Corridas Arriba/Abajo", self.var_corridas_aa),
            ("Prueba Corridas Media", self.var_corridas_media),
            ("Prueba Poker", self.var_poker),
            ("Prueba Series", self.var_series),
            ("Prueba Huecos", self.var_huecos),
        ]

        for i, (texto, var) in enumerate(validadores_info):
            ttk.Checkbutton(self.frame_validadores, text=texto, variable=var).grid(
                row=i, column=0, sticky="w", pady=2
            )

        # Nivel de significancia
        row_alfa = len(validadores_info)
        ttk.Label(self.frame_validadores, text="Nivel de significancia (α):").grid(
            row=row_alfa, column=0, sticky="w", pady=(10, 0)
        )
        self.entry_alfa = ttk.Entry(self.frame_validadores, width=25)
        self.entry_alfa.insert(0, "0.05")
        self.entry_alfa.grid(row=row_alfa + 1, column=0, sticky="ew", pady=5)

        # === PANEL DERECHO ===
        panel_derecho = ttk.Frame(self.root, padding=10)
        panel_derecho.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        panel_derecho.columnconfigure(0, weight=1)
        panel_derecho.rowconfigure(0, weight=1)

        # Notebook para tabs
        self.notebook = ttk.Notebook(panel_derecho)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

        # Tab 1: Números generados
        self.tab_numeros = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_numeros, text="Números Generados")
        self.tab_numeros.columnconfigure(0, weight=1)
        self.tab_numeros.rowconfigure(0, weight=1)

        self.text_numeros = scrolledtext.ScrolledText(self.tab_numeros, wrap=tk.WORD)
        self.text_numeros.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Tab 2: Resultados de validación
        self.tab_resultados = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_resultados, text="Resultados de Validación")
        self.tab_resultados.columnconfigure(0, weight=1)
        self.tab_resultados.rowconfigure(0, weight=1)

        self.text_resultados = scrolledtext.ScrolledText(self.tab_resultados, wrap=tk.WORD)
        self.text_resultados.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Tab 3: Gráficas
        self.tab_graficas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_graficas, text="Gráficas")
        self.tab_graficas.columnconfigure(0, weight=1)
        self.tab_graficas.rowconfigure(0, weight=1)

        # Frame para gráficas
        self.frame_graficas = ttk.Frame(self.tab_graficas)
        self.frame_graficas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_graficas.columnconfigure(0, weight=1)
        self.frame_graficas.rowconfigure(0, weight=1)

        # Inicializar parámetros
        self.actualizar_parametros(None)

    def toggle_validadores(self):
        """Mostrar u ocultar la sección de validadores"""
        if self.validadores_visibles:
            self.frame_validadores.grid_remove()
            self.btn_toggle_validadores.config(text="▶ Modificar Validadores")
            self.validadores_visibles = False
        else:
            self.frame_validadores.grid(row=2, column=0, sticky="ew", pady=5)
            self.btn_toggle_validadores.config(text="▼ Modificar Validadores")
            self.validadores_visibles = True

    def actualizar_parametros(self, event):
        # Limpiar frame de parámetros
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()

        generador = self.combo_generador.get()

        # Crear campos según el generador seleccionado
        if generador == "Cuadrados Medios":
            ttk.Label(self.frame_parametros, text="Semilla:").grid(row=0, column=0, sticky="w")
            self.entry_semilla = ttk.Entry(self.frame_parametros, width=25)
            self.entry_semilla.insert(0, "5735")
            self.entry_semilla.grid(row=1, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Dígitos (D):").grid(row=2, column=0, sticky="w")
            self.entry_d = ttk.Entry(self.frame_parametros, width=25)
            self.entry_d.insert(0, "4")
            self.entry_d.grid(row=3, column=0, sticky="ew", pady=2)

        elif generador == "Productos Medios":
            ttk.Label(self.frame_parametros, text="Semilla 1:").grid(row=0, column=0, sticky="w")
            self.entry_semilla1 = ttk.Entry(self.frame_parametros, width=25)
            self.entry_semilla1.insert(0, "5015")
            self.entry_semilla1.grid(row=1, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Semilla 2:").grid(row=2, column=0, sticky="w")
            self.entry_semilla2 = ttk.Entry(self.frame_parametros, width=25)
            self.entry_semilla2.insert(0, "5734")
            self.entry_semilla2.grid(row=3, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Dígitos (D):").grid(row=4, column=0, sticky="w")
            self.entry_d = ttk.Entry(self.frame_parametros, width=25)
            self.entry_d.insert(0, "4")
            self.entry_d.grid(row=5, column=0, sticky="ew", pady=2)

        elif generador == "Multiplicador Constante":
            ttk.Label(self.frame_parametros, text="Semilla:").grid(row=0, column=0, sticky="w")
            self.entry_semilla = ttk.Entry(self.frame_parametros, width=25)
            self.entry_semilla.insert(0, "9803")
            self.entry_semilla.grid(row=1, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Constante (a):").grid(row=2, column=0, sticky="w")
            self.entry_a = ttk.Entry(self.frame_parametros, width=25)
            self.entry_a.insert(0, "6965")
            self.entry_a.grid(row=3, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Dígitos (D):").grid(row=4, column=0, sticky="w")
            self.entry_d = ttk.Entry(self.frame_parametros, width=25)
            self.entry_d.insert(0, "4")
            self.entry_d.grid(row=5, column=0, sticky="ew", pady=2)

        elif generador == "Congruencial Lineal":
            ttk.Label(self.frame_parametros, text="Semilla (X0):").grid(row=0, column=0, sticky="w")
            self.entry_semilla = ttk.Entry(self.frame_parametros, width=25)
            self.entry_semilla.insert(0, "37")
            self.entry_semilla.grid(row=1, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Constante (a):").grid(row=2, column=0, sticky="w")
            self.entry_a = ttk.Entry(self.frame_parametros, width=25)
            self.entry_a.insert(0, "19")
            self.entry_a.grid(row=3, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Constante (c):").grid(row=4, column=0, sticky="w")
            self.entry_c = ttk.Entry(self.frame_parametros, width=25)
            self.entry_c.insert(0, "33")
            self.entry_c.grid(row=5, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Módulo (m):").grid(row=6, column=0, sticky="w")
            self.entry_m = ttk.Entry(self.frame_parametros, width=25)
            self.entry_m.insert(0, "100")
            self.entry_m.grid(row=7, column=0, sticky="ew", pady=2)

        elif generador == "Congruencial Multiplicativo":
            ttk.Label(self.frame_parametros, text="Semilla (X0, impar):").grid(row=0, column=0, sticky="w")
            self.entry_semilla = ttk.Entry(self.frame_parametros, width=25)
            self.entry_semilla.insert(0, "17")
            self.entry_semilla.grid(row=1, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Constante (a):").grid(row=2, column=0, sticky="w")
            self.entry_a = ttk.Entry(self.frame_parametros, width=25)
            self.entry_a.insert(0, "21")
            self.entry_a.grid(row=3, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Módulo (m):").grid(row=4, column=0, sticky="w")
            self.entry_m = ttk.Entry(self.frame_parametros, width=25)
            self.entry_m.insert(0, "32")
            self.entry_m.grid(row=5, column=0, sticky="ew", pady=2)

        elif generador == "Congruencial Aditivo":
            ttk.Label(self.frame_parametros, text="Secuencia inicial (separada por comas):").grid(row=0, column=0, sticky="w")
            self.entry_secuencia = ttk.Entry(self.frame_parametros, width=25)
            self.entry_secuencia.insert(0, "65,89,98,3,69")
            self.entry_secuencia.grid(row=1, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Módulo (m):").grid(row=2, column=0, sticky="w")
            self.entry_m = ttk.Entry(self.frame_parametros, width=25)
            self.entry_m.insert(0, "100")
            self.entry_m.grid(row=3, column=0, sticky="ew", pady=2)

        elif generador == "Congruencial Cuadrático":
            ttk.Label(self.frame_parametros, text="Semilla (X0):").grid(row=0, column=0, sticky="w")
            self.entry_semilla = ttk.Entry(self.frame_parametros, width=25)
            self.entry_semilla.insert(0, "13")
            self.entry_semilla.grid(row=1, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Constante (a):").grid(row=2, column=0, sticky="w")
            self.entry_a = ttk.Entry(self.frame_parametros, width=25)
            self.entry_a.insert(0, "26")
            self.entry_a.grid(row=3, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Constante (b):").grid(row=4, column=0, sticky="w")
            self.entry_b = ttk.Entry(self.frame_parametros, width=25)
            self.entry_b.insert(0, "27")
            self.entry_b.grid(row=5, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Constante (c):").grid(row=6, column=0, sticky="w")
            self.entry_c = ttk.Entry(self.frame_parametros, width=25)
            self.entry_c.insert(0, "27")
            self.entry_c.grid(row=7, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Módulo (m):").grid(row=8, column=0, sticky="w")
            self.entry_m = ttk.Entry(self.frame_parametros, width=25)
            self.entry_m.insert(0, "8")
            self.entry_m.grid(row=9, column=0, sticky="ew", pady=2)

        elif generador == "Blum, Blum y Shub":
            ttk.Label(self.frame_parametros, text="Semilla (X0):").grid(row=0, column=0, sticky="w")
            self.entry_semilla = ttk.Entry(self.frame_parametros, width=25)
            self.entry_semilla.insert(0, "7")
            self.entry_semilla.grid(row=1, column=0, sticky="ew", pady=2)

            ttk.Label(self.frame_parametros, text="Módulo (m):").grid(row=2, column=0, sticky="w")
            self.entry_m = ttk.Entry(self.frame_parametros, width=25)
            self.entry_m.insert(0, "100")
            self.entry_m.grid(row=3, column=0, sticky="ew", pady=2)

    def generar_numeros(self):
        try:
            n = int(self.entry_n.get())
            generador = self.combo_generador.get()

            # Ejecutar el generador seleccionado
            if generador == "Cuadrados Medios":
                semilla = self.entry_semilla.get()
                d = int(self.entry_d.get())
                resultado = cuadrados_medios(semilla, d, n)

            elif generador == "Productos Medios":
                semilla1 = self.entry_semilla1.get()
                semilla2 = self.entry_semilla2.get()
                d = int(self.entry_d.get())
                resultado = productos_medios(semilla1, semilla2, d, n)

            elif generador == "Multiplicador Constante":
                semilla = self.entry_semilla.get()
                a = int(self.entry_a.get())
                d = int(self.entry_d.get())
                resultado = multiplicador_constante(semilla, a, d, n)

            elif generador == "Congruencial Lineal":
                semilla = int(self.entry_semilla.get())
                a = int(self.entry_a.get())
                c = int(self.entry_c.get())
                m = int(self.entry_m.get())
                resultado = congruencial_lineal(semilla, a, c, m, n)

            elif generador == "Congruencial Multiplicativo":
                semilla = int(self.entry_semilla.get())
                a = int(self.entry_a.get())
                m = int(self.entry_m.get())
                resultado = congruencial_multiplicativo(semilla, a, m, n)

            elif generador == "Congruencial Aditivo":
                secuencia = [int(x.strip()) for x in self.entry_secuencia.get().split(',')]
                m = int(self.entry_m.get())
                resultado = congruencial_aditivo(secuencia, m, n)

            elif generador == "Congruencial Cuadrático":
                semilla = int(self.entry_semilla.get())
                a = int(self.entry_a.get())
                b = int(self.entry_b.get())
                c = int(self.entry_c.get())
                m = int(self.entry_m.get())
                resultado = congruencial_cuadratico(semilla, a, b, c, m, n)

            elif generador == "Blum, Blum y Shub":
                semilla = int(self.entry_semilla.get())
                m = int(self.entry_m.get())
                resultado = blum_blum_shub(semilla, m, n)

            # Verificar si hay error
            if isinstance(resultado, str):
                messagebox.showerror("Error", resultado)
                return

            # Convertir a flotantes si son strings
            self.numeros_generados = [float(r) for r in resultado]

            # Mostrar en el text widget
            self.text_numeros.delete(1.0, tk.END)
            self.text_numeros.insert(tk.END, f"Números generados ({generador}):\n\n")
            for i, num in enumerate(self.numeros_generados, 1):
                self.text_numeros.insert(tk.END, f"{i:3d}: {num:.4f}\n")

            # Crear gráfica de distribución
            self.crear_grafica_distribucion()

            # Aplicar validadores automáticamente
            self.aplicar_validadores()

            messagebox.showinfo("Éxito", f"Se generaron {len(self.numeros_generados)} números y se aplicaron los validadores")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar números: {str(e)}")

    def aplicar_validadores(self):
        if not self.numeros_generados:
            return

        try:
            alfa = float(self.entry_alfa.get())
            self.resultados_validacion = {}

            self.text_resultados.delete(1.0, tk.END)
            self.text_resultados.insert(tk.END, "RESULTADOS DE VALIDACIÓN\n")
            self.text_resultados.insert(tk.END, "="*60 + "\n\n")

            # Aplicar validadores seleccionados
            if self.var_media.get():
                resultado = prueba_media(self.numeros_generados, alfa)
                self.resultados_validacion["Media"] = resultado
                self.mostrar_resultado("Prueba de Media", resultado)

            if self.var_varianza.get():
                resultado = prueba_varianza(self.numeros_generados, alfa)
                self.resultados_validacion["Varianza"] = resultado
                self.mostrar_resultado("Prueba de Varianza", resultado)

            if self.var_chi_cuadrado.get():
                resultado = prueba_chi_cuadrado(self.numeros_generados, alfa=alfa)
                self.resultados_validacion["Chi-Cuadrado"] = resultado
                self.mostrar_resultado("Prueba Chi-Cuadrado", resultado)

            if self.var_ks.get():
                resultado = prueba_ks(self.numeros_generados, alfa)
                self.resultados_validacion["KS"] = resultado
                self.mostrar_resultado("Prueba Kolmogorov-Smirnov", resultado)

            if self.var_corridas_aa.get():
                resultado = prueba_corridas_arriba_abajo(self.numeros_generados, alfa)
                self.resultados_validacion["Corridas AA"] = resultado
                self.mostrar_resultado("Prueba Corridas Arriba/Abajo", resultado)

            if self.var_corridas_media.get():
                resultado = prueba_corridas_media(self.numeros_generados, alfa)
                self.resultados_validacion["Corridas Media"] = resultado
                self.mostrar_resultado("Prueba Corridas Media", resultado)

            if self.var_poker.get():
                resultado = prueba_poker(self.numeros_generados, alfa=alfa)
                self.resultados_validacion["Poker"] = resultado
                self.mostrar_resultado("Prueba Poker", resultado)

            if self.var_series.get():
                resultado = prueba_series(self.numeros_generados, alfa=alfa)
                self.resultados_validacion["Series"] = resultado
                self.mostrar_resultado("Prueba Series", resultado)

            if self.var_huecos.get():
                resultado = prueba_huecos(self.numeros_generados, alfa=alfa)
                self.resultados_validacion["Huecos"] = resultado
                self.mostrar_resultado("Prueba Huecos", resultado)

        except Exception as e:
            messagebox.showerror("Error", f"Error al aplicar validadores: {str(e)}")

    def mostrar_resultado(self, nombre, resultado):
        self.text_resultados.insert(tk.END, f"{nombre}\n")
        self.text_resultados.insert(tk.END, "-"*60 + "\n")
        for clave, valor in resultado.items():
            self.text_resultados.insert(tk.END, f"{clave}: {valor}\n")
        self.text_resultados.insert(tk.END, "\n")

    def crear_grafica_distribucion(self):
        # Limpiar gráficas anteriores
        for widget in self.frame_graficas.winfo_children():
            widget.destroy()

        # Crear figura con dos subplots
        fig = Figure(figsize=(10, 8), dpi=100)

        # Subplot 1: Histograma
        ax1 = fig.add_subplot(211)
        ax1.hist(self.numeros_generados, bins=20, density=True, alpha=0.7,
                color='steelblue', edgecolor='black')
        ax1.axhline(y=1, color='red', linestyle='--', label='Uniforme esperada')
        ax1.set_xlabel('Valor')
        ax1.set_ylabel('Densidad')
        ax1.set_title('Distribución de Números Generados')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Subplot 2: Serie temporal
        ax2 = fig.add_subplot(212)
        ax2.plot(range(len(self.numeros_generados)), self.numeros_generados,
                marker='o', linestyle='-', markersize=3, color='green')
        ax2.axhline(y=0.5, color='red', linestyle='--', label='Media esperada (0.5)')
        ax2.set_xlabel('Índice')
        ax2.set_ylabel('Valor')
        ax2.set_title('Serie Temporal de Números Generados')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        fig.tight_layout()

        # Integrar en tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Cambiar al tab de gráficas
        self.notebook.select(self.tab_graficas)


def main():
    root = tk.Tk()
    app = AplicacionPseudoaleatorios(root)
    root.mainloop()


if __name__ == "__main__":
    main()