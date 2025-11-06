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

st.title("Distribución Uniforme (Discreta)")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Uniforme Discreta es la más simple de todas las distribuciones. Describe un escenario donde hay un número finito de resultados ($n$), y **todos los resultados son igualmente probables**.
    
    - **Parámetros:** Generalmente se define por un rango:
        - $a$: El valor mínimo posible (entero).
        - $b$: El valor máximo posible (entero).
    - **Resultados:** El número total de resultados es $n = b - a + 1$.
    - **Rango:** La variable $X$ puede tomar cualquier valor entero $k \in \{a, a+1, \dots, b\}$.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Es la base de la probabilidad clásica (Laplaciana), donde la probabilidad se define como 'casos favorables / casos posibles'.")
    st.markdown("""
    **Casos de Uso:**
    - El lanzamiento de un dado justo de 6 caras ($a=1, b=6, n=6$).
    - El giro de una ruleta justa con 38 números ($a=1, b=38, n=38$).
    - Elegir una carta al azar de una baraja ($n=52$).
    - Un generador de números aleatorios que produce enteros entre 1 y 100.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Uniforme Continua:** Es la contraparte discreta de la Uniforme Continua, que modela un rango infinito de resultados igualmente probables.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Masa de Probabilidad (PMF)")
    st.write(r"Sea $n = b - a + 1$ el número de resultados. La probabilidad de cualquier resultado $k$ es:")
    st.latex(r"P(X=k) = \frac{1}{n} = \frac{1}{b-a+1} \quad \text{para } k \in \{a, \dots, b\}")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \frac{a+b}{2}")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \frac{n^2 - 1}{12} = \frac{(b-a+1)^2 - 1}{12}")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta los límites $a$ y $b$ para ver la distribución. Siempre será un gráfico plano.")
    
    col1, col2 = st.columns(2)
    with col1:
        a_slider = st.slider("Mínimo (a)", min_value=1, max_value=20, value=1, step=1, key='unif_a_slider')
    with col2:
        b_slider = st.slider("Máximo (b)", min_value=a_slider, max_value=a_slider + 20, value=6, step=1, key='unif_b_slider')

    if a_slider > b_slider:
        st.error("El mínimo 'a' no puede ser mayor que el máximo 'b'.")
    else:
        try:
            # SciPy usa randint(low, high+1)
            dist = stats.randint(low=a_slider, high=b_slider + 1)
            k_values = np.arange(a_slider, b_slider + 1)
            
            fig = plot_discrete_distribution(dist, k_values, f"PMF Uniforme Discreta (a={a_slider}, b={b_slider})")
            ax = fig.gca()
            # Ajustar el eje Y para que se vea mejor
            ax.set_ylim(bottom=0, top=dist.pmf(a_slider) * 1.2)
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula $P(X=k)$ y $P(X \le k)$.")
    
    col1, col2 = st.columns(2)
    with col1:
        calc_a = st.number_input("Mínimo (a)", value=1, step=1, key='unif_calc_a')
    with col2:
        calc_b = st.number_input("Máximo (b)", min_value=calc_a, value=6, step=1, key='unif_calc_b')
        
    n_outcomes = calc_b - calc_a + 1
    calc_k = st.number_input("Valor de k", min_value=calc_a, max_value=calc_b, value=calc_a, step=1, key='unif_calc_k')
        
    if calc_a > calc_b:
        st.error("'a' no puede ser mayor que 'b'.")
    else:
        try:
            dist = stats.randint(low=calc_a, high=calc_b + 1)
            prob_k = dist.pmf(calc_k)
            prob_cdf = dist.cdf(calc_k)
            
            st.subheader("Resultados:")
            st.markdown(f"**Número de resultados (n):** `{n_outcomes}`")
            st.markdown(f"**$P(X = {calc_k})$:** `{prob_k:.6f}`")
            st.markdown(f"**$P(X \le {calc_k})$:** `{prob_cdf:.6f}`")
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Lanzar un dado D6:** El resultado es Uniforme Discreto en $\{1, 2, 3, 4, 5, 6\}$. $P(X=k) = 1/6$.
    2.  **Lotería (un solo dígito):** El último dígito de la lotería, de 0 a 9. $P(X=k) = 1/10$.
    3.  **Simulación:** La función `random.randint(a, b)` en muchos lenguajes de programación genera números que siguen esta distribución.
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("Lanzas un dado justo de 20 caras (un icosaedro), numerado del 1 al 20. ¿Cuál es la probabilidad de sacar *exactamente* un 17?")
    ans1 = st.number_input("Tu respuesta (P(X=17)):", min_value=0.0, max_value=1.0, step=0.001, format="%.3f", key='unif_ex1_ans')
    if st.button("Revisar 1", key='unif_ex1_btn'):
        correct_ans = 1/20
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.3f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.3f}.")
        with st.expander("Ver Solución"):
            st.write(f"Hay $n = 20 - 1 + 1 = 20$ resultados. La probabilidad es $P(X=k) = 1/n$.")
            st.code(f"1 / 20 = 0.050")
    
    st.subheader("Ejercicio 2")
    st.write("En el mismo dado D20 (a=1, b=20), ¿cuál es la probabilidad de sacar 5 *o menos* ($k=5$)?")
    ans2 = st.number_input("Tu respuesta (P(X≤5)):", min_value=0.0, max_value=1.0, step=0.001, format="%.3f", key='unif_ex2_ans')
    if st.button("Revisar 2", key='unif_ex2_btn'):
        correct_ans = stats.randint.cdf(k=5, low=1, high=21)
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.3f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.3f}.")
        with st.expander("Ver Solución"):
            st.write(f"Buscamos $P(X \le 5) = P(X=1) + P(X=2) + P(X=3) + P(X=4) + P(X=5)$.")
            st.write("Como cada uno tiene $P=0.05$, es $5 \times 0.05 = 0.25$.")
            st.code(f"stats.randint.cdf(k=5, low=1, high=21) = 0.250")
            
    st.subheader("Ejercicio 3")
    st.write("¿Cuál es la media (valor esperado) del lanzamiento de un dado D6 ($a=1, b=6$)?")
    ans3 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, step=0.1, format="%.1f", key='unif_ex3_ans')
    if st.button("Revisar 3", key='unif_ex3_btn'):
        correct_ans = (1 + 6) / 2
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.1f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f}.")
        with st.expander("Ver Solución"):
            st.write(f"La media es $\mu = (a+b)/2$.")
            st.code(f"(1 + 6) / 2 = 3.5")
