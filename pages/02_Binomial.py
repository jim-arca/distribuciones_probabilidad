import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Importamos la función de ayuda
try:
    from helpers import plot_discrete_distribution
except ImportError:
    st.error("No se pudo importar 'helpers.py'. Asegúrate de que esté en el directorio raíz.")
    st.stop()

# --- Contenido de la Página Binomial ---

st.title("Distribución Binomial")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Binomial modela el **número de éxitos** $k$ en una secuencia de **$n$ ensayos de Bernoulli independientes** e idénticos, cada uno con una probabilidad de éxito $p$.
    
    Es fundamental para modelar escenarios de conteo donde cada intento es independiente y tiene solo dos resultados.
    
    - **Parámetros:** - $n$: Número total de ensayos (entero, $n \ge 1$).
        - $p$: Probabilidad de éxito en cada ensayo ($0 \le p \le 1$).
    - **Rango:** La variable $X$ puede tomar valores enteros $k$ desde $0$ hasta $n$.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("La distribución binomial es uno de los pilares de la teoría de la probabilidad, también desarrollada extensamente por **Jakob Bernoulli**.")
    st.markdown("""
    **Casos de Uso:**
    - El número de "Caras" obtenidas al lanzar una moneda 20 veces.
    - El número de productos defectuosos en un lote de 100.
    - El número de pacientes que se recuperan en un grupo de 50 que recibieron un tratamiento.
    - El número de preguntas respondidas correctamente al azar en un examen de opción múltiple.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Bernoulli:** La Binomial es la suma de $n$ distribuciones de Bernoulli(p). Una Binomial(n=1, p) es exactamente una Bernoulli(p).
    - **Poisson:** Cuando $n$ es muy grande y $p$ es muy pequeña, la distribución Binomial(n, p) se puede aproximar muy bien por una Distribución de Poisson con $\lambda = n \cdot p$.
    - **Normal:** Cuando $n$ es grande (especialmente si $np \ge 5$ y $n(1-p) \ge 5$), la Binomial se puede aproximar por una Distribución Normal con $\mu = np$ y $\sigma^2 = np(1-p)$.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Masa de Probabilidad (PMF)")
    st.latex(r"P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}")
    st.write(r"Donde $\binom{n}{k} = \frac{n!}{k!(n-k)!}$ es el coeficiente binomial, que representa el número de formas de elegir $k$ éxitos de $n$ ensayos.")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = np")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = np(1-p)")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta $n$ y $p$ para ver cómo cambia la forma de la distribución.")
    
    col1, col2 = st.columns(2)
    with col1:
        n_slider = st.slider("Número de ensayos (n)", min_value=1, max_value=100, value=20, step=1, key='bin_n_slider')
    with col2:
        p_slider = st.slider("Probabilidad de éxito (p)", min_value=0.01, max_value=0.99, value=0.5, step=0.01, key='bin_p_slider')
    
    # Validación
    if not (0.01 <= p_slider <= 0.99) or not (n_slider >= 1):
        st.error("Parámetros inválidos. 'n' debe ser >= 1 y 'p' debe estar en [0.01, 0.99].")
    else:
        try:
            dist = stats.binom(n=n_slider, p=p_slider)
            k_values = np.arange(0, n_slider + 1)
            fig = plot_discrete_distribution(dist, k_values, f"PMF Binomial (n={n_slider}, p={p_slider:.2f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula $P(X=k)$ (PMF) y $P(X \le k)$ (CDF) para una Binomial.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        calc_n = st.number_input("Número de ensayos (n)", min_value=1, value=20, step=1, key='bin_calc_n')
    with col2:
        calc_p = st.number_input("Probabilidad (p)", min_value=0.0, max_value=1.0, value=0.5, step=0.01, key='bin_calc_p')
    with col3:
        # Aseguramos que k no pueda ser mayor que n dinámicamente
        calc_k = st.number_input("Valor de k", min_value=0, max_value=calc_n, value=min(10, calc_n), step=1, key='bin_calc_k')

    # Validación
    if not (0 <= calc_p <= 1):
        st.error("La probabilidad 'p' debe estar entre 0 y 1.")
    elif calc_k > calc_n:
        st.error("El valor 'k' no puede ser mayor que 'n'. (Ajusta 'n' primero)")
    elif calc_k < 0:
        st.error("'k' no puede ser negativo.")
    else:
        try:
            dist = stats.binom(n=calc_n, p=calc_p)
            prob_k = dist.pmf(calc_k)
            prob_cdf = dist.cdf(calc_k)
            prob_gt_k = 1 - prob_cdf
            prob_gte_k = 1 - dist.cdf(calc_k - 1) if calc_k > 0 else 1.0
            
            st.subheader("Resultados:")
            st.markdown(f"**$P(X = {calc_k})$:** `{prob_k:.6f}` (Prob. de *exactamente* {calc_k} éxitos)")
            st.markdown(f"**$P(X \le {calc_k})$:** `{prob_cdf:.6f}` (Prob. de *como máximo* {calc_k} éxitos)")
            st.markdown(f"**$P(X > {calc_k})$:** `{prob_gt_k:.6f}` (Prob. de *más de* {calc_k} éxitos)")
            st.markdown(f"**$P(X \ge {calc_k})$:** `{prob_gte_k:.6f}` (Prob. de *al menos* {calc_k} éxitos)")
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Exámenes:** Un estudiante responde 10 preguntas de verdadero/falso al azar (p=0.5). ¿Cuál es la probabilidad de que acierte exactamente 8? (n=10, p=0.5, k=8).
    2.  **Calidad:** Un fabricante sabe que el 2% de sus chips son defectuosos (p=0.02). Si un cliente compra un lote de 500 chips (n=500), ¿cuál es la probabilidad de que 15 o más sean defectuosos? (Calcular $P(X \ge 15)$).
    3.  **Genética:** Un par de padres tiene una probabilidad de 0.25 de tener un hijo con ojos azules (p=0.25). Si tienen 4 hijos (n=4), ¿cuál es la probabilidad de que 2 de ellos tengan ojos azules? (k=2).
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("Lanzas una moneda justa 15 veces (n=15, p=0.5). ¿Cuál es la probabilidad de obtener *exactamente* 7 caras (k=7)?")
    ans1 = st.number_input("Tu respuesta (P(X=7)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='bin_ex1_ans')
    if st.button("Revisar 1", key='bin_ex1_btn'):
        correct_ans = stats.binom.pmf(k=7, n=15, p=0.5)
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Usamos la PMF Binomial: $P(X=7) = \\binom{{15}}{{7}} (0.5)^7 (1-0.5)^{{15-7}}$")
            st.code(f"stats.binom.pmf(k=7, n=15, p=0.5) = {correct_ans:.4f}")
    
    st.subheader("Ejercicio 2")
    st.write("Un 10% de la población es zurda (p=0.1). En una clase de 20 estudiantes (n=20), ¿cuál es la probabilidad de que *como máximo* 2 sean zurdos (k=2)?")
    ans2 = st.number_input("Tu respuesta (P(X≤2)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='bin_ex2_ans')
    if st.button("Revisar 2", key='bin_ex2_btn'):
        correct_ans = stats.binom.cdf(k=2, n=20, p=0.1)
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Buscamos la CDF: $P(X \le 2) = P(X=0) + P(X=1) + P(X=2)$.")
            st.code(f"stats.binom.cdf(k=2, n=20, p=0.1) = {correct_ans:.4f}")
            
    st.subheader("Ejercicio 3")
    st.write("En el mismo escenario (n=20, p=0.1), ¿cuál es el número *esperado* (media) de estudiantes zurdos en la clase?")
    ans3 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, max_value=20.0, step=0.1, format="%.1f", key='bin_ex3_ans')
    if st.button("Revisar 3", key='bin_ex3_btn'):
        correct_ans = 20 * 0.1
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.1f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f}.")
        with st.expander("Ver Solución"):
            st.write(f"La media de una binomial es $\mu = np$.")
            st.code(f"20 * 0.1 = 2.0")
