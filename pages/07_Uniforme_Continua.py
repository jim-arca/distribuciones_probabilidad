import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Importamos la función de ayuda para distribuciones continuas
try:
    from helpers import plot_continuous_distribution
except ImportError:
    st.error("No se pudo importar 'helpers.py'. Asegúrate de que esté en el directorio raíz.")
    st.stop()

# --- Contenido de la Página ---

st.title("Distribución Uniforme (Continua)")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Uniforme Continua modela un escenario donde todos los resultados en un **rango continuo** $[a, b]$ son **igualmente probables**.
    
    A veces se le llama la "distribución rectangular" debido a la forma de su PDF. Es la base de muchos generadores de números aleatorios.
    
    - **Parámetros:**
        - $a$: El valor mínimo posible.
        - $b$: El valor máximo posible ($b > a$).
    - **Rango:** La variable $X$ puede tomar cualquier valor real $x \in [a, b]$.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Es la distribución continua más simple, fundamental en la teoría de la probabilidad y la base para generar otras distribuciones aleatorias (método de la transformada inversa).")
    st.markdown("""
    **Casos de Uso:**
    - **Generadores de números aleatorios:** La mayoría de las funciones `rand()` generan números U(0, 1).
    - **Tiempo de Espera:** El tiempo de espera de un autobús que llega *exactamente* cada 20 minutos (tu tiempo de espera está entre 0 y 20 min).
    - **Errores de Redondeo:** El error al redondear un número al entero más cercano sigue una U(-0.5, 0.5).
    - **Modelado de Incertidumbre:** Cuando solo se conocen los valores mínimo y máximo de un parámetro.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Uniforme Discreta:** Es la contraparte continua de la Uniforme Discreta.
    - **Base para Simulación:** Casi todas las demás distribuciones (Normal, Exponencial, etc.) pueden generarse en una simulación a partir de una secuencia de números U(0, 1).
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.write(r"La PDF es una constante dentro del rango $[a, b]$ y cero fuera de él.")
    st.latex(r"""
    f(x) = 
    \begin{cases} 
    \frac{1}{b-a} & \text{si } a \le x \le b \\
    0 & \text{en otro caso}
    \end{cases}
    """)
    st.write("La altura de la PDF debe ser $1/(b-a)$ para que el área total (base $\times$ altura) sea 1.")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \frac{a+b}{2}")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \frac{(b-a)^2}{12}")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta los límites $a$ y $b$ para ver la distribución rectangular.")
    
    col1, col2 = st.columns(2)
    with col1:
        a_slider = st.slider("Mínimo (a)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5, key='unif_c_a_slider')
    with col2:
        b_slider = st.slider("Máximo (b)", min_value=a_slider + 0.1, max_value=a_slider + 20.0, value=10.0, step=0.5, key='unif_c_b_slider')

    if not b_slider > a_slider:
        st.error("El máximo 'b' debe ser estrictamente mayor que 'a'.")
    else:
        try:
            # SciPy usa loc=a, scale=(b-a)
            dist = stats.uniform(loc=a_slider, scale=b_slider - a_slider)
            
            # Definir rango del gráfico con un margen
            x_min = a_slider - (b_slider - a_slider) * 0.2
            x_max = b_slider + (b_slider - a_slider) * 0.2
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Uniforme Continua (a={a_slider:.1f}, b={b_slider:.1f})")
            ax = fig.gca()
            # Ajustar el eje Y para que se vea mejor
            pdf_height = 1 / (b_slider - a_slider)
            ax.set_ylim(bottom=0, top=pdf_height * 1.2)
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula $P(X \le x)$ (CDF) y $P(x_1 \le X \le x_2)$.")
    
    st.subheader("Parámetros")
    col1, col2 = st.columns(2)
    with col1:
        calc_a = st.number_input("Mínimo (a)", value=0.0, step=0.1, key='unif_c_calc_a')
    with col2:
        calc_b = st.number_input("Máximo (b)", value=10.0, step=0.1, key='unif_c_calc_b')

    if not calc_b > calc_a:
        st.error("'b' debe ser mayor que 'a'.")
    else:
        try:
            dist = stats.uniform(loc=calc_a, scale=calc_b - calc_a)
            
            st.subheader("Cálculo de Probabilidad")
            
            st.write("**1. Probabilidad Acumulada $P(X \le x)$**")
            calc_x = st.number_input("Valor de x", value=(calc_a + calc_b) / 2, step=0.1, key='unif_c_calc_x')
            prob_cdf = dist.cdf(calc_x)
            st.markdown(f"**$P(X \le {calc_x:.2f})$:** `{prob_cdf:.6f}`")

            st.write("**2. Probabilidad de Rango $P(x_1 \le X \le x_2)$**")
            col_a, col_b = st.columns(2)
            with col_a:
                calc_x1 = st.number_input("Límite inferior (x₁)", value=calc_a, step=0.1, key='unif_c_calc_x1')
            with col_b:
                calc_x2 = st.number_input("Límite superior (x₂)", value=calc_b, step=0.1, key='unif_c_calc_x2')
            
            if calc_x1 >= calc_x2:
                st.warning("El límite inferior 'x₁' debe ser menor que 'x₂'.")
            else:
                prob_range = dist.cdf(calc_x2) - dist.cdf(calc_x1)
                st.markdown(f"**$P({calc_x1:.2f} \le X \le {calc_x2:.2f})$:** `{prob_range:.6f}`")

            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
                
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Llegada de Tren:** Un tren llega cada 30 minutos. Si llegas a la estación en un momento aleatorio, tu tiempo de espera sigue una U(0, 30). La prob. de esperar menos de 10 min es $10/30 = 1/3$.
    2.  **Producción:** Un eje de metal debe medir entre 5.0 y 5.1 cm. Si la máquina los produce con una distribución uniforme en ese rango, la prob. de que uno mida entre 5.0 y 5.05 cm es $(5.05 - 5.0) / (5.1 - 5.0) = 0.5$.
    3.  **Simulación:** La función `Math.random()` en JavaScript genera números U(0, 1).
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("Un generador de números aleatorios produce números U(0, 1). ¿Cuál es la altura de la PDF, $f(x)$?")
    ans1 = st.number_input("Tu respuesta (f(x)):", min_value=0.0, step=0.1, format="%.1f", key='unif_c_ex1_ans')
    if st.button("Revisar 1", key='unif_c_ex1_btn'):
        correct_ans = 1.0
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La altura es {correct_ans:.1f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f}.")
        with st.expander("Ver Solución"):
            st.write(f"Aquí $a=0$ y $b=1$. La altura es $f(x) = 1 / (b-a)$.")
            st.code(f"1 / (1 - 0) = 1.0")
    
    st.subheader("Ejercicio 2")
    st.write("Un autobús llega cada 15 minutos ($a=0, b=15$). Si llegas a la parada, ¿cuál es la probabilidad de que esperes *entre* 5 y 10 minutos?")
    ans2 = st.number_input("Tu respuesta (P(5≤X≤10)):", min_value=0.0, max_value=1.0, step=0.001, format="%.3f", key='unif_c_ex2_ans')
    if st.button("Revisar 2", key='unif_c_ex2_btn'):
        correct_ans = (10 - 5) / (15 - 0)
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.3f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.3f}.")
        with st.expander("Ver Solución"):
            st.write(f"La probabilidad es (ancho del rango deseado) / (ancho del rango total).")
            st.code(f"(10 - 5) / (15 - 0) = 5 / 15 = 0.333")
            
    st.subheader("Ejercicio 3")
    st.write("Para el mismo autobús (a=0, b=15), ¿cuál es tu tiempo *esperado* (media) de espera?")
    ans3 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, step=0.1, format="%.1f", key='unif_c_ex3_ans')
    if st.button("Revisar 3", key='unif_c_ex3_btn'):
        correct_ans = (0 + 15) / 2
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.1f} minutos.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f} minutos.")
        with st.expander("Ver Solución"):
            st.write(f"La media es $\mu = (a+b)/2$.")
            st.code(f"(0 + 15) / 2 = 7.5")
