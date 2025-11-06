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

st.title("Distribución de Poisson")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución de Poisson modela el **número de eventos** que ocurren en un **intervalo fijo de tiempo o espacio**, dado que estos eventos ocurren con una tasa media constante e independientemente del tiempo transcurrido desde el último evento.
    
    Es una distribución discreta que se usa para modelar "conteos" de eventos raros.
    
    - **Parámetro:** $\lambda$ (lambda): La tasa media (o valor esperado) de eventos en el intervalo. $\lambda > 0$.
    - **Rango:** La variable $X$ (conteo de eventos) puede tomar valores $k = 0, 1, 2, ...$
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Nombrada en honor al matemático francés **Siméon Denis Poisson** (1837), quien la introdujo como una generalización de la Binomial. Un famoso ejemplo histórico fue modelar el número de soldados del ejército prusiano muertos por patadas de caballo por año.")
    st.markdown("""
    **Casos de Uso:**
    - El número de clientes que llegan a una caja en un supermercado en una hora.
    - El número de llamadas telefónicas recibidas en un *call center* en un minuto.
    - El número de errores tipográficos (erratas) en una página de un libro.
    - El número de partículas radiactivas emitidas por un material en un segundo.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Binomial:** La Poisson es el límite de la Distribución Binomial(n, p) cuando $n \to \infty$ y $p \to 0$, de tal manera que $np = \lambda$ se mantiene constante. Se usa como una **aproximación a la Binomial** cuando $n$ es grande ($n \ge 100$) y $p$ es pequeña ($p \le 0.01$).
    - **Exponencial:** Si los eventos siguen un proceso de Poisson con tasa $\lambda$, el tiempo *entre* los eventos sigue una Distribución Exponencial con parámetro $\lambda$.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Masa de Probabilidad (PMF)")
    st.latex(r"P(X=k) = \frac{\lambda^k e^{-\lambda}}{k!} \quad \text{para } k = 0, 1, 2, \dots")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \lambda")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \lambda")
    st.write("¡Nota: la media y la varianza son idénticas!")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta la tasa media ($\lambda$) para ver cómo cambia la distribución. A medida que $\lambda$ aumenta, la distribución comienza a parecerse a una campana (Normal).")
    
    lambda_slider = st.slider("Tasa media (λ)", min_value=0.1, max_value=30.0, value=5.0, step=0.1, key='poisson_lambda_slider')
    
    if lambda_slider <= 0:
        st.error("Lambda (λ) debe ser positiva.")
    else:
        try:
            dist = stats.poisson(mu=lambda_slider)
            # Graficar hasta k = media + 3 desviaciones estándar (sigma = sqrt(lambda))
            k_max = int(lambda_slider + 4 * np.sqrt(lambda_slider))
            k_values = np.arange(0, k_max + 1)
            
            fig = plot_discrete_distribution(dist, k_values, f"PMF de Poisson (λ={lambda_slider:.1f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva")
    st.write("Calcula $P(X=k)$ (PMF) y $P(X \le k)$ (CDF) para una Poisson.")
    
    col1, col2 = st.columns(2)
    with col1:
        calc_lambda = st.number_input("Tasa media (λ)", min_value=0.01, value=5.0, step=0.1, key='poisson_calc_lambda')
    with col2:
        calc_k = st.number_input("Número de eventos (k)", min_value=0, value=5, step=1, key='poisson_calc_k')

    if calc_lambda <= 0:
        st.error("'λ' debe ser positiva.")
    elif calc_k < 0:
        st.error("'k' debe ser >= 0.")
    else:
        try:
            dist = stats.poisson(mu=calc_lambda)
            prob_k = dist.pmf(calc_k)
            prob_cdf = dist.cdf(calc_k)
            prob_gt_k = 1 - prob_cdf # P(X > k)
            
            st.subheader("Resultados:")
            st.markdown(f"**$P(X = {calc_k})$:** `{prob_k:.6f}` (Prob. de *exactamente* {calc_k} eventos)")
            st.markdown(f"**$P(X \le {calc_k})$:** `{prob_cdf:.6f}` (Prob. de *como máximo* {calc_k} eventos)")
            st.markdown(f"**$P(X > {calc_k})$:** `{prob_gt_k:.6f}` (Prob. de *más de* {calc_k} eventos)")
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
            
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Atención al Cliente:** Un banco recibe un promedio de 10 clientes por hora ($\lambda=10$). ¿Cuál es la prob. de que reciba exactamente 8 clientes en una hora? ($k=8$).
    2.  **Calidad Textil:** Una fábrica de alfombras encuentra un promedio de 0.8 defectos por metro cuadrado ($\lambda=0.8$). ¿Cuál es la prob. de que un metro cuadrado no tenga ningún defecto? ($k=0$).
    3.  **Gestión de Emergencias:** Una estación de bomberos recibe un promedio de 3 llamadas por día ($\lambda=3$). ¿Cuál es la prob. de que reciba 5 o más llamadas en un día? (Calcular $P(X \ge 5) = 1 - P(X \le 4)$).
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1")
    st.write("Un hospital recibe un promedio de 4 pacientes con gripe por hora ($\lambda=4$). ¿Cuál es la prob. de que reciba *exactamente* 4 pacientes en la próxima hora ($k=4$)?")
    ans1 = st.number_input("Tu respuesta (P(X=4)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='poisson_ex1_ans')
    if st.button("Revisar 1", key='poisson_ex1_btn'):
        correct_ans = stats.poisson.pmf(k=4, mu=4)
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Usamos la PMF de Poisson: $P(X=4) = \\frac{{4^4 e^{{-4}}}}{{4!}}$")
            st.code(f"stats.poisson.pmf(k=4, mu=4) = {correct_ans:.4f}")
    
    st.subheader("Ejercicio 2")
    st.write("En el mismo hospital ($\lambda=4$), ¿cuál es la prob. de que reciba *como máximo* 2 pacientes? ($k=2$)")
    ans2 = st.number_input("Tu respuesta (P(X≤2)):", min_value=0.0, max_value=1.0, step=0.001, format="%.4f", key='poisson_ex2_ans')
    if st.button("Revisar 2", key='poisson_ex2_btn'):
        correct_ans = stats.poisson.cdf(k=2, mu=4)
        if np.isclose(ans2, correct_ans):
            st.success(f"¡Correcto! La probabilidad es {correct_ans:.4f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.4f}.")
        with st.expander("Ver Solución"):
            st.write(f"Buscamos $P(X \le 2) = P(X=0) + P(X=1) + P(X=2)$.")
            st.code(f"stats.poisson.cdf(k=2, mu=4) = {correct_ans:.4f}")
            
    st.subheader("Ejercicio 3")
    st.write("Un sitio web recibe un promedio de $\lambda=9$ visitantes por minuto. ¿Cuál es la varianza $\sigma^2$ del número de visitantes por minuto?")
    ans3 = st.number_input("Tu respuesta (Varianza σ²):", min_value=0.0, step=0.1, format="%.1f", key='poisson_ex3_ans')
    if st.button("Revisar 3", key='poisson_ex3_btn'):
        correct_ans = 9.0
        if np.isclose(ans3, correct_ans):
            st.success(f"¡Correcto! La varianza es {correct_ans:.1f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.1f}.")
        with st.expander("Ver Solución"):
            st.write(f"Para una distribución de Poisson, la varianza es siempre igual a la media.")
            st.code(f"μ = λ = 9, por lo tanto σ² = λ = 9.0")
