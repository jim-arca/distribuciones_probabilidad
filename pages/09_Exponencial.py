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

st.title("Distribución Exponencial")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Exponencial es una distribución continua que modela el **tiempo entre eventos** en un proceso de Poisson (donde los eventos ocurren a una tasa media constante $\lambda$).
    
    Si la *cantidad* de eventos sigue una Poisson, el *tiempo entre* ellos sigue una Exponencial.
    
    Su característica clave es la **propiedad de "falta de memoria"**: la probabilidad de que un evento ocurra en el futuro es independiente de cuánto tiempo ha pasado. (Ej. El tiempo de espera restante para el autobús es el mismo, no importa si acabas de llegar o llevas 10 min).
    
    - **Parámetro:**
        - $\lambda$ (lambda): La **tasa** de eventos (ej. 5 clientes/hora).
        - $\beta$ (beta): La **escala** o tiempo medio entre eventos ($\beta = 1/\lambda$, ej. 1/5 = 0.2 horas/cliente).
    - **Rango:** La variable $X$ (tiempo) puede tomar valores $x \ge 0$.
    """)
    st.info("Nota: SciPy usa el parámetro de escala $\beta$ (scale), donde $\beta = 1/\lambda$.")

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Es fundamental en la teoría de colas (líneas de espera) y en la ingeniería de confiabilidad.")
    st.markdown("""
    **Casos de Uso:**
    - **Fiabilidad:** El tiempo hasta que una bombilla o componente electrónico falla.
    - **Teoría de Colas:** El tiempo entre la llegada de clientes a un cajero.
    - **Física:** El tiempo que tarda una partícula radiactiva en desintegrarse.
    - **Telecomunicaciones:** Duración de las llamadas telefónicas.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Poisson:** Son dos caras de la misma moneda. Poisson cuenta eventos en un tiempo; Exponencial mide el tiempo entre eventos.
    - **Gamma:** La Exponencial es un caso especial de la Gamma (con $\alpha=1$). La Gamma modela el tiempo hasta que ocurren $k$ (o $\alpha$) eventos.
    - **Geométrica:** La Exponencial es la contraparte continua de la Geométrica.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.write(r"En términos de la tasa $\lambda$:")
    st.latex(r"f(x) = \lambda e^{-\lambda x} \quad \text{para } x \ge 0")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \frac{1}{\lambda} = \beta")
    st.write(r"El tiempo medio hasta el próximo evento es $1/\lambda$.")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \frac{1}{\lambda^2} = \beta^2")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta la tasa ($\lambda$). Una tasa alta significa eventos frecuentes (tiempos cortos), empujando la curva hacia la izquierda.")
    
    lambda_slider = st.slider("Tasa (λ)", min_value=0.1, max_value=10.0, value=1.0, step=0.1, key='exp_lambda')
    
    if lambda_slider <= 0:
        st.error("Lambda (λ) debe ser positiva.")
    else:
        try:
            # SciPy usa scale = 1 / lambda
            beta_scale = 1.0 / lambda_slider
            dist = stats.expon(scale=beta_scale)
            
            # Graficar hasta 3 veces la media
            x_max = 3 * dist.mean()
            
            fig = plot_continuous_distribution(dist, 0, x_max, f"PDF Exponencial (λ={lambda_slider:.1f}, media β={beta_scale:.2f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula $P(X \le x)$ (prob. de que el evento ocurra *antes* de $x$) y $P(X > x)$ (prob. de que dure *más* de $x$).")
    
    st.subheader("Parámetros")
    calc_lambda = st.number_input("Tasa (λ) (eventos por unidad de tiempo)", min_value=0.01, value=1.0, step=0.1, key='exp_calc_lambda')
    
    st.subheader("Cálculo de Probabilidad")
    calc_x = st.number_input("Tiempo (x)", min_value=0.0, value=1.0, step=0.1, key='exp_calc_x')

    if calc_lambda <= 0 or calc_x < 0:
        st.error("'λ' debe ser positiva y 'x' debe ser >= 0.")
    else:
        try:
            beta_scale_calc = 1.0 / calc_lambda
            dist = stats.expon(scale=beta_scale_calc)
            
            prob_cdf = dist.cdf(calc_x)
            prob_sf = dist.sf(calc_x) # Survival function (1 - cdf)
            
            st.subheader("Resultados:")
            st.markdown(f"**$P(X \le {calc_x:.2f})$:** `{prob_cdf:.6f}` (Prob. de que el evento ocurra *antes* de {calc_x})")
            st.markdown(f"**$P(X > {calc_x:.2f})$:** `{prob_sf:.6f}` (Prob. de que el evento ocurra *después* de {calc_x})")
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ = 1/λ):** `{dist.mean():.4f}` (Tiempo medio entre eventos)")
            st.markdown(f"**Varianza (σ² = 1/λ²):** `{dist.var():.4f}`")
                
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Fiabilidad:** La vida útil de una batería sigue una Exp(λ=0.1 fallos/año). ¿Prob. de que falle antes de 5 años? $P(X \le 5)$.
    2.  **Atención al Cliente:** Los clientes llegan a un banco a una tasa de $\lambda=20$ clientes/hora. El tiempo entre llegadas es Exp($\lambda=20$). ¿Prob. de que el próximo cliente tarde más de 5 minutos? (CUIDADO: 5 min = 1/12 horas).
    3.  **Llamadas:** La duración de una llamada es Exp con media 3 minutos ($\mu = 3$, $\lambda=1/3$). ¿Prob. de que una llamada dure más de 2 minutos? $P(X > 2)$.
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("Los clientes llegan a una tasa $\lambda=4$ por hora. ¿Cuál es el tiempo medio (esperado) entre llegadas?")
    ans1 = st.number_input("Tu respuesta (Media μ en horas):", min_value=0.0, step=0.01, format="%.2f", key='exp_ex1_ans')
    if st.button("Revisar 1", key='exp_ex1_btn'):
        correct_ans = 1 / 4
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.2f} horas (o 15 min).")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.2f}.")
        with st.expander("Ver Solución"):
            st.write(f"La media (tiempo esperado) es $\mu = 1/\lambda$.")
            st.code(f"1 / 4 = 0.25 horas")
    
    st.subheader("Ejercicio 2")
    st.write("La vida útil de un chip sigue Exp(λ=0.5 fallos/año). ¿Cuál es la prob. de que dure *más* de 3 años ($P(X > 3)$)?")
    ans2 = st.number_input("Tu respuesta (P(X>3)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='exp_ex2_ans')
    if st.button("Revisar 2", key='exp_ex2_btn'):
        dist_ex = stats.expon(scale=1/0.5)
        correct_ans = dist_ex.sf(3)
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Buscamos $P(X > 3) = 1 - P(X \le 3) = e^{{-\lambda x}}$.")
            st.code(f"stats.expon(scale=1/0.5).sf(3) = {correct_ans:.4f}")
            st.code(f"np.exp(-0.5 * 3) = np.exp(-1.5) = {correct_ans:.4f}")
            
    st.subheader("Ejercicio 3 (Prop. Falta de Memoria)")
    st.write("En el Ej. 2 ($\lambda=0.5$), el chip ya ha durado 2 años. ¿Cuál es la prob. de que dure *al menos* 3 años *más* (es decir, dure 5 años en total)?")
    ans3 = st.number_input("Tu respuesta (P(X>5 | X>2)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='exp_ex3_ans')
    if st.button("Revisar 3", key='exp_ex3_btn'):
        dist_ex = stats.expon(scale=1/0.5)
        correct_ans = dist_ex.sf(3) # ¡Es la misma que el Ej. 2!
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La prob. es {correct_ans:.4f}. Es la misma que $P(X > 3)$.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Por la propiedad de falta de memoria, $P(X > s+t | X > s) = P(X > t)$.")
            st.write("El hecho de que haya sobrevivido 2 años no importa. Buscamos la prob. de que sobreviva 3 años *adicionales*.")
            st.code(f"P(X > 2+3 | X > 2) = P(X > 3) = {correct_ans:.4f}")
