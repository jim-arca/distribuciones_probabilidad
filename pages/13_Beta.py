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

st.title("Distribución Beta")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Teoría y Fórmulas", "Visualización", "Calculadora", "Ejemplos", "Ejercicios"
])

with tab1:
    st.header("Concepto Teórico")
    st.write("""
    La Distribución Beta es una distribución continua definida en el intervalo **$[0, 1]$**. Es extremadamente útil para modelar **proporciones, porcentajes, o probabilidades**.
    
    Es la "distribución de las probabilidades". Mientras una Binomial modela cuántos éxitos *ocurren*, la Beta puede modelar la *probabilidad subyacente* $p$ de que ocurran.
    
    - **Parámetros:**
        - $\alpha$ (alfa): Parámetro de forma ($ \alpha > 0 $). Se puede interpretar como "número de éxitos + 1".
        - $\beta$ (beta): Parámetro de forma ($ \beta > 0 $). Se puede interpretar como "número de fracasos + 1".
    - **Rango:** La variable $X$ (la proporción) puede tomar cualquier valor $x \in [0, 1]$.
    """)
    st.write("La forma de la distribución cambia drásticamente según $\alpha$ y $\beta$:")
    st.markdown("""
    - $\alpha=1, \beta=1$: **Uniforme Continua** (todos los valores igual de probables).
    - $\alpha > 1, \beta > 1$: Forma de campana, unimodal.
    - $\alpha < 1, \beta < 1$: Forma de U (más probable en los extremos 0 o 1).
    - $\alpha=1, \beta > 1$: Decreciente.
    - $\alpha > 1, \beta=1$: Creciente.
    """)

    st.header("Contexto Histórico y Casos de Uso")
    st.write("Es fundamental en la **Inferencia Bayesiana**, donde se usa como la distribución *a priori* para una probabilidad binomial. Fue estudiada por Thomas Bayes y Pierre-Simon Laplace.")
    st.markdown("""
    **Casos de Uso:**
    - **Bayesiana:** Modelar la incertidumbre sobre la probabilidad $p$ de una moneda (ej. $\alpha$=clics, $\beta$=no-clics).
    - **Proporciones:** El porcentaje de votantes que apoyan a un candidato.
    - **Gestión de Tareas (PERT):** La distribución PERT es un caso especial re-escalado de la Beta.
    - **Datos Fraccionales:** La fracción de un día que un servidor está activo.
    """)

    st.header("Relación con Otras Distribuciones")
    st.write("""
    - **Uniforme Continua:** Es un caso especial de la Beta($\alpha=1, \beta=1$).
    - **Binomial:** La Beta es la distribución conjugada a priori de la Binomial en estadística Bayesiana.
    """)

    st.header("Fórmulas Matemáticas")
    st.subheader("Función de Densidad de Probabilidad (PDF)")
    st.latex(r"f(x) = \frac{x^{\alpha-1} (1-x)^{\beta-1}}{B(\alpha, \beta)}")
    st.write(r"Donde $B(\alpha, \beta) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$ es la función Beta (que usa la función Gamma $\Gamma$).")
    
    st.subheader("Media (Valor Esperado)")
    st.latex(r"\mu = E[X] = \frac{\alpha}{\alpha + \beta}")
    
    st.subheader("Varianza")
    st.latex(r"\sigma^2 = \text{Var}(X) = \frac{\alpha \beta}{(\alpha + \beta)^2 (\alpha + \beta + 1)}")

with tab2:
    st.header("Visualización Interactiva")
    st.write("Ajusta $\alpha$ y $\beta$ para ver la increíble flexibilidad de la Beta.")
    
    col1, col2 = st.columns(2)
    with col1:
        alpha_slider = st.slider("Forma (α)", min_value=0.1, max_value=20.0, value=2.0, step=0.1, key='beta_alpha')
    with col2:
        beta_slider = st.slider("Forma (β)", min_value=0.1, max_value=20.0, value=5.0, step=0.1, key='beta_beta')

    if alpha_slider <= 0 or beta_slider <= 0:
        st.error("Alfa (α) y Beta (β) deben ser positivos.")
    else:
        try:
            dist = stats.beta(a=alpha_slider, b=beta_slider)
            
            # El rango es siempre 0 a 1
            x_min = 0
            x_max = 1
            
            fig = plot_continuous_distribution(dist, x_min, x_max, f"PDF Beta (α={alpha_slider:.1f}, β={beta_slider:.1f})")
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"Error al generar el gráfico: {e}")

