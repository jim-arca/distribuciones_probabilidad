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

st.title("Distribución de Weibull")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución de Weibull es una distribución continua extremadamente flexible, usada principalmente en **ingeniería de confiabilidad** y **análisis de supervivencia** para modelar el **tiempo hasta el fallo**.
    
    Su gran ventaja es que puede modelar diferentes tipos de tasas de fallo, dependiendo del valor de su parámetro de forma.
    
    - **Parámetros:**
        - $k$ (o $c$): El parámetro de **forma** ($k > 0$). Es el más importante.
        - $\lambda$ (o $scale$): El parámetro de **escala** ($\lambda > 0$).
    - **Rango:** La variable $X$ (tiempo) puede tomar valores $x \ge 0$.
    """)
    st.subheader("La importancia del parámetro de Forma (k):")
    st.markdown("""
    - **$k < 1$ (Tasa de fallo decreciente):** Fallos "infantiles". Los productos defectuosos fallan rápido. La prob. de fallo disminuye con el tiempo.
    - **$k = 1$ (Tasa de fallo constante):** ¡Es idéntica a la **Distribución Exponencial**! Los fallos son aleatorios (sin memoria).
    - **$k > 1$ (Tasa de fallo creciente):** Fallos por "desgaste" (wear-out). La prob. de fallo aumenta con el tiempo a medida que el producto envejece.
    """)
    st.info("Nota: SciPy usa `c` para la forma ($k$) y `scale` para la escala ($\lambda$).")

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Desarrollada por el ingeniero sueco **Waloddi Weibull** en 1939 para describir la resistencia de los materiales.")
    st.markdown("""
    **Casos de Uso:**
    - **Ingeniería:** Tiempo de vida de rodamientos, condensadores, o cualquier componente mecánico/electrónico.
    - **Meteorología:** Modelar la velocidad del viento.
    - **Medicina:** Tiempos de supervivencia de pacientes después de un tratamiento.
    - **Seguros:** Modelar el tamaño de reclamaciones (similar a Lognormal).
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Exponencial:** La Weibull($k=1, \lambda$) es exactamente la Exponencial(escala=$\lambda$).
    - **Rayleigh:** Usada en física, es un caso especial de Weibull con $k=2$.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.latex(r"f(x) = \frac{k}{\lambda} \left( \frac{x}{\lambda} \right)^{k-1} e^{-(x/\lambda)^k} \quad \text{para } x \ge 0")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \lambda \Gamma(1 + 1/k)")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \lambda^2 \left[ \Gamma(1 + 2/k) - (\Gamma(1 + 1/k))^2 \right]")
    st.write(r"Donde $\Gamma$ es la función Gamma.")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta $k$ (forma) y $\lambda$ (escala). Observa el cambio drástico en $k=1$.")
    
    col1, col2 = st.columns(2)
    with col1:
        k_slider = st.slider("Forma (k)", min_value=0.1, max_value=5.0, value=2.0, step=0.1, key='weibull_k')
    with col2:
        lambda_slider = st.slider("Escala (λ)", min_value=0.1, max_value=20.0, value=10.0, step=0.5, key='weibull_lambda')

    if k_slider <= 0 or lambda_slider <= 0:
        st.error("k y λ deben ser positivos.")
    else:
        try:
            # SciPy usa c=k, scale=lambda
            dist = stats.weibull_min(c=k_slider, scale=lambda_slider)
            
            x_min = 0
            x_max = dist.ppf(0.995) # Graficar hasta el 99.5%
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Weibull (k={k_slider:.1f}, λ={lambda_slider:.1f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva (Completa)")
    st.write("Calcula $P(X \le x)$ (prob. de fallo *antes* de $x$) y $P(X > x)$ (prob. de *supervivencia*).")
    
    st.subheader("Parámetros")
    col1, col2 = st.columns(2)
    with col1:
        calc_k = st.number_input("Forma (k)", min_value=0.01, value=2.0, step=0.1, key='weibull_calc_k')
    with col2:
        calc_lambda = st.number_input("Escala (λ)", min_value=0.01, value=10.0, step=0.1, key='weibull_calc_lambda')
    
    st.subheader("Cálculo de Probabilidad")
    calc_x = st.number_input("Tiempo (x)", min_value=0.0, value=10.0, step=0.1, key='weibull_calc_x')

    if calc_k <= 0 or calc_lambda <= 0 or calc_x < 0:
        st.error("'k' y 'λ' deben ser positivos, 'x' debe ser >= 0.")
    else:
        try:
            dist = stats.weibull_min(c=calc_k, scale=calc_lambda)
            
            prob_cdf = dist.cdf(calc_x)
            prob_sf = dist.sf(calc_x) # Survival function (1 - cdf)
            
            st.subheader("Resultados:")
            st.markdown(f"**$P(X \le {calc_x:.2f})$:** `{prob_cdf:.6f}` (Prob. de fallo *antes* de {calc_x})")
            st.markdown(f"**$P(X > {calc_x:.2f})$:** `{prob_sf:.6f}` (Prob. de *sobrevivir más allá* de {calc_x})")
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}` (Tiempo medio de fallo)")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
                
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Garantía de Producto:** Un rodamiento falla con Weibull($k=2, \lambda=5000$ horas). $k=2$ indica desgaste. ¿Qué prob. hay de que falle antes de 1000 horas? $P(X \le 1000)$.
    2.  **Velocidad del Viento:** La velocidad del viento en un parque eólico sigue Weibull($k=1.8, \lambda=8$ m/s). ¿Prob. de que el viento esté entre 5 y 10 m/s?
    3.  **Mortalidad Infantil:** Ciertos componentes electrónicos fallan con $k=0.7$ (tasa decreciente). La mayoría de los fallos ocurren al principio (quemado inicial).
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1: Identificación")
    st.write("¿Qué distribución es idéntica a una Weibull con parámetro de forma $k=1$?")
    ans1 = st.text_input("Tu respuesta (Nombre de la distribución):", key='weibull_ex1_ans').strip().lower()
    if st.button("Revisar 1", key='weibull_ex1_btn'):
        if "exponencial" in ans1:
            st.success("¡Correcto! Es la Distribución Exponencial.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es 'Exponencial'.")
        with st.expander("Ver Solución"):
            st.write(f"Cuando $k=1$, la PDF de Weibull se simplifica a $f(x) = (1/\lambda) e^{{-(x/\lambda)}}$, que es la PDF de la Exponencial con escala $\lambda$. Ambas modelan fallos aleatorios.")
    
    st.subheader("Ejercicio 2: Conceptual")
    st.write("Un ingeniero modela el tiempo de fallo de un motor. Observa que los fallos son raros al principio, pero aumentan drásticamente a medida que los motores envejecen. ¿Qué rango de $k$ debería usar?")
    ans2 = st.text_input("Tu respuesta (Ej: 'k=1', 'k<1', 'k>1'):", key='weibull_ex2_ans').strip().lower()
    if st.button("Revisar 2", key='weibull_ex2_btn'):
        if ans2 == "k>1":
            st.success("¡Correcto! $k>1$ modela fallos por desgaste (tasa de fallo creciente).")
        else:
            st.error(f"Incorrecto. La respuesta correcta es $k>1$.")
        
    st.subheader("Ejercicio 3: Cálculo")
    st.write("Un componente tiene $k=1$ y $\lambda=500$ horas. ¿Cuál es la prob. de que falle *antes* de $x=500$ horas?")
    ans3 = st.number_input("Tu respuesta (P(X≤500)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='weibull_ex3_ans')
    if st.button("Revisar 3", key='weibull_ex3_btn'):
        dist_ex = stats.weibull_min(c=1, scale=500)
        correct_ans = dist_ex.cdf(500)
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Esto es una Exponencial con media $\lambda=500$. Buscamos $P(X \le 500)$.")
            st.latex(r"CDF = $1 - e^{-(x/\lambda)^k} = 1 - e^{-(500/500)^1} = 1 - e^{-1}$")
            st.code(f"1 - np.exp(-1) = {correct_ans:.4f}")
