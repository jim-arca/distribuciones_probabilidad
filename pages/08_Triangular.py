import streamlit as st
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Importamos la función de ayuda
try:
    from helpers import plot_continuous_distribution
except ImportError:
    st.error("No se pudo importar 'helpers.py'. Asegúrate de que esté en el directorio raíz.")
    st.stop()

# --- Contenido de la Página ---

st.title("Distribución Triangular")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Triangular es una distribución continua definida por tres puntos: un mínimo $a$, un máximo $b$, y un modo (pico) $c$, donde $a \le c \le b$.
    
    Es muy utilizada en **simulación de negocios** y **gestión de proyectos (PERT)** cuando solo se pueden estimar los escenarios mínimo, más probable (modo) y máximo para una variable.
    
    - **Parámetros:**
        - $a$: Valor mínimo.
        - $b$: Valor máximo ($b > a$).
        - $c$: Modo (valor más probable), $a \le c \le b$.
    - **Rango:** La variable $X$ puede tomar cualquier valor real $x \in [a, b]$.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Su popularidad no viene de un origen físico (como la Normal), sino de su utilidad práctica en la estimación y simulación. Es una "distribución de bajo conocimiento", útil cuando no hay datos suficientes para justificar una distribución más compleja.")
    st.markdown("""
    **Casos de Uso:**
    - **Gestión de Proyectos:** Estimar la duración de una tarea (optimista $a$, pesimista $b$, más probable $c$).
    - **Análisis de Riesgo:** Modelar el impacto financiero de un riesgo.
    - **Costos:** Estimar el costo de un componente con incertidumbre.
    - **Simulación Monte Carlo:** Cuando se necesita una entrada subjetiva de expertos.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Uniforme Continua:** Si $c = a = b$ (conceptual) o si $c$ se acerca a $a$ o $b$, se deforma. Si $c = (a+b)/2$, es simétrica. Si $a=c$ o $b=c$, se convierte en un triángulo rectángulo.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.write(r"La PDF es una función lineal a trozos (dos líneas que forman un triángulo).")
    st.latex(r"""
    f(x) = 
    \begin{cases} 
    \frac{2(x-a)}{(b-a)(c-a)} & \text{si } a \le x \le c \\
    \frac{2(b-x)}{(b-a)(b-c)} & \text{si } c < x \le b \\
    0 & \text{en otro caso}
    \end{cases}
    """)
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \frac{a+b+c}{3}")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \frac{a^2 + b^2 + c^2 - ab - ac - bc}{18}")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta los parámetros $a, b, c$ para ver la forma del triángulo.")
    
    col1, col2 = st.columns(2)
    with col1:
        a_slider = st.slider("Mínimo (a)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5, key='tri_a')
    with col2:
        b_slider = st.slider("Máximo (b)", min_value=a_slider + 1.0, max_value=a_slider + 20.0, value=10.0, step=0.5, key='tri_b')
    
    # c debe estar entre a y b
    c_slider = st.slider("Modo (c)", min_value=a_slider, max_value=b_slider, value=(a_slider + b_slider) / 2, step=0.5, key='tri_c')

    if not (a_slider <= c_slider <= b_slider and b_slider > a_slider):
        st.error("Parámetros inválidos. Asegúrate de que $a \le c \le b$ y $a < b$.")
    else:
        try:
            # SciPy usa 'c' como un factor (c-a)/(b-a)
            c_scaled = (c_slider - a_slider) / (b_slider - a_slider)
            dist = stats.triang(c=c_scaled, loc=a_slider, scale=b_slider - a_slider)
            
            x_min = a_slider - (b_slider - a_slider) * 0.1
            x_max = b_slider + (b_slider - a_slider) * 0.1
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Triangular (a={a_slider:.1f}, c={c_slider:.1f}, b={b_slider:.1f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula $P(X \le x)$ (CDF) y $P(x_1 \le X \le x_2)$.")
    
    st.subheader("Parámetros")
    col1, col2, col3 = st.columns(3)
    with col1:
        calc_a = st.number_input("Mínimo (a)", value=0.0, step=0.1, key='tri_calc_a')
    with col2:
        calc_c = st.number_input("Modo (c)", value=5.0, step=0.1, key='tri_calc_c')
    with col3:
        calc_b = st.number_input("Máximo (b)", value=10.0, step=0.1, key='tri_calc_b')

    if not (calc_a <= calc_c <= calc_b and calc_b > calc_a):
        st.error("Parámetros inválidos. Asegúrate de que $a \le c \le b$ y $a < b$.")
    else:
        try:
            c_scaled_calc = (calc_c - calc_a) / (calc_b - calc_a)
            dist = stats.triang(c=c_scaled_calc, loc=calc_a, scale=calc_b - calc_a)
            
            st.subheader("Cálculo de Probabilidad")
            
            st.write("**1. Probabilidad Acumulada $P(X \le x)$**")
            calc_x = st.number_input("Valor de x", value=(calc_a + calc_b) / 2, step=0.1, key='tri_calc_x')
            prob_cdf = dist.cdf(calc_x)
            st.markdown(f"**$P(X \le {calc_x:.2f})$:** `{prob_cdf:.6f}`")

            st.write("**2. Probabilidad de Rango $P(x_1 \le X \le x_2)$**")
            col_a, col_b = st.columns(2)
            with col_a:
                calc_x1 = st.number_input("Límite inferior (x₁)", value=calc_a, step=0.1, key='tri_calc_x1')
            with col_b:
                calc_x2 = st.number_input("Límite superior (x₂)", value=calc_b, step=0.1, key='tri_calc_x2')
            
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
    1.  **Duración de Tarea:** Una tarea tomará: Mínimo 8 días ($a=8$), Máximo 20 días ($b=20$), Más probable 10 días ($c=10$). ¿Prob. de terminar en 12 días o menos?
    2.  **Ventas de Producto:** Se espera vender: Mínimo 1000 unidades ($a=1000$), Máximo 6000 ($b=6000$), Más probable 5000 ($c=5000$).
    3.  **Tiempo de Conducción:** El viaje al trabajo toma: Mínimo 25 min, Máximo 55 min, Más probable 30 min.
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("Para una tarea con $a=10, b=30, c=15$, ¿cuál es la duración media (esperada) de la tarea?")
    ans1 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, step=0.1, format="%.2f", key='tri_ex1_ans')
    if st.button("Revisar 1", key='tri_ex1_btn'):
        correct_ans = (10 + 30 + 15) / 3
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.2f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(f"La media es $\mu = (a+b+c)/3$.")
            st.code(f"(10 + 30 + 15) / 3 = 55 / 3 = 18.33")
    
    st.subheader("Ejercicio 2")
    st.write("Un proyecto tiene $a=5, b=15, c=10$ (distribución simétrica). ¿Cuál es la probabilidad de que dure *exactamente* 10 días?")
    ans2 = st.number_input("Tu respuesta (P(X=10)):", min_value=0.0, max_value=1.0, step=0.1, format="%.1f", key='tri_ex2_ans')
    if st.button("Revisar 2", key='tri_ex2_btn'):
        if np.isclose(ans2, 0.0):
            st.success("¡Correcto! La probabilidad es 0.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es 0.")
        with st.expander("Ver Solución"):
            st.write("¡Pregunta trampa! Para *cualquier* distribución continua, la probabilidad de un punto exacto (ej. $P(X=10.000...)$) es siempre 0. La probabilidad solo existe sobre un rango (un área bajo la PDF).")
            
    st.subheader("Ejercicio 3")
    st.write("En el mismo proyecto $a=5, b=15, c=10$, ¿cuál es la probabilidad de que dure 10 días *o menos* ($P(X \le 10)$)?")
    ans3 = st.number_input("Tu respuesta (P(X≤10)):", min_value=0.0, max_value=1.0, step=0.01, format="%.2f", key='tri_ex3_ans')
    if st.button("Revisar 3", key='tri_ex3_btn'):
        c_scaled_ex = (10 - 5) / (15 - 5)
        dist_ex = stats.triang(c=c_scaled_ex, loc=5, scale=15 - 5)
        correct_ans = dist_ex.cdf(10) # Debería ser 0.5
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.2f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(f"Dado que la distribución es simétrica ($c$ está justo en el medio de $a$ y $b$), la media y el modo son 10. La probabilidad de estar por debajo de la media es 0.5 (50%).")
            st.code(f"stats.triang(c=0.5, loc=5, scale=10).cdf(10) = 0.50")
