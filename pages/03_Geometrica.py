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

# --- Contenido de la Página ---

st.title("Distribución Geométrica")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Geométrica modela el número de ensayos de Bernoulli (independientes, con probabilidad de éxito $p$) necesarios **hasta obtener el primer éxito**.
    
    Es la contraparte de la Binomial, que cuenta éxitos en un número fijo de ensayos. La Geométrica cuenta ensayos hasta un número fijo de éxitos (uno).
    
    - **Parámetro:** $p$ (probabilidad de éxito en cada ensayo), $0 < p \le 1$.
    - **Rango:** La variable $X$ (número de ensayos) puede tomar valores $k = 1, 2, 3, ...$
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Es una de las distribuciones más simples basadas en los ensayos de Bernoulli. Es fundamental en la teoría de la probabilidad para modelar tiempos de espera.")
    st.markdown("""
    **Casos de Uso:**
    - El número de veces que necesitas lanzar una moneda hasta que salga "Cara".
    - El número de clientes que un vendedor debe contactar hasta cerrar la primera venta.
    - El número de controles de calidad en una línea de producción hasta encontrar el primer artículo defectuoso.
    - Un jugador de baloncesto lanzando tiros libres hasta encestar el primero.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Bernoulli:** La Geométrica es una secuencia de ensayos de Bernoulli(p) que se detiene en el primer éxito.
    - **Binomial Negativa:** Es un caso especial de la Binomial Negativa (que cuenta ensayos hasta $r$ éxitos). La Geométrica es una Binomial Negativa con $r=1$.
    - **Exponencial:** La Geométrica es la contraparte discreta de la Distribución Exponencial (que modela el tiempo de espera continuo hasta un evento).
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Masa de Probabilidad (PMF)")
    st.write(r"La probabilidad de que el primer éxito ocurra en el $k$-ésimo ensayo es:")
    st.latex(r"P(X=k) = (1-p)^{k-1} p \quad \text{para } k = 1, 2, 3, \dots")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \frac{1}{p}")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \frac{1-p}{p^2}")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta la probabilidad de éxito ($p$) para ver cómo cambia la distribución. Una $p$ alta significa que el éxito es más probable y se espera antes.")
    
    p_slider = st.slider("Probabilidad de éxito (p)", min_value=0.01, max_value=0.99, value=0.25, step=0.01, key='geom_p_slider')
    
    if not (0.01 <= p_slider <= 0.99):
        st.error("La probabilidad 'p' debe estar en [0.01, 0.99].")
    else:
        try:
            dist = stats.geom(p=p_slider)
            # Graficar los primeros 25 ensayos o hasta que la prob. sea muy baja
            k_max = max(25, int(dist.mean() * 3))
            k_values = np.arange(1, k_max + 1)
            
            fig = plot_discrete_distribution(dist, k_values, f"PMF Geométrica (p={p_slider:.2f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula $P(X=k)$ y $P(X \le k)$ para una Geométrica.")
    
    col1, col2 = st.columns(2)
    with col1:
        calc_p = st.number_input("Probabilidad (p)", min_value=0.01, max_value=1.0, value=0.25, step=0.01, key='geom_calc_p')
    with col2:
        calc_k = st.number_input("Número de ensayos (k)", min_value=1, value=5, step=1, key='geom_calc_k')

    if not (0.01 <= calc_p <= 1.0):
        st.error("'p' debe estar en [0.01, 1.0].")
    elif calc_k < 1:
        st.error("'k' debe ser >= 1.")
    else:
        try:
            dist = stats.geom(p=calc_p)
            prob_k = dist.pmf(calc_k)
            prob_cdf = dist.cdf(calc_k)
            prob_gt_k = 1 - prob_cdf # P(X > k)
            
            st.subheader("Resultados:")
            st.markdown(f"**$P(X = {calc_k})$:** `{prob_k:.6f}` (Prob. del 1er éxito *exactamente* en el ensayo {calc_k})")
            st.markdown(f"**$P(X \le {calc_k})$:** `{prob_cdf:.6f}` (Prob. del 1er éxito *en o antes* del ensayo {calc_k})")
            st.markdown(f"**$P(X > {calc_k})$:** `{prob_gt_k:.6f}` (Prob. de necesitar *más de* {calc_k} ensayos)")
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}` (Número esperado de ensayos hasta el éxito)")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Juegos de Azar:** La probabilidad de sacar un "6" en un dado es $p=1/6$. El número de lanzamientos hasta sacar el primer 6 sigue una Geom(p=1/6).
    2.  **Marketing:** Si un vendedor por teléfono tiene una tasa de éxito del 5% ($p=0.05$), el número de llamadas que debe hacer hasta conseguir su primera venta sigue una Geom(p=0.05).
    3.  **Biología:** Un pájaro tiene una probabilidad de $p=0.15$ de encontrar comida en un tipo de arbusto. El número de arbustos que inspecciona hasta encontrar comida sigue una Geom(p=0.15).
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("La probabilidad de encestar un tiro libre es 0.7 ($p=0.7$). ¿Cuál es la probabilidad de que un jugador falle los dos primeros y enceste *exactamente* en el tercero ($k=3$)?")
    ans1 = st.number_input("Tu respuesta (P(X=3)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='geom_ex1_ans')
    if st.button("Revisar 1", key='geom_ex1_btn'):
        correct_ans = stats.geom.pmf(k=3, p=0.7)
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Buscamos $P(X=3) = (1-p)^{{k-1}} p = (1-0.7)^{{3-1}} (0.7) = (0.3)^2 (0.7)$")
            st.code(f"(0.3 * 0.3 * 0.7) = 0.063")
    
    st.subheader("Ejercicio 2")
    st.write("En el mismo escenario ($p=0.7$), ¿cuál es la probabilidad de que necesite *como máximo* 2 intentos para encestar? ($k=2$)")
    ans2 = st.number_input("Tu respuesta (P(X≤2)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='geom_ex2_ans')
    if st.button("Revisar 2", key='geom_ex2_btn'):
        correct_ans = stats.geom.cdf(k=2, p=0.7)
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Buscamos $P(X \le 2) = P(X=1) + P(X=2) = 0.7 + (0.3)(0.7) = 0.7 + 0.21$")
            st.code(f"stats.geom.cdf(k=2, p=0.7) = 0.91")
            
    st.subheader("Ejercicio 3")
    st.write("Si la probabilidad de que una máquina falle en un día es $p=0.02$, ¿cuál es el número *esperado* de días hasta el primer fallo?")
    ans3 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, step=1.0, format="%.1f", key='geom_ex3_ans')
    if st.button("Revisar 3", key='geom_ex3_btn'):
        correct_ans = 1 / 0.02
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.1f} días.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f} días.")
        with st.expander("Ver Solución"):
            st.write(f"La media de una geométrica es $\mu = 1/p$.")
            st.code(f"1 / 0.02 = 50.0")