with tab3:
    st.header("Calculadora Interactiva (Conceptual)")
    st.write("Calcula la Media y Varianza. (Grupo 2)")
    
    st.subheader("Parámetros")
    col1, col2 = st.columns(2)
    with col1:
        calc_alpha = st.number_input("Forma (α)", min_value=0.01, value=2.0, step=0.1, key='beta_calc_alpha')
    with col2:
        calc_beta = st.number_input("Forma (β)", min_value=0.01, value=5.0, step=0.1, key='beta_calc_beta')

    if calc_alpha <= 0 or calc_beta <= 0:
        st.error("'α' y 'β' deben ser positivos.")
    else:
        try:
            dist = stats.beta(a=calc_alpha, b=calc_beta)
            
            st.subheader("Estadísticos:")
            st.markdown(f"**Media (μ = α / (α+β)):** `{dist.mean():.4f}`")
            st.markdown(f"**Varianza (σ²):** `{dist.var():.4f}`")
            st.markdown(f"**Modo:** `{ (calc_alpha-1) / (calc_alpha + calc_beta - 2) :.4f}` (si $\alpha>1, \beta>1$)")
            
            st.subheader("Nota Pedagógica sobre Cálculo de Probabilidad")
            st.info("""
            **Esta distribución pertenece al GRUPO 2.**
            
            En la práctica, los valores de probabilidad (CDF) para la distribución Beta no se calculan a mano. La CDF (Función de Distribución Acumulada) se conoce como la **función beta incompleta regularizada**, y es una función especial que solo se puede calcular con métodos numéricos.
            
            Por esta razón, los valores se obtienen de **software estadístico** (como R, Python con SciPy, o Excel) que tienen estas funciones implementadas.
            """)
                
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab4:
    st.header("Ejemplos Aplicados")
    st.markdown("""
    1.  **Tasa de Clics (CTR):** Un anuncio se muestra 100 veces, con 10 clics y 90 no-clics. La incertidumbre sobre la tasa de clics $p$ se puede modelar como Beta($\alpha=10+1, \beta=90+1$). La media es $11/102 \approx 10.8\%$.
    2.  **Opinión de Producto:** 50 reseñas de 5 estrellas ($\alpha=50$) y 20 reseñas de 1 estrella ($\beta=20$). La "puntuación" subyacente puede modelarse como Beta(50, 20).
    3.  **Prior Bayesiano:** Si no sabemos nada sobre $p$, podemos usar Beta(1, 1) (Uniforme), que dice que cualquier $p$ entre 0 y 1 es igualmente probable.
    """)

with tab5:
    st.header("Ejercicios Interactivos")
    
    st.subheader("Ejercicio 1: Media")
    st.write("Un bateador tiene $\alpha=30$ (hits) y $\beta=70$ (outs). ¿Cuál es su promedio de bateo esperado (Media)?")
    st.write(r"(Usar $E[X] = \alpha / (\alpha + \beta)$)")
    ans1 = st.number_input("Tu respuesta (Media μ):", min_value=0.0, max_value=1.0, step=0.001, format="%.3f", key='beta_ex1_ans')
    if st.button("Revisar 1", key='beta_ex1_btn'):
        correct_ans = 30 / (30 + 70)
        if np.isclose(ans1, correct_ans):
            st.success(f"¡Correcto! La media es {correct_ans:.3f}.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es {correct_ans:.3f}.")
        with st.expander("Ver Solución"):
            st.write(f"La media es $\mu = \alpha / (\alpha + \beta)$.")
            st.code(f"30 / (30 + 70) = 30 / 100 = 0.300")
    
    st.subheader("Ejercicio 2: Identificación")
    st.write("¿Qué distribución Beta es idéntica a la Uniforme Continua en [0, 1]?")
    col1, col2 = st.columns(2)
    with col1:
        ans_a = st.number_input("Valor de α:", min_value=0, step=1, key='beta_ex2_a')
    with col2:
        ans_b = st.number_input("Valor de β:", min_value=0, step=1, key='beta_ex2_b')
    
    if st.button("Revisar 2", key='beta_ex2_btn'):
        if ans_a == 1 and ans_b == 1:
            st.success("¡Correcto! Beta(1, 1) es la Distribución Uniforme.")
        else:
            st.error(f"Incorrecto. La respuesta correcta es α=1 y β=1.")
        
    st.subheader("Ejercicio 3: Forma")
    st.write("Si $\alpha=0.5$ y $\beta=0.5$, ¿dónde es más probable que esté el valor de $X$?")
    ans3 = st.text_input("Tu respuesta (Ej: 'cerca del centro', 'cerca de los extremos'):", key='beta_ex3_ans').strip().lower()
    if st.button("Revisar 3", key='beta_ex3_btn'):
        if "extremos" in ans3 or "0 o 1" in ans3 or "cero o uno" in ans3:
            st.success("¡Correcto! Es una forma de 'U', más probable cerca de 0 o 1.")
        else:
            st.error(f"Incorrecto. La respuesta es 'cerca de los extremos'.")
        with st.expander("Ver Solución"):
            st.write(f"Cuando $\alpha < 1$ y $\beta < 1$, la distribución tiene forma de U, lo que significa que los valores en el medio son *menos* probables que los valores en los extremos 0 y 1.")
